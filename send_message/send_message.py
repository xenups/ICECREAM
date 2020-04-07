import requests
from bottle import HTTPError
from kavenegar import *

from settings import sms

# sms_token_url = sms['sms_token_url']
# sms_security_key = sms['sms_security_key']
# sms_timeout = sms['sms_timeout']
# sms_send_url = sms['sms_send_url']
# sms_line_no = sms['sms_line_no']

sms_api_key = sms['sms_api_key']


def send_message(cell_number, activation_code):
    data = {'receptor': cell_number,
            'token': activation_code,
            'type': 'sms',
            'template': 'ratingregister'}

    receptor = cell_number
    if receptor.startswith('0999'):
        data['receptor'] = '09210419379'
    if sms_api_key is None:
        raise HTTPError(400, 'MISSING_REQUIERED_FIELD')
    try:
        api = KavenegarAPI(sms_api_key)
        params = data
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        return {'status': 500}
    except HTTPException as e:
        return {'status': 500}
    return {'status': 200}
