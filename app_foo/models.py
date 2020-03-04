"ICECREAM"
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ICECREAM.db_initializer import Base


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    room_images = relationship("RoomImage", back_populates="room")


class RoomImage(Base):
    __tablename__ = 'room_image'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id))
    room = relationship(Room)
