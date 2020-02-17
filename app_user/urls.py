"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_user.controller import get_users, new_user


class USERApp(BaseApp):
    def call_router(self, core):
        core.route('/getusers', 'GET', get_users, apply=[db_handler, jsonify])
        core.route('/adduser', 'POST', new_user, apply=[pass_data, db_handler, jsonify])
