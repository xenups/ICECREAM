"ICECREAM"
from ICECREAM import status
from sqlalchemy.orm import Session
from ICECREAM.http import HTTPResponse
from ICECREAM.models.query import get_object_or_404
from ICECREAM.paginator import Paginate
from ICECREAM.file_handler import upload
from app_foo.models import Room, RoomImage
from ICECREAM.validators import validate_data
from ICECREAM.filters import MongoFilter, get_query_from_url
from app_foo.schemas import room_serializer, room_image_serializer, rooms_serializer


def get_rooms(db_session):
    rooms = db_session.query(Room).all()
    result = rooms_serializer.dump(rooms)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def get_room(pk, db_session: Session):
    room = get_object_or_404(Room, db_session, Room.id == pk)
    result = room_serializer.dump(room)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def filter_rooms(db_session: Session):
    # /rooms/filter?query={"sort":"name-",}
    rooms_query = db_session.query(Room)
    query = get_query_from_url("query")
    filtered_query = MongoFilter(Room, rooms_query, query).filter()
    result = Paginate(filtered_query, rooms_serializer)
    return HTTPResponse(status=200, body=result)


def new_room(db_session, data):
    validate_data(data=data, serializer=room_serializer)
    room = Room()
    room.name = data['name']
    db_session.add(room)
    db_session.commit()
    result = room_serializer.dump(db_session.query(Room).get(room.id))
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def add_room_image(db_session, data):
    validate_data(data=data, serializer=room_image_serializer)
    room_image = RoomImage()
    room_image.name = upload(data=data)
    room_image.room_id = data['room_id']
    db_session.add(room_image)
    db_session.commit()
    room_image = db_session.query(RoomImage).get(room_image.id)
    result = room_image_serializer.dump(room_image)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)
