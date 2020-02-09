from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import request
from sqlalchemy.util.compat import contextmanager

connection_string = "postgresql://xenups:Qweasd1368@localhost/test"
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
db_session = Session()
Session.configure(bind=engine)

Base = declarative_base()


def get_db_session():
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
        request.db_session = Session()
        return request.db_session


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
