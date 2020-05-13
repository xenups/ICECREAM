import bottle
from bottle import request
from sqlalchemy.exc import SQLAlchemyError

from ICECREAM.db_initializer import get_db_session
import logging

logger = logging.getLogger()


def pass_data(func):
    def wrapper(*args, **kwargs):
        if request.json is not None:
            kwargs['data'] = request.json
        elif request.forms is not None:
            my_data = {}
            data_list = request.forms.dict
            for key in data_list.keys():
                my_data[key] = data_list[key][0]
            if request.files is not None and request.files.dict is not None:
                my_data['files'] = request.files.dict.get('files')

            kwargs['data'] = my_data

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


def cors(fn):
    def _cors(*args, **kwargs):
        # set CORS headers
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        bottle.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _cors


def db_handler(func):
    def wrapper(*args, **kwargs):
        session = get_db_session()
        try:
            session.expire_on_commit = False
            kwargs['db_session'] = session
            rtn = func(*args, **kwargs)
            return rtn
        except(SQLAlchemyError, bottle.HTTPError):
            session.rollback()
            raise

    return wrapper


def debug(fn):
    def wrapper(*args, **kwargs):
        logger.info("Entering {:s}".format(fn.__name__))
        result = fn(*args, **kwargs)
        logger.info("Finished {:s}".format(fn.__name__))
        return result

    return wrapper
