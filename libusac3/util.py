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
    return min(int(val), 2147483647) if val.strip() else None


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
    parse_suspension,  # Suspension Status
    parse_required_int,  # License Number
    parse_name,  # First Name
    parse_name,  # Last Name
    parse_name,  # City
    parse_state,  # State
    parse_zip,  # Zip Code
    parse_gender,  # Gender
    parse_required_int,  # Racing Age
    parse_date,  # License Expiration Date
    parse_noop, parse_noop,  # Road Club/Team
    parse_noop, parse_noop,  # Track Club/Team
    parse_noop, parse_noop,  # MTN Club/Team
    parse_noop, parse_noop,  # CX Club/Team
    str,  # Intl Team
    parse_noop,  # Collegiate Club
    parse_category,  # Road Category
    parse_category,  # Track Category
    parse_category,  # XC Category
    parse_category,  # DH Category
    parse_category,  # OT Category
    parse_category,  # MX Category
    parse_category,  # CX Category
    parse_date,  # Birthday
    parse_citizen,  # Citizenship
    parse_optional_int, parse_optional_int,  # RD Club/Team ID
    parse_optional_int, parse_optional_int,  # Track Club/Team ID
    parse_optional_int, parse_optional_int,  # MTN Club/Team ID
    parse_optional_int, parse_optional_int,  # CX Club/Team ID
    parse_optional_int,  # Collegiate Club ID
    str,  # UCI Code
    float,  # CX Rank
    parse_noop, parse_noop,  # HS Club/Team Name
    parse_optional_int, parse_optional_int,  # HS Club/Team ID
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


def process_row(transforms, row):
    """
    Apply parser transformations to a single row.

    :param transforms: an iterable of functions to be applied to the fields of the row
    :param row: a list of fields representing a row
    :return: a mutated list containing transformed values
    """
    for i in range(len(transforms)):
        if transforms[i] != str:
            row[i] = transforms[i](row[i])
    return row


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