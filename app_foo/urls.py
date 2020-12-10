"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data, debug
from app_foo.controller import get_rooms, new_room, add_room_image, filter_rooms


class FOOApp(BaseApp):
    def call_router(self, core):
        core.route('/rooms', 'GET', get_rooms, apply=[debug])
        core.route('/rooms', 'POST', new_room, apply=[pass_data, debug])
        core.route('/room_image', 'POST', add_room_image, apply=[pass_data, debug])
        core.route('/rooms/filter', 'GET', filter_rooms, apply=[debug])
