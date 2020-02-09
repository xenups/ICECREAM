from datetime import datetime
from sqlalchemy import Column, Sequence, Integer, String, DateTime, func, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from manager.db_initializer import Base


#
connection_string = "postgresql://xenups:Qweasd1368@localhost/test"
engine = create_engine(connection_string)
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session()


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    first = Column(String(80))
    last = Column(String(80))

    def __init__(self, first, last):
        self.first = first
        self.last = last


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id))
    author = relationship("Author",
                          backref=backref("quotes", lazy="dynamic"))
    posted_at = Column(DateTime)

    def __init__(self, content, author):
        self.author = author
        self.content = content
        self.posted_at = datetime.utcnow()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
