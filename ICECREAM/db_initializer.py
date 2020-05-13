import logging
from bottle import request
from sqlalchemy import orm, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_searchable import sync_trigger, make_searchable
from sqlalchemy_utils import database_exists, create_database

from settings import database
from sqla_wrapper import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger()
Base = declarative_base()
make_searchable(Base.metadata)


def get_database_uri():
    uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(database['db_user'], database['db_pass'],
                                                        database['db_host'], database['db_port'],
                                                        database['db_name'])
    try:
        if not database_exists(uri):
            create_database(uri)
    except Exception:
        raise
    return uri


db = SQLAlchemy(get_database_uri(), pool_pre_ping=True)
Base.metadata.create_all(db.engine)
orm.configure_mappers()


class ResourceMixin(object):

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def __hash__(self):
        return hash(self.id)


def get_db_session():
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
        orm.configure_mappers()
        request.db_session = db.session
        return request.db_session
