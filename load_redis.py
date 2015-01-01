from libusac3.util import load_csv, RIDER_TRANSFORMS, CLUB_TEAM_TRANSFORMS
from redis import Redis

rds = Redis()

data = load_csv("wp_p_universal.csv", RIDER_TRANSFORMS)

for d in data:
    rds.hmset("rider:%d"%d["license"], d)

data = load_csv("wp_all_clubs2.csv", CLUB_TEAM_TRANSFORMS)

for d in data:
    rds.hmset("club:%d"%d["club_id"], d)
    if d["team_id"]:
        rds.hmset("team:%d"%d["team_id"], d)