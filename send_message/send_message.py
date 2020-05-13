import requests
from kavenegar import *
from settings import sms
from ICECREAM.http import HTTPError

# sms_token_url = sms['sms_token_url']
# sms_security_key = sms['sms_security_key']
# sms_timeout = sms['sms_timeout']
# sms_send_url = sms['sms_send_url']
# sms_line_no = sms['sms_line_no']

sms_api_key = sms['sms_api_key']


class SMS(object):
    def __init__(self):
        self.api = KavenegarAPI(sms_api_key)

    def __send_sms(self, data):
        receptor = data.get("receptor")
        if receptor.startswith('0999'):
            data['receptor'] = '09210419379'
        if sms_api_key is None:
            raise HTTPError(400, 'MISSING_REQUIERED_FIELD')
        try:
            params = data
            response = self.api.verify_lookup(params)
        except APIException as e:
            return {'status': 500}
        except HTTPException as e:
            return {'status': 500}
        return {'status': 200}

    def send_activation_code(self, cell_number, activation_code):
        try:
            data = {'receptor': cell_number,
                    'token': activation_code,
                    'type': 'sms',
                    'template': 'ratingregister'}
            self.__send_sms(data)
            return True
        except Exception as error:
            return False

    def send_forget_password(self, cell_number, username, password):
        try:
            data = {'receptor': cell_number,
                    'token': username,
                    'token2': password,
                    'type': 'sms',
                    'template': 'fajrresetPassword'}
            self.__send_sms(data)
            return True
        except Exception as error:
            return False
