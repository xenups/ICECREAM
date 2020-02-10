from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import request
from sqlalchemy.util.compat import contextmanager

from settings import database


def get_database_uri():
    uri = 'postgres+psycopg2://{}:{}@{}:{}/{}'.format(database['db_user'], database['db_pass'],
                                                      database['db_host'], database['db_port'],
                                                      database['db_name'])
    return uri


Base = declarative_base()


# using singleton pattern to create engine once
class DBConnector(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.engine = create_engine(get_database_uri())
        self.Session = sessionmaker(bind=self.engine)
        self.db_session = self.Session()
        self.Session.configure(bind=self.engine)


def get_db_session():
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
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
