from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data
from app_book.controller import get_authors, new_quote, get_author, get_quotes, get_quote, delete_quote


class BookApp(BaseApp):
    def call_router(self, core):
        core.route('/getauthors', 'GET', get_authors, )
        core.route('/addquote', 'POST', new_quote, apply=[pass_data])
        core.route('/getauthor/<pk>', 'GET', get_author)
        core.route('/getquotes', 'GET', get_quotes)
        core.route('/getquote/<pk>', 'GET', get_quote)
        core.route('/deletequote/<pk>', 'GET', delete_quote)
