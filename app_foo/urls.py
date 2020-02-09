from app_foo.controller import get_categories, add_category, add_comment
from manager.wrappers import pass_data, inject_db, jsonify


def call_router(app):
    # wrappers = [check_auth, inject_db, jsonify, timeit]
    app.route('/getall', 'GET', get_categories, apply=[inject_db, jsonify])
    app.route('/category', 'POST', add_category, apply=[pass_data, inject_db])
    app.route('/comment', 'POST', add_comment, apply=[pass_data, inject_db])
