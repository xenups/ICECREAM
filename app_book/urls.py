from app_book.controller import get_authors, new_quote, get_author, get_quotes, get_quote, delete_quote
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data, db_handler


class BookApp(BaseApp):
    def call_router(self, core):
        core.route('/getallbooks', 'GET', get_authors, apply=[db_handler])
        core.route('/addquote', 'POST', new_quote, apply=[pass_data, db_handler])
        core.route('/getauthor/<pk>', 'GET', get_author, apply=[db_handler])
        core.route('/getquotes', 'GET', get_quotes, apply=[db_handler])
        core.route('/getquote/<pk>', 'GET', get_quote, apply=[db_handler])
        core.route('/deletequote/<pk>', 'GET', delete_quote, apply=[db_handler])
