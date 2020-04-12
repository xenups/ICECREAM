"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data, jsonify
from app_tutorial.controller import get_students, new_student, new_class, get_peoples


class ClassApp(BaseApp):
    def call_router(self, core):
        core.route('/getstudents', 'GET', get_students, apply=[db_handler, jsonify])
        core.route('/addstudent', 'POST', new_student, apply=[pass_data, db_handler, jsonify])
        core.route('/addclass', 'POST', new_class, apply=[pass_data, db_handler, jsonify])
        core.route('/getpeoples', 'GET', get_peoples, apply=[db_handler, jsonify])
