"ICECREAM"
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric, Table
from sqlalchemy.orm import relationship

from ICECREAM.db_initializer import Base


#########   simple table tutorial    #############
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column('title', String(32))
    in_stock = Column('in_stuck', Boolean)
    quantity = Column('quantity', Integer)
    price = Column('price', Numeric)


######## one to many ############
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Comments(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey(Article.id))


######## one to many ############

#########   many to one    #############
class Tire(Base):
    __tablename__ = 'tire'
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    car = relationship("Car")


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)


#########   many to one    #############

######### one to one ###############
class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    mobile_phone = relationship("MobilePhone", uselist=False, back_populates="people")


class MobilePhone(Base):
    __tablename__ = 'mobile_phones'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    people = relationship("People", back_populates="mobile_phone")


######### one to one ###############

#########  many to many ############

students_classes_association = Table('students_classes', Base.metadata,
                                     Column('student_id', Integer, ForeignKey('students.id')),
                                     Column('class_id', Integer, ForeignKey('classes.id'))
                                     )


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    classes = relationship("Class", secondary=students_classes_association)


class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)

#########  many to many ############
