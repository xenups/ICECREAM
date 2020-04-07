"ICECREAM"

from uuid import uuid4
from bottle import HTTPError
from ICECREAM.cache import RedisCache
from marshmallow import ValidationError
from app_signup.schemas import SMSSchema
from ICECREAM.util import generate_otp_code
from send_message.send_message import send_message
from app_signup.repository.user_repository import user_by_cell_number

valid_activating_interval = 86400
valid_registering_interval = 200


def account_activation(data, db_session):
    try:
        SMSSchema().load(data)
    except ValidationError as err:
        return err.messages

    cache = RedisCache()
    cell_number = data.get('cell_number')

    if user_by_cell_number(cell_no=cell_number, db_session=db_session):
        raise HTTPError(409, body='USER_ALREADY_EXISTS')

    if cache.get_cache_multiple_value(cell_number, 'activation_code'):
        raise HTTPError(403, ' Message.ALREADY_HAS_VALID_KEY')

    activation_code = generate_otp_code()
    if send_message(cell_number=cell_number, activation_code=activation_code):
        cache.set_cache_multiple_value(key=cell_number, value=activation_code, custom_value_name='activation_code',
                                       ttl=valid_registering_interval)
    else:
        raise HTTPError(403, ' Message.Didnt send')

    result = {'msg': ' Message.MESSAGE_SENT' + cell_number}
    return result


def account_validation(data, db_session):
    cache = RedisCache()
    cell_number = data.get('cell_no')
    if user_by_cell_number(cell_number, db_session):
        raise HTTPError(409, body='USER_ALREADY_EXISTS')

    activation_code = cache.get_cache_multiple_value(cell_number, 'activation_code')

    if activation_code is None or activation_code != data.get('activation_code'):
        raise HTTPError(204, body='NO_VALID_ACTIVATION_CODE')

    signup_token = str(uuid4())
    cache.set_cache_multiple_value(cell_number, signup_token, 'signup_token', valid_activating_interval)

    data = {'cell_no': cell_number, 'signup_token': signup_token}
    return data
