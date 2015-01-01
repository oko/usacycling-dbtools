from sqlalchemy.ext.declarative import declarative_base

# Change libusac3.sql_base.Base before importing
# libusac3.sql in order to import models using your
# application's database mapping.
Base = declarative_base()