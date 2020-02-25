"ICECREAM"
import logging
import sys

from bottle import HTTPResponse, HTTPError
from bottle_jwt import jwt_auth_required
from marshmallow import Schema, fields, ValidationError

from ICECREAM.wrappers import model_to_dict
from app_foo.models import Room
from app_foo.schemas import RoomSchema, room_serializer


def get_rooms(db_session):
    try:
        rooms = db_session.query(Room).all()
        serializer = RoomSchema(many=True)
        return rooms
    except Exception as e:
        logging.error(e)
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def new_room(db_session, data):
    try:
        try:
            room_serializer.load(data)
        except ValidationError as err:
            return err.messages
        room = Room()
        room.name = data['name']
        db_session.add(room)
        db_session.commit()
        # result = room_serializer.dump(db_session.query(Room).get(room.id))
        result = db_session.query(Room).get(room.id)
        return result
    except Exception as err:
        raise err
