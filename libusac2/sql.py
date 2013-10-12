"""
Alternative mappings for use with relational databases.
Foreign key-ish values (club/team IDs) are converted to
``None`` for use in foreign key relations.
"""


def unicode_conv(s):
    return str(s).decode('utf-8', 'replace')


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
convert_zip = lambda s: convert_int_neg_if_invalid(s[:5] if len(s) > 5 else s) if s != '' else None
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
convert_pro = lambda s: 1000 if s.lower() == 'pr' else convert_int_blank_if_invalid(s)
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

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from .sql_base import ModelBase

class Club(ModelBase):

    __tablename__ = 'usac_clubs'

    club_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    contact_name = Column(String(255))
    address_1 = Column(String(255))
    address_2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(20))
    zip = Column(Integer)
    phone = Column(Integer)

    def __init__(self, **data):
        self.club_id = data['club_id']
        self.name = data['club_name']
        self.contact_name = data['contact_name']
        self.address_1 = data['address_1']
        self.address_2 = data['address_2']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.ph_num = data['ph_num']
        self.ncca_division = data['ncca_division']
        self.ncca_conf = data['ncca_conf']

    def __repr__(self):
        return "<Club #%d: %s>" % (self.club_id, self.name)


class Team(ModelBase):

    __tablename__ = 'usac_teams'

    team_id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey(Club.__tablename__ + '.club_id'))
    club = relationship("Club")
    name = Column(String(255))
    contact_name = Column(String(255))
    address1 = Column(String(255))
    address2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(20))
    zip = Column(Integer)
    phone = Column(Integer)

    def __init__(self, **data):
        self.team_id = data['team_id']
        self.club_id = data['club_id']
        self.name = data['club_name']
        self.contact_name = data['contact_name']
        self.address_1 = data['address_1']
        self.address_2 = data['address_2']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.ph_num = data['ph_num']
        self.ncca_division = data['ncca_division']
        self.ncca_conf = data['ncca_conf']

    def __repr__(self):
        return "<Team #%d: %s>" % (self.team_id, self.name)


CLUB_HEADERS = OrderedDict([('club_id', convert_int_neg_if_invalid),
                            ('club_name', unicode_conv),
                            ('team_id', convert_int_neg_if_invalid),
                            ('team_name', unicode_conv),
                            ('contact_name', unicode_conv),
                            ('address_1', unicode_conv),
                            ('address_2', unicode_conv),
                            ('city', unicode_conv),
                            ('state', convert_state),
                            ('zip', convert_zip),
                            ('ph_num', convert_phone),
                            ('ncca_division', convert_ncca_division),
                            ('ncca_conf', unicode_conv)])


class Rider(ModelBase):
    __tablename__ = "usac_rider"
    license_number = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    city = Column(String(255))
    state = Column(String(255))
    gender = Column(String(1))
    citizen = Column(String(1))
    
    racing_age = Column(Integer)
    birth_date = Column(Date)
    exp_date = Column(Date)

    is_pro = Column(Boolean)
    
    road_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    road_club = relationship("Club", foreign_keys=[road_club_id], backref="club_road_members")
    road_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    road_team = relationship("Team", foreign_keys=[road_team_id], backref="team_road_members")
    track_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    track_club = relationship("Club", foreign_keys=[track_club_id], backref="club_track_members")
    track_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    track_team = relationship("Team", foreign_keys=[track_team_id], backref="team_track_members")
    cx_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    cx_club = relationship("Club", foreign_keys=[cx_club_id], backref="club_cx_members")
    cx_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    cx_team = relationship("Team", foreign_keys=[cx_team_id], backref="team_cx_members")
    
    intl_team = Column(String(255))
    ncca_club = Column(String(255))
    
    road_cat = Column(Integer)
    track_cat = Column(Integer)
    cx_cat = Column(Integer)

    def __init__(self, **data):
        self.license_number = data['license_number']
        if self.license_number < 0:
            raise ValueError("invalid license number (less than zero)")
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        if not self.first_name or not self.last_name:
            raise ValueError("missing name")
        self.city = data['city']
        self.state = data['state']
        self.gender = data['gender']
        self.citizen = data['citizen']
        self.racing_age = data['racing_age']
        self.birth_date = data['birth_date']
        self.exp_date = data['exp_date']
        self.road_club_id = data['road_club_id']
        self.road_team_id = data['road_team_id']
        self.track_club_id = data['track_club_id']
        self.track_team_id = data['track_team_id']
        self.cx_club_id = data['cx_club_id']
        self.cx_team_id = data['cx_team_id']
        self.intl_team = data['intl_team']
        self.ncca_club = data['ncca_club']
        self.road_cat = data['road_cat']
        self.track_cat = data['track_cat']
        self.cx_cat = data['cx_cat']
        self.is_pro = self.road_cat == 1000

    def __repr__(self):
        return "<Rider #%d: %s %s>" % (self.license_number, self.first_name, self.last_name)

RIDER_HEADERS = OrderedDict([('suspension', lambda s: True if s != '' else False),
                             ('license_number', convert_int_neg_if_invalid),
                             ('last_name', unicode_conv),
                             ('first_name', unicode_conv),
                             ('city', unicode_conv),
                             ('state', unicode_conv),
                             ('gender', convert_gender),
                             ('racing_age', convert_int_none_if_invalid),
                             ('exp_date', convert_date),
                             ('road_club', unicode_conv),
                             ('road_team', unicode_conv),
                             ('track_club', unicode_conv),
                             ('track_team', unicode_conv),
                             ('cx_club', unicode_conv),
                             ('cx_team', unicode_conv),
                             ('intl_team', unicode_conv),
                             ('ncca_club', unicode_conv),
                             ('road_cat', convert_pro),
                             ('track_cat', convert_pro),
                             ('cx_cat', convert_pro),
                             ('birth_date', convert_date),
                             ('citizen', convert_citizenship),
                             ('road_club_id', convert_int_none_if_invalid),
                             ('road_team_id', convert_int_none_if_invalid),
                             ('track_club_id', convert_int_none_if_invalid),
                             ('track_team_id', convert_int_none_if_invalid),
                             ('cx_club_id', convert_int_none_if_invalid),
                             ('cx_team_id', convert_int_none_if_invalid)])