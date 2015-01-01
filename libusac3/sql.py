from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


class Club(Base):
    __tablename__ = "usac_club"

    club_id = Column(Integer, primary_key=True)
    name = Column(String(255))

    contact_name = Column(String(255))
    address_1 = Column(String(255))
    address_2 = Column(String(255))
    city = Column(String(64))
    state = Column(String(2))
    zipcode = Column(Integer)
    phone_number = Column(String(32))
    division = Column(Integer)
    ncca_conf = Column(String(5))

    def __init__(self, data):
        self.club_id = data[0]
        self.name = data[1]

        self.contact_name = data[4]
        self.address_1 = data[5]
        self.address_2 = data[6]
        self.city = data[7]
        self.state = data[8]
        self.zipcode = data[9]
        self.phone_number = data[10]
        self.division = data[11]
        self.ncca_conf = data[12]


class Team(Base):
    __tablename__ = "usac_team"

    team_id = Column(Integer, primary_key=True)
    name = Column(String(255))

    club_id = Column(Integer, ForeignKey(Club.__tablename__+".club_id"))
    club = relationship("Club", backref="teams")

    def __init__(self, data):
        self.team_id = data[2]
        self.name = data[3]
        self.club_id = data[0]


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
    coll_club = Column(String(255))

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

    def __init__(self, data):
        self.suspension = data[0]     # Suspension Status
        self.license = data[1]        # License Number
        self.first_name = data[3]     # First Name
        self.last_name = data[2]      # Last Name
        self.city = data[4]           # City
        self.state = data[5]          # State
        self.zipcode = data[6]        # Zip Code
        self.gender = data[7]         # Gender
        self.racing_age = data[8]     # Racing Age
        self.expire_date = data[9]    # License Expiration Date
        self.intl_team = data[18]     # Intl Team
        self.road_cat = data[20]      # Road Category
        self.track_cat = data[21]     # Track Category
        self.xc_cat = data[22]        # XC Category
        self.dh_cat = data[23]        # DH Category
        self.ot_cat = data[24]        # OT Category
        self.mx_cat = data[25]        # MX Category
        self.cx_cat = data[26]        # CX Category
        self.birth_date = data[27]    # Birthday
        self.citizenship = data[28]   # Citizenship
        self.road_club_id = data[29]
        self.road_team_id = data[30]  # RD Club/Team ID
        self.track_club_id = data[31]
        self.track_team_id = data[32] # Track Club/Team ID
        self.mtn_club_id = data[33]
        self.mtn_team_id = data[34]   # MTN Club/Team ID
        self.cx_club_id = data[35]
        self.cx_team_id = data[36]    # CX Club/Team ID
        self.coll_club_id = data[37]  # Collegiate Club ID
        self.uci_code = data[38]      # UCI Code
        self.cx_rank = data[39]       # CX Rank
        self.hs_club_id = data[42]
        self.hs_team_id = data[43]    # HS Club/Team ID

    def __repr__(self):
        return "<Rider #%d '%s %s'>" % (self.license, self.first_name, self.last_name)

