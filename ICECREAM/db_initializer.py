import logging
from bottle import request
from mongosql import MongoSqlBase
from sqlalchemy import orm
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils import database_exists, create_database

from settings import database
from sqla_wrapper import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger()
Base = declarative_base(cls=(MongoSqlBase,))
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


def get_db_session():
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
        orm.configure_mappers()
        request.db_session = db.session
        return request.db_session
