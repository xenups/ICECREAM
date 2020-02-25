"ICECREAM"
import json
import random
from uuid import uuid4

from bottle import HTTPError

import redis
from marshmallow import ValidationError

from app_signup.repository.user_repository import check_user_exist_by_cell_number
from app_signup.schemas import SMSSchema
from send_message.send_message import send_message

redis_app = redis.Redis()

valid_activating_interval = 86400
valid_registering_interval = 200


def activate_account(data, db_session):
    print('hi')
    # redis = get_redis()
    # redis = redis_connector()
    cell_number = data.get('cell_no')
    if check_user_exist_by_cell_number(cell_number, db_session):
        raise HTTPError(409, body='USER_ALREADY_EXISTS')
    cell_data = redis_app.get(cell_number)
    if cell_data is None:
        raise HTTPError(204, body='NO_VALID_ACTIVATION_CODE')

    activation_code = (json.loads(cell_data.decode("utf-8"))).get(
        'activation_code', None)

    if activation_code is None:
        raise HTTPError(204, body='NO_VALID_ACTIVATION_CODE')

    if activation_code != data.get('activation_code'):
        raise HTTPError(409, body='WRONG_ACTIVATION_CODE')

    signup_token = str(uuid4())
    redis_app.delete(cell_number)
    redis_app.set(cell_number, json.dumps({'signup_token': signup_token}),
                  ex=valid_activating_interval)

    data = {'cell_no': cell_number, 'signup_token': signup_token}
    return data


def register(data, db_session):
    try:
        SMSSchema().load(data)
    except ValidationError as err:
        return err.messages
    cell_no = data.get('cell_no')
    if check_user_exist_by_cell_number(cell_no, db_session):
        raise HTTPError(409, body='USER_ALREADY_EXISTS')
    cell_data = redis_app.get(cell_no)

    if cell_data:
        activation_code = (json.loads(cell_data.decode('utf-8'))).get(
            'activation_code', None)
        if activation_code:
            raise HTTPError(403, ' Message.ALREADY_HAS_VALID_KEY')
        else:
            redis_app.delete(cell_no)
    password = str(random.randint(1000, 9999))
    data = {'receptor': cell_no,
            'token': password,
            'type': 'sms',
            'template': 'ratingregister'}
    sent_data = send_message(data)
    print(sent_data)

    redis_app.set(cell_no, json.dumps({'activation_code': password}),
                  ex=valid_registering_interval)
    result = {'msg': ' Message.MESSAGE_SENT' + cell_no}
    return result

