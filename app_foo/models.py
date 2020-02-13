"ICECREAM"
from sqlalchemy import Column, Integer, String

from ICECREAM.db_initializer import Base


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
