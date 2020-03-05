"ICECREAM"
import logging
from bottle import HTTPError
from ICECREAM.file_handler import upload
from app_foo.models import Room, RoomImage
from app_foo.schemas import RoomSchema, room_serializer, room_image_serializer


def hello():
    return {"result": 'hellow world'}


def get_rooms(db_session):
    try:
        rooms = db_session.query(Room).all()
        serializer = RoomSchema(many=True)
        result = serializer.dump(rooms)
        return result
    except Exception as e:
        logging.error(e)
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def new_room(db_session, data):
    validation_errors = room_serializer.validate(data=data)
    if validation_errors:
        return validation_errors
    try:
        room = Room()
        room.name = data['name']
        db_session.add(room)
        db_session.commit()
        # result = room_serializer.dump(db_session.query(Room).get(room.id))
        result = db_session.query(Room).get(room.id)
        return result
    except Exception as err:
        raise err


def add_room_image(db_session, data):
    validation_errors = room_image_serializer.validate(data=data)
    if validation_errors:
        return validation_errors
    room_image = RoomImage()
    room_image.name = upload(data=data)
    room_image.room_id = data['room_id']
    db_session.add(room_image)
    db_session.commit()

    result = db_session.query(RoomImage).get(room_image.id)
    dumped_result = room_image_serializer.dump(result)

    return dumped_result
