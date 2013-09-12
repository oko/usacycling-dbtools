"""
Alternative mappings for use with relational databases.
Foreign key-ish values (club/team IDs) are converted to
``None`` for use in foreign key relations.
"""

from .util import (
    convert_int_neg_if_invalid,
    convert_int_none_if_invalid,
    convert_citizenship,
    convert_ncca_division,
    convert_phone,
    convert_pro,
    convert_state,
    convert_zip,
    Gender,
)
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
                             ('road_club_id', convert_int_none_if_invalid),
                             ('road_team_id', convert_int_none_if_invalid),
                             ('track_club_id', convert_int_none_if_invalid),
                             ('track_team_id', convert_int_none_if_invalid),
                             ('cx_club_id', convert_int_none_if_invalid),
                             ('cx_team_id', convert_int_none_if_invalid)])

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