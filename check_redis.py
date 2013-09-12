from redis import Redis
from pprint import pprint
from datetime import datetime

rds = Redis()

rider_ct = len(rds.keys("rider*"))
team_ct = len(rds.keys("team*"))
club_ct = len(rds.keys("club*"))

print(">> Database contains %d clubs, %d teams, and %d members." % (club_ct, team_ct, rider_ct))

print("Initializing checks at %s" % datetime.now())
riders = rds.keys("rider*")

for r in riders:
    rdr = rds.hgetall(r)
    int(rdr['road_cat'])
    int(rdr['track_cat'])
    try:
        assert rdr['first_name']
        assert rdr['last_name']
    except AssertionError:
        print(">> Rider failed name check: %d" % int(rdr['license_number']))
        rds.delete(r)

print("Finished checks at %s" % datetime.now())