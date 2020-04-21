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
    email = Column(String)


class User(ResourceMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    roles = Column(String, nullable=False, default="")
    person_id = Column(Integer, ForeignKey('persons.id'))

    person = relationship(Person, primaryjoin=person_id == Person.id, lazy=True)

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
