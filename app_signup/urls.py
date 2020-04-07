"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_signup.controller import account_validation, account_activation


class SignUpApp(BaseApp):
    def call_router(self, core):
        core.route('/register/validate-account', 'POST', account_validation, apply=[db_handler, pass_data, jsonify])
        core.route('/register/activate-account', 'POST', account_activation, apply=[db_handler, pass_data, jsonify])
