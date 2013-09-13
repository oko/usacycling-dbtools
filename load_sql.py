from libusac2.csv import parse_csv
from libusac2.sql import RIDER_HEADERS, CLUB_HEADERS
from redis import Redis

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if len(sys.argv) < 3:
    print("Usage: loader_redis.py <club-csv> <rider-csv> <db-uri>")
    exit(1)

club_file = sys.argv[1]
rider_file = sys.argv[2]
database = sys.argv[3]

engine = create_engine(database)
session = sessionmaker(bind=engine)()

from libusac2.sql import ModelBase
ModelBase.metadata.create_all(bind=engine)

#rds.delete(*rds.keys('rider*'))
#rds.delete(*rds.keys('club*'))
#rds.delete(*rds.keys('team*'))

from datetime import datetime

print("Initializing load at %s" % datetime.now())

clubs = parse_csv(club_file, CLUB_HEADERS)
print(">> Clubs CSV parsed.")
riders = parse_csv(rider_file, RIDER_HEADERS)
print(">> Rider CSV parsed.")

from libusac2.sql import Club, Team, Rider

valid_club_ids = set()
valid_team_ids = set()

for c in clubs:
    if session.query(Club).get(int(c['club_id'])) is None:
        cl = Club(**c)
        session.add(cl)
        session.commit()
        valid_club_ids.add(cl.club_id)
    if c['team_id'] >= 0:
        t = Team(**c)
        session.add(t)
        session.commit()
        valid_team_ids.add(t.team_id)

print(">> Clubs loaded.")

def get_if_not_none(val, cls):
    if val is None:
        return None
    else:
        return cls.query.get(val)
rdrs = []
for r in riders:
    try:
        rdr = Rider(**r)
        if rdr.road_club_id not in valid_club_ids:
            rdr.road_club_id = None
        if rdr.track_club_id not in valid_club_ids:
            rdr.track_club_id = None
        if rdr.cx_club_id not in valid_club_ids:
            rdr.cx_club_id = None
        if rdr.road_team_id not in valid_team_ids:
            rdr.road_team_id = None
        if rdr.track_team_id not in valid_team_ids:
            rdr.track_team_id = None
        if rdr.cx_team_id not in valid_team_ids:
            rdr.cx_team_id = None
        rdrs.append(rdr)
    except ValueError as e:
        print(">> Error processing %d: '%s'" % (r['license_number'], e.message))


session.add_all(rdrs)
session.commit()
print(">> Riders loaded.")

rider_ct = session.query(Rider).all().count()
team_ct = session.query(Team).all().count()
club_ct = session.query(Club).all().count()

print((">> Loaded %d clubs, %d teams, and %d members from CSV." % (club_ct, team_ct, rider_ct)))

print("Finished load at %s" % datetime.now())
