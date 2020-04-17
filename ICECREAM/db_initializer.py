from bottle import request
from .util import Singleton
from settings import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util.compat import contextmanager
from sqlalchemy.ext.declarative import declarative_base

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


class ResourceMixin(object):

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def __hash__(self):
        return hash(self.id)


def get_database_uri():
    uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(database['db_user'], database['db_pass'],
                                                        database['db_host'], database['db_port'],
                                                        database['db_name'])
    return uri


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
