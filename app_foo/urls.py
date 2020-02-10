from app_foo.controller import get_categories, add_category, add_comment
from manager.baseapp import BaseApp
from manager.wrappers import pass_data, db_handler


class CategoryApp(BaseApp):
    def call_router(self, core):
        # wrappers = [check_auth, inject_db, jsonify, timeit]
        core.route('/getall', 'GET', get_categories, apply=[db_handler])
        core.route('/category', 'POST', add_category, apply=[pass_data, db_handler])
        core.route('/comment', 'POST', add_comment, apply=[pass_data, db_handler])
