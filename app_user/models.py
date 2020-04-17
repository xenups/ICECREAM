"ICECREAM"
from sqlalchemy.orm import relationship
from ICECREAM.db_initializer import Base, ResourceMixin
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from werkzeug.security import generate_password_hash, check_password_hash


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    last_name = Column(String)
    bio = Column(String)


class User(ResourceMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    roles = Column(String, nullable=False, default="")
    person_id = Column(Integer, ForeignKey('persons.id'))

    person = relationship(Person, primaryjoin=person_id == Person.id, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_roles(self):
        return self.roles.split(",")

    def set_roles(self, roles):
        self.roles = ",".join(roles)


class Message(ResourceMixin, Base):
    """Message Model"""
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    owner_id = Column(ForeignKey(User.id), nullable=False)
    owner = relationship(User, uselist=False, lazy="joined")
