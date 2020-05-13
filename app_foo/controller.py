"ICECREAM"
import logging
from ICECREAM.file_handler import upload
from ICECREAM.http import HTTPResponse
from ICECREAM.validators import validate_data
from app_foo.models import Room, RoomImage
from app_foo.schemas import RoomSchema, room_serializer, room_image_serializer


def hello():
    return {"result": 'hellow world'}


def get_rooms(db_session):
    rooms = db_session.query(Room).all()
    serializer = RoomSchema(many=True)
    result = serializer.dump(rooms)
    return HTTPResponse(status=200, body=result)


def new_room(db_session, data):
    validate_data(data=data, serializer=room_serializer)
    room = Room()
    room.name = data['name']
    db_session.add(room)
    db_session.commit()
    result = room_serializer.dump(db_session.query(Room).get(room.id))
    return HTTPResponse(status=200, body=result)


def add_room_image(db_session, data):
    validate_data(data=data, serializer=room_image_serializer)
    room_image = RoomImage()
    room_image.name = upload(data=data)
    room_image.room_id = data['room_id']
    db_session.add(room_image)
    db_session.commit()
    room_image = db_session.query(RoomImage).get(room_image.id)
    result = room_image_serializer.dump(room_image)
    return HTTPResponse(status=200, body=result)
