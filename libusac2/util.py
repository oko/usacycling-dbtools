
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


def convert_int_blank_if_invalid(s):
    """
    Convert a CSV string to an integer, returning None if invalid
    :param s: the string to convert
    :return: an integer conversion or a blank string if invalid
    """
    s = s.lower()
    try:
        return int(s)
    except ValueError:
        return ''


def convert_int_str_if_invalid(s):
    """
    Convert a CSV string to an integer, returning None if invalid
    :param s: the string to convert
    :return: an integer conversion or the original string if invalid
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
        return 'n'
    s = s[0]
    if s == 'y' or s == 'u' or s == 'p':
        return s
    else:
        return 'n'


# Phone number conversion
def convert_phone(s):
    if type(s) == int:
        return s
    else:
        return s.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('.', '')[:10]


# Zip code conversion
def convert_zip(s):
    if type(s) == int:
        return s
    else:
        return convert_int_neg_if_invalid(s[:5] if len(s) > 5 else s) if s != '' else None


# NCCA division conversion
def convert_ncca_division(s):
    if type(s) == int:
        return s
    if s.lower() == 'd1':
        return 1
    else:
        return 2

# State conversion
convert_state = lambda s: str(s).strip()[:2].upper()


# Pro Category conversion
def convert_pro(s):
    if type(s) == int:
        return s
    else:
        return convert_int_neg_if_invalid(s)

from datetime import datetime, date


def convert_date(s):
    if type(s) == datetime:
        return s.date()
    if type(s) == date:
        return s
    else:
        return parser.parse(s)


def convert_gender(s):
    if len(s) > 0:
        if s.lower()[0] == 'f':
            return 'f'
        else:
            return 'm'
    else:
        return 'm'

from collections import OrderedDict
from dateutil import parser

RIDER_HEADERS = OrderedDict([('suspension', lambda x: True if x != '' else False),
                             ('license_number', convert_int_blank_if_invalid),
                             ('last_name', str),
                             ('first_name', str),
                             ('city', str),
                             ('state', str),
                             ('gender', convert_gender),
                             ('racing_age', convert_int_blank_if_invalid),
                             ('exp_date', convert_date),
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
                             ('cx_cat', convert_pro),
                             ('birth_date', convert_date),
                             ('citizen', convert_citizenship),
                             ('road_club_id', convert_int_blank_if_invalid),
                             ('road_team_id', convert_int_blank_if_invalid),
                             ('track_club_id', convert_int_blank_if_invalid),
                             ('track_team_id', convert_int_blank_if_invalid),
                             ('cx_club_id', convert_int_blank_if_invalid),
                             ('cx_team_id', convert_int_blank_if_invalid)])

CLUB_HEADERS = OrderedDict([('club_id', convert_int_blank_if_invalid),
                            ('club_name', str),
                            ('team_id', convert_int_blank_if_invalid),
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