"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import  pass_data
from app_signup.controller import phone_validation, phone_activation


class SignUpApp(BaseApp):
    def call_router(self, core):
        core.route('/register/activate-phone', 'POST', phone_activation, apply=[pass_data])
        core.route('/register/validate-phone', 'POST', phone_validation, apply=[pass_data])
