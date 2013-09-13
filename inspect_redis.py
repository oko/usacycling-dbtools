from redis import Redis
from libusac2.util import RIDER_HEADERS, CLUB_HEADERS

rds = Redis()

rider_ct = len(rds.keys("rider*"))
team_ct = len(rds.keys("team:*")) - len(rds.keys("team:*:riders")) - len(rds.keys("team:*:riders:*"))
club_ct = len(rds.keys("club:*")) - len(rds.keys("club:*:riders")) - len(rds.keys("club:*:riders:*"))

print((">> Inspecting %d clubs, %d teams, and %d members" % (club_ct, team_ct, rider_ct)))


def r(lic):
    lic = int(lic)
    raw = rds.hgetall('rider:%d' % lic)
    for h, f in RIDER_HEADERS.iteritems():
        raw[h] = f(raw[h])
    return raw

print(r(347128))