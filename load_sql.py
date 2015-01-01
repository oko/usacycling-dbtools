from libusac3.util import load_csv, RIDER_TRANSFORMS, CLUB_TEAM_TRANSFORMS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description='Load the USAC CSV files into an SQL database.')
parser.add_argument('uri', type=str, help='an SQL database URI')
parser.add_argument('riderfile', type=str, help='the USAC universal format rider CSV file (wp_p_universal.csv)')
parser.add_argument('clubsfile', type=str, help='the USAC one-line-per-team format clubs CSV file (wp_all_clubs2.csv)')
args = parser.parse_args()

print("Launching USAC database load @ %s..." % datetime.now())

engine = create_engine(args.uri)
Session = sessionmaker(bind=engine)
session = Session()

from libusac3.sql import Base, Rider, Club, Team

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

club_data = load_csv(args.clubsfile, CLUB_TEAM_TRANSFORMS)

clubs_duped = map(lambda c: Club(**c), club_data)
clubs_id_set = set()
clubs_deduped = []
for c in clubs_duped:
    if c.club_id in clubs_id_set:
        continue
    else:
        clubs_deduped.append(c)
        clubs_id_set.add(c.club_id)

session.add_all(clubs_deduped)
session.commit()
session.add_all(map(lambda t: Team(**t), filter(lambda t: t['team_id'] is not None, club_data)))
session.commit()

# Get all valid club & team IDs
valid_club_ids = tuple(map(lambda x: x.club_id, session.query(Club).all()))
valid_team_ids = tuple(map(lambda x: x.team_id, session.query(Team).all()))

# Define rider data scrub function using
# newly instantiated club/team IDs to check
# for existence
def clean_rider_ids(rider):
    if rider.road_club_id not in valid_club_ids:
        rider.road_club_id = None
    if rider.track_club_id not in valid_club_ids:
        rider.track_club_id = None
    if rider.mtn_club_id not in valid_club_ids:
        rider.mtn_club_id = None
    if rider.cx_club_id not in valid_club_ids:
        rider.cx_club_id = None
    if rider.road_team_id not in valid_team_ids:
        rider.road_team_id = None
    if rider.track_team_id not in valid_team_ids:
        rider.track_team_id = None
    if rider.mtn_team_id not in valid_team_ids:
        rider.mtn_team_id = None
    if rider.cx_team_id not in valid_team_ids:
        rider.cx_team_id = None
    if rider.coll_club_id not in valid_club_ids:
        rider.coll_club_id = None
    return rider

# Load rider data
rider_data = load_csv(args.riderfile, RIDER_TRANSFORMS)

# Loop through, clean up data, convert to mapped object
for i in range(len(rider_data)):
    session.add(clean_rider_ids(Rider(**rider_data[i])))
    # Commit every 1k objects
    if i % 1000 == 0:
        session.commit()
# Commit any remaining objects
session.commit()

print("...completed @ %s" % datetime.now())