"ICECREAM"
import datetime

from sqlalchemy.orm import relationship
from ICECREAM.db_initializer import Base, ResourceMixin
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    last_name = Column(String)
    email = Column(String)
    person_images = relationship("PersonImage", back_populates="person")


class PersonImage(Base):
    __tablename__ = 'person_image'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey(Person.id))
    person = relationship(Person)


class User(ResourceMixin, Base):
    __tablename__ = 'users'
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    roles = Column(String, nullable=False, default="")
    person_id = Column(Integer, ForeignKey('persons.id'))

    person = relationship(Person, primaryjoin=person_id == Person.id, lazy=True)
    # movie_raters = relationship(MovieRater, back_populates="user")

    @property
    def get_phone(self):
        return self.phone

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_roles(self):
        return self.roles.split(",")

    def set_roles(self, roles):
        self.roles = ",".join(roles)
