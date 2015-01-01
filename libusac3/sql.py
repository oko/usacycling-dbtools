from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .sql_base import Base


class Club(Base):
    __tablename__ = "usac_club"

    club_id = Column(Integer, primary_key=True)
    club_name = Column(String(255))

    contact_name = Column(String(255))
    address_1 = Column(String(255))
    address_2 = Column(String(255))
    city = Column(String(64))
    state = Column(String(2))
    zipcode = Column(Integer)
    phone_number = Column(String(32))
    division = Column(Integer)
    ncca_conf = Column(String(5))

    def __init__(self, **kwargs):
        self.club_id = kwargs["club_id"]
        self.club_name = kwargs["club_name"]

        self.contact_name = kwargs["contact_name"]
        self.address_1 = kwargs["address_1"]
        self.address_2 = kwargs["address_2"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.zipcode = kwargs["zipcode"]
        self.phone_number = kwargs["phone_number"]
        self.division = kwargs["division"]
        self.ncca_conf = kwargs["ncca_conf"]

    def __repr__(self):
        return "<Club #%d: %s>" % (self.club_id, self.name)


class Team(Base):
    __tablename__ = "usac_team"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(255))

    club_id = Column(Integer, ForeignKey(Club.__tablename__+".club_id"))
    club = relationship("Club", backref="teams")

    def __init__(self, **kwargs):
        self.team_id = kwargs["team_id"]
        self.team_name = kwargs["team_name"]
        self.club_id = kwargs["club_id"]

    def __repr__(self):
        return "<Team #%d: %s (club #%d)>" % (self.team_id, self.name, self.club_id)


class Rider(Base):

    __tablename__ = "usac_rider"

    suspension = Column(Integer)

    license = Column(Integer, primary_key=True)

    first_name = Column(String(64))
    last_name = Column(String(64))

    city = Column(String(64))
    state = Column(String(2))
    zipcode = Column(Integer)

    gender = Column(String(1))
    racing_age = Column(Integer)

    expire_date = Column(Date)

    intl_team = Column(String(255))

    road_cat = Column(Integer)
    track_cat = Column(Integer)
    xc_cat = Column(Integer)
    dh_cat = Column(Integer)
    ot_cat = Column(Integer)
    mx_cat = Column(Integer)
    cx_cat = Column(Integer)

    birth_date = Column(Date)
    citizenship = Column(String(1))
    
    road_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    road_club = relationship("Club", foreign_keys=[road_club_id], backref="club_road_members")
    road_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    road_team = relationship("Team", foreign_keys=[road_team_id], backref="team_road_members")
    track_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    track_club = relationship("Club", foreign_keys=[track_club_id], backref="club_track_members")
    track_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    track_team = relationship("Team", foreign_keys=[track_team_id], backref="team_track_members")
    mtn_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    mtn_club = relationship("Club", foreign_keys=[mtn_club_id], backref="club_mtn_members")
    mtn_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    mtn_team = relationship("Team", foreign_keys=[mtn_team_id], backref="team_mtn_members")
    cx_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    cx_club = relationship("Club", foreign_keys=[cx_club_id], backref="club_cx_members")
    cx_team_id = Column(Integer, ForeignKey(Team.__tablename__ + ".team_id"))
    cx_team = relationship("Team", foreign_keys=[cx_team_id], backref="team_cx_members")

    coll_club_id = Column(Integer, ForeignKey(Club.__tablename__ + ".club_id"))
    coll_club = relationship("Club", foreign_keys=[coll_club_id], backref="club_coll_members")
    
    uci_code = Column(String(32))
    cx_rank = Column(Float)

    hs_club_id = Column(Integer)
    hs_team_id = Column(Integer)

    def __init__(self, **kwargs):
        self.suspension = kwargs["suspension"]  # Suspension Status
        self.license = kwargs["license"]        # License Number
        self.first_name = kwargs["first_name"]     # First Name
        self.last_name = kwargs["last_name"]      # Last Name
        self.city = kwargs["city"]           # City
        self.state = kwargs["state"]          # State
        self.zipcode = kwargs["zipcode"]        # Zip Code
        self.gender = kwargs["gender"]         # Gender
        self.racing_age = kwargs["racing_age"]     # Racing Age
        self.expire_date = kwargs["expire_date"]    # License Expiration Date
        self.intl_team = kwargs["intl_team"]     # Intl Team
        self.road_cat = kwargs["road_cat"]      # Road Category
        self.track_cat = kwargs["track_cat"]     # Track Category
        self.xc_cat = kwargs["xc_cat"]        # XC Category
        self.dh_cat = kwargs["dh_cat"]        # DH Category
        self.ot_cat = kwargs["ot_cat"]        # OT Category
        self.mx_cat = kwargs["mx_cat"]        # MX Category
        self.cx_cat = kwargs["cx_cat"]        # CX Category
        self.birth_date = kwargs["birth_date"]    # Birthday
        self.citizenship = kwargs["citizenship"]   # Citizenship
        self.road_club_id = kwargs["road_club_id"]
        self.road_team_id = kwargs["road_team_id"]  # RD Club/Team ID
        self.track_club_id = kwargs["track_club_id"]
        self.track_team_id = kwargs["track_team_id"] # Track Club/Team ID
        self.mtn_club_id = kwargs["mtn_club_id"]
        self.mtn_team_id = kwargs["mtn_team_id"]   # MTN Club/Team ID
        self.cx_club_id = kwargs["cx_club_id"]
        self.cx_team_id = kwargs["cx_team_id"]    # CX Club/Team ID
        self.coll_club_id = kwargs["coll_club_id"]  # Collegiate Club ID
        self.uci_code = kwargs["uci_code"]      # UCI Code
        self.cx_rank = kwargs["cx_rank"]       # CX Rank
        self.hs_club_id = kwargs["hs_club_id"]
        self.hs_team_id = kwargs["hs_team_id"]    # HS Club/Team ID

    def __repr__(self):
        return "<Rider #%d '%s %s'>" % (self.license, self.first_name, self.last_name)

