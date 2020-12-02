from datetime import datetime
from ICECREAM.db_initializer import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


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
