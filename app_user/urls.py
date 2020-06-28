"ICECREAM"
from bottle_jwt import jwt_auth_required

from ICECREAM.baseapp import BaseApp
from app_user.controller import get_users, create_user, get_user, activate_user, forget_pass, reset_pass, edit_user, \
    add_person_image, get_rules, get_roles, set_user_role, change_password, get_current_user, remove_person_image
from ICECREAM.wrappers import db_handler, pass_data, debug


class USERApp(BaseApp):
    def call_router(self, core):
        core.route('/api/users/<pk>', 'GET', get_user, apply=[debug, jwt_auth_required])
        core.route('/api/users', 'GET', get_users, apply=[])
        core.route('/api/users/current', 'GET', get_current_user, apply=[debug, jwt_auth_required])
        core.route('/api/users/<pk>', 'PATCH', edit_user, apply=[pass_data, jwt_auth_required])
        core.route('/api/user', 'POST', create_user, apply=[pass_data, jwt_auth_required])
        core.route('/api/user/activate/<pk>', 'PATCH', activate_user, apply=[pass_data, db_handler, jwt_auth_required])
        core.route('/api/user/image', 'POST', add_person_image, apply=[pass_data, jwt_auth_required])
        core.route('/api/user/image/<pk>', 'DELETE', remove_person_image,
                   apply=[pass_data, db_handler, jwt_auth_required])
        core.route('/api/user/forget-password', 'POST', forget_pass, apply=[pass_data, db_handler])
        core.route('/api/user/reset-password', 'PATCH', reset_pass, apply=[pass_data, db_handler])
        core.route('/api/user/change-password', 'PATCH', change_password,
                   apply=[pass_data, db_handler, jwt_auth_required])
        core.route('/api/rules', 'GET', get_rules, apply=[db_handler, jwt_auth_required])
        core.route('/api/roles', 'GET', get_roles, apply=[jwt_auth_required, ])
        core.route('/api/user/role/<pk>', 'PATCH', set_user_role, apply=[pass_data, db_handler, jwt_auth_required, ])
