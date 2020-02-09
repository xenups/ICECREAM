from sqlalchemy import Column, Sequence, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from manager.db_initializer import Base


class Categores(Base):
    __tablename__ = 'categoriess'
    id = Column(UUID, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(UUID, primary_key=True)

    comment = Column(String(250), nullable=False)
    creation_date = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    category_id = Column(UUID, ForeignKey(Categores.id), nullable=False)
    category = relationship(Categores, primaryjoin=category_id == Categores.id, lazy=True)
