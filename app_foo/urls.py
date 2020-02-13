"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import db_handler, pass_data
from app_foo.controller import get_rooms, new_room


class FOOApp(BaseApp):
    def call_router(self, core):
        core.route('/getrooms', 'GET', get_rooms, apply=[db_handler])
        core.route('/addroom', 'POST', new_room, apply=[pass_data, db_handler])
