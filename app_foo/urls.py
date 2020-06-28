"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import  pass_data
from app_foo.controller import get_rooms, new_room, add_room_image, hello


class FOOApp(BaseApp):
    def call_router(self, core):
        core.route('/getrooms', 'GET', get_rooms)
        core.route('/addroom', 'POST', new_room, apply=[pass_data])
        core.route('/addroomimage', 'POST', add_room_image, apply=[pass_data])
        core.route('/hello', 'GET', callback=hello, apply=[])
