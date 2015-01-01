import os
import os.path

import csv
import us

import dateutil.parser

from .exc import CSVNotFoundError

from .num import *


def parse_noop(val):
    """
    A no-op function for fields that can be skipped.

    :param val: input string (ignored)
    """
    pass


def parse_suspension(val):
    """
    Parse suspension status data. Valid statuses are active, pending, or suspended.

    :param val: input string
    :return: an ``INT`` corresponding to a suspension status in ``libusac3.num``
    """
    val = val.lower()
    if not val:
        return SUSPENSION_ACTIVE
    elif "pending" in val:
        return SUSPENSION_PENDING
    elif "suspended" in val:
        return SUSPENSION_SUSPENDED


def parse_required_int(val):
    """
    Parse an integer that must have a value.

    Truncates to 2147483647 (maximum signed integer value).

    :param val: input string
    :return: an ``int``
    """
    return min(int(val), 2147483647)


def parse_optional_int(val):
    """
    Parse an integer that may not have a value. Return ``None`` if there is
    nothing in the input.

    Truncates to 2147483647 (maximum signed integer value).

    :param val: input string
    :return: an ``int`` or ``None``
    """
    return min(int(val), 2147483647) if val is not None and val != 'None' and val.strip() else None


def parse_category(val):
    """
    Parse race category. Pro riders will be given category 0.

    :param val: input string
    :return:
    """
    try:
        return int(val)
    except ValueError:
        if val == "PR":
            return 0
        else:
            return -1


def parse_name(val):
    """
    Parse a name field. Normalizes names with capitalized first letters of words.

    :param val: input string
    :return: a normalized name (capitalized first letters)
    """
    return val.lower().title()


def parse_zip(val):
    """
    Parse a zipcode (truncate value at 99999)

    :param val: input string
    :return: an ``int`` containing the zipcode value, ``-1`` if zipcode is invalid
    """
    try:
        return min(int(val), 99999)
    except ValueError:
        return -1


GENDERS = ("M", "F")


def parse_gender(val):
    """
    Parse gender data

    :param val: input string
    :return: a single character indicating M/F gender or "U" if other.
    """
    val = val.upper()
    if val in GENDERS:
        return val
    else:
        return "U"


STATE_LIST = list(map(lambda s: s.abbr, us.states.STATES))


def parse_state(val):
    """
    Parse state data, checking against `us.states.STATES`

    :param val: input string
    :return: the all-caps state abbreviation if the state is valid, otherwise ``None``
    """
    val = val.upper()
    if val in STATE_LIST:
        return val


CITIZENS = ('P', 'Y', 'N', 'U', 'A')


def parse_citizen(val):
    """
    Parse citizenship data.

    :param val: input data
    :return: a single-character string containing the citizenship status
    """
    if val in CITIZENS:
        return val
    else:
        return "U"


def parse_date(val):
    """
    Parse a date.

    :param val: input string
    :return: a ``datetime.date()`` value representing the date
    """
    return dateutil.parser.parse(val).date()


def parse_ncca_division(val):
    """
    Parse NCCA division data.

    :param val: input string
    :return: an ``int`` value representing the NCCA division number.
    """
    try:
        return int(val[1:])
    except ValueError:
        return None


RIDER_TRANSFORMS = (
    ("suspension", parse_suspension),  # Suspension Status
    ("license", parse_required_int),  # License Number
    ("last_name", parse_name),  # First Name
    ("first_name", parse_name),  # Last Name
    ("city", parse_name),  # City
    ("state", parse_state),  # State
    ("zipcode", parse_zip),  # Zip Code
    ("gender", parse_gender),  # Gender
    ("racing_age", parse_required_int),  # Racing Age
    ("expire_date", parse_date),  # License Expiration Date
    (None, parse_noop), (None, parse_noop),  # Road Club/Team
    (None, parse_noop), (None, parse_noop),  # Track Club/Team
    (None, parse_noop), (None, parse_noop),  # MTN Club/Team
    (None, parse_noop), (None, parse_noop),  # CX Club/Team
    ("intl_team", str),  # Intl Team
    (None, parse_noop),  # Collegiate Club
    ("road_cat", parse_category),  # Road Category
    ("track_cat", parse_category),  # Track Category
    ("xc_cat", parse_category),  # XC Category
    ("dh_cat", parse_category),  # DH Category
    ("ot_cat", parse_category),  # OT Category
    ("mx_cat", parse_category),  # MX Category
    ("cx_cat", parse_category),  # CX Category
    ("birth_date", parse_date),  # Birthday
    ("citizenship", parse_citizen),  # Citizenship
    ("road_club_id", parse_optional_int), ("road_team_id", parse_optional_int),  # RD Club/Team ID
    ("track_club_id", parse_optional_int), ("track_team_id", parse_optional_int),  # Track Club/Team ID
    ("mtn_club_id", parse_optional_int), ("mtn_team_id", parse_optional_int),  # MTN Club/Team ID
    ("cx_club_id", parse_optional_int), ("cx_team_id", parse_optional_int),  # CX Club/Team ID
    ("coll_club_id", parse_optional_int),  # Collegiate Club ID
    ("uci_code", str),  # UCI Code
    ("cx_rank", float),  # CX Rank
    (None, parse_noop), (None, parse_noop),  # HS Club/Team Name
    ("hs_club_id", parse_optional_int), ("hs_team_id", parse_optional_int),  # HS Club/Team ID
)

CLUB_TEAM_TRANSFORMS = (
    ("club_id", parse_required_int),
    ("club_name", str),
    ("team_id", parse_optional_int),
    ("team_name", str),
    ("contact_name", parse_name),
    ("address_1", parse_name),
    ("address_2", parse_name),
    ("city", parse_name),
    ("state", parse_state),
    ("zipcode", parse_zip),
    ("phone_number", str),
    ("division", parse_ncca_division),
    ("ncca_conf", str),
)


from collections import OrderedDict


def process_row(transforms, row):
    """
    Apply parser transformations to a single row.

    :param transforms: an iterable of functions to be applied to the fields of the row
    :param row: a list of fields representing a row
    :return: a mutated list containing transformed values
    """
    row_dict = {}
    for i in range(len(transforms)):
        if transforms[i][0] is not None:
            row_dict[transforms[i][0]] = transforms[i][1](row[i])
    return row_dict


def load_csv(path, transforms):
    """
    Load a CSV file and apply parser transformations to all rows.

    :param path: path to a CSV file
    :param transforms: an iterable of functions to be applied to the fields of each row during loading
    :return: a ``list`` of transformed rows :raise CSVNotFoundError: if the file is not found
    """
    if not os.path.exists(path):
        raise CSVNotFoundError("Could not find CSV file '%s'" % path)
    output = []

    # Use ``utf-8`` when possible.
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        first = True
        for row in reader:
            # Skip header fields
            if first:
                first = False
                continue
            output.append(process_row(transforms, row))
    return output