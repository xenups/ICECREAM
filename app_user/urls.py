"ICECREAM"
from ICECREAM.baseapp import BaseApp
from bottle_jwt import jwt_auth_required
from app_user.controller import get_users, create_user, new_message
from ICECREAM.wrappers import db_handler, pass_data, jsonify


class USERApp(BaseApp):
    def call_router(self, core):
        core.route('/getusers', 'GET', get_users, apply=[db_handler, jsonify, jwt_auth_required])
        core.route('/adduser', 'POST', create_user, apply=[pass_data, db_handler, jsonify])
        core.route('/createmessage', 'POST', new_message, apply=[pass_data, db_handler, jsonify])
