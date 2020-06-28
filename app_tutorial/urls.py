"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data
from app_tutorial.controller import get_students, new_student, new_class, get_peoples


class ClassApp(BaseApp):
    def call_router(self, core):
        core.route('/getstudents', 'GET', get_students)
        core.route('/addstudent', 'POST', new_student, apply=[pass_data])
        core.route('/addclass', 'POST', new_class, apply=[pass_data])
        core.route('/getpeoples', 'GET', get_peoples)
