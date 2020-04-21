"ICECREAM"
import bottle
from sqlalchemy.orm import Session
from sqlalchemy_filters import apply_filters

from ICECREAM.cache import RedisCache
from ICECREAM.paginator import Paginate
from app_user.models import User, Person
from send_message.send_message import SMS
from ICECREAM.util import generate_otp_code
from ICECREAM.rbac import get_user_identity
from ICECREAM.http import HTTPError, HTTPResponse
from ICECREAM.models.query import get_or_create, get_object, is_object_exist_409, get_object_or_404
from app_user.schemas import users_serializer, user_serializer, forget_pass_serializer, reset_password_serializer

forget_password_ttl = 600


def get_users(db_session):
    try:
        page_number = bottle.request.GET.get('page') or 1
        page_size = bottle.request.GET.get('count') or 10
        users = db_session.query(User)
        return Paginate(users, int(page_number), int(page_size), users_serializer)
    except Exception as e:
        raise HTTPError(status=404, body=e.args)


def get_user(pk, db_session):
    user = get_object_or_404(User, db_session, User.id == pk)
    result = user_serializer.dump(user)
    raise HTTPResponse(status=200, body=result)


def delete_user(pk, db_session):
    identity = get_user_identity(db_session)
    if identity.check_permission("delete_user", User):
        user = get_object_or_404(User, db_session, User.id == pk)
        db_session.delete(user)
        db_session.commit()
        raise HTTPResponse(status=204, body="Successfully deleted !")
    raise HTTPError(status=403, body="Access denied")


def create_user(db_session, data):
    validation_errors = user_serializer.validate(data)
    if validation_errors:
        raise HTTPError(404, validation_errors)
    identity = get_user_identity(db_session)
    if identity.check_permission("add_user", User):
        is_object_exist_409(User, db_session, User.phone == data['phone'])
        person = data['person']
        person_obj = get_or_create(Person, db_session, name=person['name'])
        person_obj.name = person['name']
        person_obj.last_name = person['last_name']
        person_obj.email = person['email']
        db_session.add(person_obj)
        user = get_or_create(User, db_session, phone=data['phone'])
        user.phone = data['phone']
        user.set_roles(data['roles'])
        user.username = user.get_phone
        user.set_password(data['password'])
        user.person = person_obj
        db_session.add(user)
        db_session.commit()
        result = user_serializer.dump(db_session.query(User).get(user.id))
        return result
    raise HTTPError(403, "Access denied")


def forget_pass(db_session, data):
    validation_errors = forget_pass_serializer.validate(data)
    if validation_errors:
        raise HTTPError(404, validation_errors)
    cache = RedisCache()
    phone = data.get('phone')
    get_object_or_404(User, db_session, User.phone == phone)
    if cache.get_cache_multiple_value(phone, 'forget_password_token'):
        raise HTTPError(403, ' Phone already has valid  code')
    forget_password_token = generate_otp_code()
    # celery
    if SMS().send_forget_password(phone, phone, forget_password_token):
        cache.set_cache_multiple_value(key=phone, value=forget_password_token,
                                       custom_value_name='forget_password_token',
                                       ttl=forget_password_ttl)
    else:
        raise HTTPError(403, ' Message Didnt send')
    raise HTTPResponse(200, 'Message sent')


def reset_pass(data, db_session: Session):
    validation_errors = reset_password_serializer.validate(data)
    if validation_errors:
        raise HTTPError(404, validation_errors)
    cache = RedisCache()
    phone = data.get('phone')
    user = get_object_or_404(User, db_session, User.phone == phone)
    forget_password_token = cache.get_cache_multiple_value(phone, 'forget_password_token')
    if forget_password_token is None or forget_password_token != data.get('token'):
        raise HTTPError(404, body='code is not valid')
    user.set_password(password=data.get('password'))
    db_session.commit()
    result = reset_password_serializer.dump(user)
    return result


# def filters(query):
#     _filters = bottle.request.query.smart_filters()
#     query_filters = []
#     print(_filters.items())
    # for field, value in _filters.items():
    #     _filter = {'field': str(field), 'op': '==', 'value': str(value)}
    #     query_filters.append(_filter)
    # return apply_filters(query, query_filters)


def new_message(db_session, data):
    pass
    # query = db_session.query(User).join(Person)

    # filter_spec = [{'model': 'User', 'field': 'phone', 'op': '==', 'value': '09210419379'},
    #                {'model': 'Person', 'field': 'name', 'op': '==', 'value': "amir"}]
    # filtered_query = apply_filters(query, filter_spec)

    # result = filtered_query.all()
    # print(result)
    # users = db_session.query(User)
    # us = filters(query)
    # print(us)
    # for f in us:
    #     print(f.person.name)

    # filter_spec = [{'field': 'phone', 'op': '==', 'value': '09210419379'},
    #                {'field': 'email', 'op': '==', 'value': 'xenups@gmail.com'}]
    # users = db_session.query(User)
    # filtered_query = apply_filters(users, filter_spec)
    # for f in filtered_query:
    #     user = User()
    #     user = f
    #     print(user)
    #     d= user_serializer.dump(user)
    #     print(d)

    # print(user.person.name)
    # identity = get_user_identity(db_session)
    # if identity.check_permission("create", Message):
    #     print("man staff am va mitunam add konam")
    # if identity.check_permission("edit", Message):
    #     print("man admin am va mitunam edit konam")
