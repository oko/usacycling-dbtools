from libusac3.util import load_csv, RIDER_TRANSFORMS
from redis import Redis

rds = Redis()

data = load_csv("wp_p_universal.csv", RIDER_TRANSFORMS)
for d in data:
    rds.hmset("rider:%d"%d[1], {
    "suspension": d[0],     # Suspension Status
    "license": d[1],        # License Number
    "first_name": d[2],     # First Name
    "last_name": d[3],      # Last Name
    "city": d[4],           # City
    "state": d[5],          # State
    "zipcode": d[6],        # Zip Code
    "gender": d[7],         # Gender
    "racing_age": d[8],     # Racing Age
    "expire_date": d[9],    # License Expiration Date
    "intl_team": d[20],     # Intl Team
    "coll_club": d[21],     # Collegiate Club
    "road_cat": d[22],      # Road Category
    "track_cat": d[23],     # Track Category
    "xc_cat": d[24],        # XC Category
    "dh_cat": d[25],        # DH Category
    "ot_cat": d[26],        # OT Category
    "mx_cat": d[27],        # MX Category
    "cx_cat": d[28],        # CX Category
    "birth_date": d[29],    # Birthday
    "citizenship": d[30],   # Citizenship
    "road_club_id": d[31],
    "road_team_id": d[32],  # RD Club/Team ID
    "track_club_id": d[33],
    "track_team_id": d[34], # Track Club/Team ID
    "mtn_club_id": d[35],
    "mtn_team_id": d[36],   # MTN Club/Team ID
    "cx_club_id": d[37],
    "cx_team_id": d[38],    # CX Club/Team ID
    "coll_club_id": d[39],  # Collegiate Club ID
    "uci_code": d[40],      # UCI Code
    "cx_rank": d[41],       # CX Rank
    "hs_club_id": d[42],
    "hs_team_id": d[43],    # HS Club/Team ID
    })