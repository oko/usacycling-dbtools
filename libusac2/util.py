
class Gender:
    MALE = 0
    FEMALE = 1


class Citizen:
    NONRESIDENT = 0
    CITIZEN = 1
    UNKNOWN = 2
    PERM_RES = 3

GENDER_STRING_MAP = {Gender.MALE: 'male', Gender.FEMALE: 'female'}


def convert_int_neg_if_invalid(s):
    """
    Convert a CSV string to an integer, returning -1 if invalid
    :param s: the string to convert
    :return: an integer conversion or ``None`` if invalid
    """
    s = s.lower()
    try:
        return int(s)
    except ValueError:
        return -1


def convert_int_none_if_invalid(s):
    """
    Convert a CSV string to an integer, returning None if invalid
    :param s: the string to convert
    :return: an integer conversion or ``None`` if invalid
    """
    s = s.lower()
    try:
        return int(s)
    except ValueError:
        return None

def convert_int_str_if_invalid(s):
    """
    Convert a CSV string to an integer, returning None if invalid
    :param s: the string to convert
    :return: an integer conversion or ``None`` if invalid
    """
    s = s.lower()
    try:
        return int(s)
    except ValueError:
        return str(s)


def convert_citizenship(s):
    """
    Convert a citizenship flag from CSV to the appropriate integer
    :param s: the string to convert
    :return: an integer value enumerated in ``Citizen``
    """
    s = s.lower()
    if len(s) == 0:
        return Citizen.NONRESIDENT
    s = s[0]
    if s == 'y':
        return Citizen.CITIZEN
    elif s == 'u':
        return Citizen.UNKNOWN
    elif s == 'p':
        return Citizen.PERM_RES
    else:
        return Citizen.NONRESIDENT

# Phone number conversion
convert_phone = lambda x: x.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('.', '')[:10]
# Zip code conversion
convert_zip = lambda x: convert_int_neg_if_invalid(x[:5] if len(x) > 5 else x) if x != '' else None
# NCCA division conversion
convert_ncca_division = lambda x: 1 if x.lower() == 'd1' else 2
# State conversion
convert_state = lambda x: str(x).strip()[:2]
# Pro Category conversion
convert_pro = lambda x: 1000 if x.lower() == 'pr' else convert_int_neg_if_invalid(x)


from collections import OrderedDict
from dateutil import parser

RIDER_HEADERS = OrderedDict([('suspension', lambda x: True if x != '' else False),
                             ('license_number', convert_int_neg_if_invalid),
                             ('last_name', str),
                             ('first_name', str),
                             ('city', str),
                             ('state', str),
                             ('gender', lambda x: Gender.FEMALE if x[0] == 'f' else Gender.MALE),
                             ('racing_age', convert_int_neg_if_invalid),
                             ('exp_date', lambda x: parser.parse(x)),
                             ('road_club', str),
                             ('road_team', str),
                             ('track_club', str),
                             ('track_team', str),
                             ('cx_club', str),
                             ('cx_team', str),
                             ('intl_team', str),
                             ('ncca_club', str),
                             ('road_cat', convert_pro),
                             ('track_cat', convert_pro),
                             ('cx_cat', convert_int_neg_if_invalid),
                             ('birth_date', lambda x: parser.parse(x)),
                             ('citizen', convert_citizenship),
                             ('road_club_id', convert_int_neg_if_invalid),
                             ('road_team_id', convert_int_neg_if_invalid),
                             ('track_club_id', convert_int_neg_if_invalid),
                             ('track_team_id', convert_int_neg_if_invalid),
                             ('cx_club_id', convert_int_neg_if_invalid),
                             ('cx_team_id', convert_int_neg_if_invalid)])

CLUB_HEADERS = OrderedDict([('club_id', convert_int_neg_if_invalid),
                            ('club_name', str),
                            ('team_id', convert_int_neg_if_invalid),
                            ('team_name', str),
                            ('contact_name', str),
                            ('address_1', str),
                            ('address_2', str),
                            ('city', str),
                            ('state', convert_state),
                            ('zip', convert_zip),
                            ('ph_num', convert_phone),
                            ('ncca_division', convert_ncca_division),
                            ('ncca_conf', str)])