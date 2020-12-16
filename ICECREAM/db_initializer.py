import logging
from sqlalchemy import orm
from bottle import request
from settings import database
from mongosql import MongoSqlBase
from sqlalchemy.orm import Session
from sqla_wrapper import SQLAlchemy
from abc import ABCMeta, abstractmethod
from sqlalchemy_searchable import make_searchable
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger()
Base = declarative_base(cls=(MongoSqlBase,))
metadata = Base.metadata


class ConnectionFactory(object):
    __metaclass__ = ABCMeta

    def connect(self):
        return SQLAlchemy(self.get_database_uri(), pool_pre_ping=True)

    @abstractmethod
    def get_database_uri(self):
        raise NotImplementedError()


class PostgresConnectionFactory(ConnectionFactory):
    def __init__(self, database_conf: {}, meta_data=None):
        self.user = database_conf['db_user']
        self.password = database_conf['db_pass']
        self.host = database_conf['db_host']
        self.database = database_conf['db_name']
        self.port = database_conf['db_port']
        make_searchable(meta_data)

    def get_database_uri(self):
        uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.user, self.password,
                                                            self.host, self.port,
                                                            self.database)
        return uri


class Sqlite3ConnectionFactory(ConnectionFactory):
    def __init__(self, db_name="db"):
        self.__db = db_name

    def get_database_uri(self):
        return "sqlite:///{}.sqlite3".format(self.__db)


def create_db_connection(database_conf, meta_data, type_db="sqlite"):
    if type_db == "sqlite":
        return Sqlite3ConnectionFactory().connect()
    elif type_db == "postgres":
        return PostgresConnectionFactory(database_conf, meta_data).connect()
    else:
        raise Exception(f"Not implemented {type_db}")


db = create_db_connection(database, metadata, type_db=database["db_type"])
db.session_options = {'autocommit': True}
metadata.create_all(db.engine)
orm.configure_mappers()


def get_db_session() -> Session:
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
        request.db_session = db.session
        return request.db_session
