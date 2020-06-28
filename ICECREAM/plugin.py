import inspect

import bottle
from sqlalchemy.exc import SQLAlchemyError

from ICECREAM.db_initializer import get_db_session

if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass


    bottle.PluginError = PluginError


class DBInjectorPlugin(object):
    name = 'sqlalchemy'
    api = 2

    def __init__(self, keyword='db_session'):
        self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, DBInjectorPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError(
                    "Found another SQLAlchemy plugin with " "conflicting settings (non-unique keyword).")
            elif other.name == self.name:
                self.name += '_%s' % self.keyword

    def apply(self, callback, route):
        if bottle.__version__.startswith('0.9'):
            _callback = route['callback']
        else:
            _callback = route.callback

        try:
            inspect.signature
            # check if inspect.signature exists
        except AttributeError:
            argspec = inspect.getfullargspec(_callback)
            parameters = argspec.args
            accept_kwargs = argspec.keywords
        else:
            parameters = inspect.signature(_callback).parameters
            accept_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD
                                for p in parameters.values())

        if not (accept_kwargs or self.keyword in parameters):
            return callback

        def wrapper(*args, **kwargs):
            session = get_db_session()
            try:
                session.expire_on_commit = True
                kwargs['db_session'] = session
                rtn = callback(*args, **kwargs)
                kwargs['db_session'].commit()
                return rtn
            except(SQLAlchemyError, bottle.HTTPError, Exception):
                session.rollback()
                raise
            finally:
                session.close()

        return wrapper


Plugin = DBInjectorPlugin
