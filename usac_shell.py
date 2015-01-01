from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://localhost:5432/usac")
Session = sessionmaker(bind=engine)
session = Session()

from libusac3.sql import Base, Rider, Club, Team

Base.metadata.create_all(bind=engine)


def get_rider(license_num):
    return session.query(Rider).get(license_num)


def get_club(club_id):
    return session.query(Club).get(club_id)


def get_team(team_id):
    return session.query(Team).get(team_id)


import bpython
bpython.embed(locals_=locals())