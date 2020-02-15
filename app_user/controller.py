"ICECREAM"
from bottle import HTTPResponse
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from ICECREAM.models.query import get_or_create
from app_user.models import User, Person
from app_user.schemas import UserSchema, user_serializer, users_serializer


def get_users(db_session):
    try:
        user = db_session.query(User).all()
        print(user)
        user = users_serializer.dump(user)
        return HTTPResponse(status=200, body={'users': user})
    except NoResultFound as e:
        raise e


def new_user(db_session, data):
    try:
        user_serializer.load(data)
        person = data['person']
        name = person['name']
        last_name = person['last_name']
        phone = person['phone']
        bio = person['bio']
        username = data['username']

        person = get_or_create(Person, db_session, name=name, phone=phone)
        person.name = name
        person.last_name = last_name
        person.phone = phone
        person.bio = bio
        db_session.add(person)

        user = get_or_create(User, db_session, username=username)
        user.username = username
        user.set_password(data['password'])
        user.person = person
        db_session.add(user)
        db_session.commit()
        result = user_serializer.dump(db_session.query(User).get(user.id))
        return HTTPResponse(status=200, body={'result': result})
    except SQLAlchemyError as err:
        print(err)
        return err
