import os
import os.path

import csv
import us

from dateutil.parser import parse as date_parse

from .exc import CSVNotFoundError

from .num import *


def parse_suspension(val):
    val = val.lower()
    if not val:
        return SUSPENSION_ACTIVE
    elif "pending" in val:
        return SUSPENSION_PENDING
    elif "suspended" in val:
        return SUSPENSION_SUSPENDED


def parse_required_int(val):
    return min(int(val), 2147483647)


def parse_optional_int(val):
    return min(int(val), 2147483647) if val.strip() else None


def parse_category(val):
    try:
        return int(val)
    except ValueError:
        if val == "PR":
            return 0
        else:
            return -1


def parse_name(val):
    return val.lower().title()


def parse_zip(val):
    try:
        return min(int(val), 99999)
    except ValueError:
        return -1

GENDERS = ("M", "F")

def parse_gender(val):
    val = val.upper()
    if val in GENDERS:
        return val
    else:
        return "U"

STATE_LIST = list(map(lambda s: s.abbr, us.states.STATES))

def parse_state(val):
    val = val.upper()
    if val in STATE_LIST:
        return val


CITIZENS = ('P', 'Y', 'N', 'U', 'A')
def parse_citizen(val):
    if val in CITIZENS:
        return val
    else:
        return "U"

def parse_date(val):
    return date_parse(val).date()


def parse_ncca_division(val):
    try:
        return int(val[1:])
    except ValueError:
        return None

RIDER_TRANSFORMS = (
    parse_suspension,                           # Suspension Status
    parse_required_int,                         # License Number
    parse_name,                                 # First Name
    parse_name,                                 # Last Name
    parse_name,                                 # City
    parse_state,                                # State
    parse_zip,                                  # Zip Code
    parse_gender,                               # Gender
    parse_required_int,                         # Racing Age
    parse_date,                                 # License Expiration Date
    str, str,                                   # Road Club/Team
    str, str,                                   # Track Club/Team
    str, str,                                   # MTN Club/Team
    str, str,                                   # CX Club/Team
    str,                                        # Intl Team
    str,                                        # Collegiate Club
    parse_category,                             # Road Category
    parse_category,                             # Track Category
    parse_category,                             # XC Category
    parse_category,                             # DH Category
    parse_category,                             # OT Category
    parse_category,                             # MX Category
    parse_category,                             # CX Category
    parse_date,                                 # Birthday
    parse_citizen,                              # Citizenship
    parse_optional_int, parse_optional_int,     # RD Club/Team ID
    parse_optional_int, parse_optional_int,     # Track Club/Team ID
    parse_optional_int, parse_optional_int,     # MTN Club/Team ID
    parse_optional_int, parse_optional_int,     # CX Club/Team ID
    parse_optional_int,                         # Collegiate Club ID
    str,                                        # UCI Code
    float,                                        # CX Rank
    str, str,                                   # HS Club/Team Name
    parse_optional_int, parse_optional_int,     # HS Club/Team ID
)

CLUB_TEAM_TRANSFORMS = (
    parse_required_int,
    str,
    parse_optional_int,
    str,
    parse_name,
    parse_name,
    parse_name,
    parse_name,
    parse_state,
    parse_zip,
    str,
    parse_ncca_division,
    str,
)

# Suspension,license#,last name,first name,city,state,zip,gender,racing age,exp date,Rdclub,Rdteam,Trackclub,Trackteam,MTNclub,MTNteam,CXclub,CXteam,IntlTeam,Collclub,Road Cat,Track Cat, XC Cat, DH Cat, OT Cat, MX Cat, Cross Cat,birthdate,citizen,RD Club id,RD Team id,Track Clubid,Track Teamid,MTN Clubid,MTN Teamid,CX Clubid,CX Team id,Coll Clubid,UCI Code,CX Rank,HS Club,HS Team,HS Club id,HS Team id

def process_row(transforms, row):
    for i in range(len(transforms)):
        if transforms[i] != str:
            row[i] = transforms[i](row[i])
    return row

def load_csv(path, transforms):
    if not os.path.exists(path):
        raise CSVNotFoundError("Could not find CSV file '%s'" % path)
    output = []
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            output.append(process_row(transforms, row))
    return output