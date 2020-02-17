"ICECREAM"
from bottle import HTTPResponse, HTTPError
from bottle_jwt import jwt_auth_required
from marshmallow import Schema, fields, ValidationError
from app_foo.models import Room
from app_foo.schemas import RoomSchema, room_serializer


def get_rooms(db_session):
    try:
        rooms = db_session.query(Room).all()
        serializer = RoomSchema(many=True)
        result = serializer.dump(rooms)

        return rooms
        # return HTTPResponse(status=200, body={'result': result})
    except Exception as e:
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def new_room(db_session, data):
    try:
        room_serializer.load(data)
        room = Room()
        room.name = data['name']
        db_session.add(room)
        db_session.commit()
        result = room_serializer.dump(db_session.query(Room).get(room.id))
        # return HTTPResponse(status=200, body={'result': result})
        return result
    except ValidationError as err:
        return err.messages
