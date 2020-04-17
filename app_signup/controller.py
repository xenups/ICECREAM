"ICECREAM"
from uuid import uuid4
from ICECREAM.http import HTTPError
from ICECREAM.cache import RedisCache
from marshmallow import ValidationError
from app_signup.schemas import SMSSchema
from app_user.models import User, Person
from ICECREAM.util import generate_otp_code
from ICECREAM.models.query import is_object_exist_409
from send_message.send_message import send_message

valid_activating_interval = 86400
valid_registering_interval = 200


def phone_activation(data, db_session):
    try:
        SMSSchema().load(data)
    except ValidationError as err:
        return err.messages
    cache = RedisCache()
    phone = data.get('phone')
    is_object_exist_409(User, db_session, User.phone == phone)
    if cache.get_cache_multiple_value(phone, 'activation_code'):
        raise HTTPError(403, ' Phone already has valid activation code')
    activation_code = generate_otp_code()
    if send_message(cell_number=phone, activation_code=activation_code):
        cache.set_cache_multiple_value(key=phone, value=activation_code, custom_value_name='activation_code',
                                       ttl=valid_registering_interval)
    else:
        raise HTTPError(403, ' Message.Didnt send')
    result = {'msg': ' Message.MESSAGE_SENT' + phone}
    return result


def phone_validation(data, db_session):
    cache = RedisCache()
    cell_number = data.get('phone')
    is_object_exist_409(User, db_session, User.phone == cell_number)

    activation_code = cache.get_cache_multiple_value(cell_number, 'activation_code')

    if activation_code is None or activation_code != data.get('activation_code'):
        raise HTTPError(404, body='Validation code is not valid')

    signup_token = str(uuid4())
    cache.set_cache_multiple_value(cell_number, signup_token, 'signup_token', valid_activating_interval)

    data = {'phone': cell_number, 'signup_token': signup_token}
    return data
