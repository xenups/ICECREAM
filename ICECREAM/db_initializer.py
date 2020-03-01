from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import request
from sqlalchemy.util.compat import contextmanager

from settings import database

from .util import Singleton

Base = declarative_base()


class BaseDBConnector:
    def __init__(self):
        try:
            self.engine = create_engine(get_database_uri())
            self.Session = sessionmaker(bind=self.engine)
            self.db_session = self.Session()
            self.Session.configure(bind=self.engine)
        except Exception as error:
            print(error)


class DBConnector(BaseDBConnector, metaclass=Singleton):
    pass


def get_database_uri():
    uri = 'postgres+psycopg2://{}:{}@{}:{}/{}'.format(database['db_user'], database['db_pass'],
                                                      database['db_host'], database['db_port'],
                                                      database['db_name'])
    return uri


def get_db_session():
    if hasattr(request, 'db_session'):
        print('it has session')
        return request.db_session
    else:
        print('session created again')
        db = DBConnector()
        request.db_session = db.db_session
        return request.db_session


def recreate_database():
    db = DBConnector()
    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)


@contextmanager
def session_scope():
    db = DBConnector()
    session = db.db_session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
