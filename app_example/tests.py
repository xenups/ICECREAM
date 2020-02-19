#!/usr/bin/env python3
import unittest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .models import Movie, Actor, ContactDetails, Stuntman

uri = 'postgres+psycopg2://{}:{}@{}:{}/{}'.format('xenups', '',
                                                  'localhost', '5432',
                                                  'test')


class TestAppExample(unittest.TestCase):
    def test_connecting_to_db(self):
        try:
            engine = create_engine(uri)
            Session = sessionmaker(bind=engine)
            session = Session()
            Base = declarative_base()
            print('its connected')
        except Exception as e:
            print(e)

    def test_create_movie(self):

        engine = create_engine(uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base = declarative_base()
        bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
        furious_7 = Movie("Furious 7", date(2015, 4, 2))
        pain_and_gain = Movie("Pain & Gain", date(2013, 8, 23))
        # # 5 - creates actors
        matt_damon = Actor("Matt Damon", date(1970, 10, 8))
        amir_lesani = Actor("Amir Lesani", date(1970, 10, 8))
        dwayne_johnson = Actor("Dwayne Johnson", date(1972, 5, 2))
        mark_wahlberg = Actor("Mark Wahlberg", date(1971, 6, 5))
        # 6 - add actors to movies
        bourne_identity.actors = [matt_damon]
        furious_7.actors = [dwayne_johnson, amir_lesani]
        pain_and_gain.actors = [dwayne_johnson, mark_wahlberg]
        # 7 - add contact details to actors
        matt_contact = ContactDetails("415 555 2671", "Burbank, CA", matt_damon)
        dwayne_contact = ContactDetails("423 555 5623", "Glendale, CA", dwayne_johnson)
        dwayne_contact_2 = ContactDetails("421 444 2323", "West Hollywood, CA", dwayne_johnson)
        mark_contact = ContactDetails("421 333 9428", "Glendale, CA", mark_wahlberg)

        # 8 - create stuntmen
        matt_stuntman = Stuntman("John Doe", True, matt_damon)
        dwayne_stuntman = Stuntman("John Roe", True, dwayne_johnson)
        mark_stuntman = Stuntman("Richard Roe", True, mark_wahlberg)

        # 9 - persists data
        session.add(bourne_identity)
        session.add(furious_7)
        session.add(pain_and_gain)

        session.add(matt_contact)
        session.add(dwayne_contact)
        session.add(dwayne_contact_2)
        session.add(mark_contact)

        session.add(matt_stuntman)
        session.add(dwayne_stuntman)
        session.add(mark_stuntman)

        # 10 - commit and close session
        session.commit()
        session.close()


# 5 - creates actors

if __name__ == '__main__':
    unittest.main()
