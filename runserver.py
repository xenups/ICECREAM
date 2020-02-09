from bottle import Bottle, run
from app_foo.urls import call_router as category_route
from app_book.urls import call_router as book_route
import sys
from manager.core import execute_from_command_line

if __name__ == '__main__':
    app = Bottle()
    address = execute_from_command_line(sys.argv)
    book_route(app)
    category_route(app)
    run(app, host=address['host'], port=address['port'])
