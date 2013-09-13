from libusac2.csv import parse_csv
from libusac2.sql import RIDER_HEADERS, CLUB_HEADERS
from redis import Redis

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


if len(sys.argv) < 2:
    print("Usage: inspect_pgsql.py <db-uri>")
    exit(1)

database = sys.argv[1]

engine = create_engine(database)
session = sessionmaker(bind=engine)()

from libusac2.sql import ModelBase, Club, Team, Rider
ModelBase.metadata.create_all(bind=engine)

rider_ct = session.query(Rider).count()
team_ct = session.query(Team).count()
club_ct = session.query(Club).count()

print((">> Inspecting %d clubs, %d teams, and %d members" % (club_ct, team_ct, rider_ct)))

def r(lic):
    return session.query(Rider).get(lic)

def c(lic):
    return session.query(Club).get(lic)

def t(lic):
    return session.query(Team).get(lic)