"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_signup.controller import phone_validation, phone_activation


class SignUpApp(BaseApp):
    def call_router(self, core):
        core.route('/register/activate-phone', 'POST', phone_activation, apply=[db_handler, pass_data, jsonify])
        core.route('/register/validate-phone', 'POST', phone_validation, apply=[db_handler, pass_data, jsonify])
