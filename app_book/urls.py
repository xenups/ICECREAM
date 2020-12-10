from bottle_jwt2 import jwt_auth_required
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data, debug
from app_book.controller import get_authors, new_quote, get_author, get_quotes, get_quote, delete_quote


class BookApp(BaseApp):
    def call_router(self, core):
        core.route('/authors', 'GET', get_authors, apply=[jwt_auth_required, debug])
        core.route('/quotes', 'POST', new_quote, apply=[pass_data])
        core.route('/authors/<pk>', 'GET', get_author)
        core.route('/quotes', 'GET', get_quotes)
        core.route('/quotes/<pk>', 'GET', get_quote)
        core.route('/quotes/<pk>', 'GET', delete_quote)
