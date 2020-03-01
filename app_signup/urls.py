"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_signup.controller import validation_account, activation_account


class SignUpApp(BaseApp):
    def call_router(self, core):
        core.route('/register/validate-account', 'POST', validation_account, apply=[db_handler, pass_data, jsonify])
        core.route('/register/activate-account', 'POST', activation_account, apply=[db_handler, pass_data, jsonify])
