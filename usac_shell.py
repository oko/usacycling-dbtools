from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import argparse

parser = argparse.ArgumentParser(description='Open the USAC database SQL ORM in a Python shell')
parser.add_argument('uri', type=str, help='an SQL database URI')
args = parser.parse_args()

engine = create_engine(args.uri)
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