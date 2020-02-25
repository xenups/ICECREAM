"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_signup.controller import activate_account, register


class SignUpApp(BaseApp):
    def call_router(self, core):
        core.route('/register/activate-account', 'POST', activate_account, apply=[db_handler, pass_data, jsonify])
        core.route('/register/send-code', 'POST', register, apply=[db_handler, pass_data, jsonify])
