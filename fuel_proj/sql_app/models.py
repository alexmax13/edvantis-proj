from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stations(Base):
    __tablename__ = "stations"

    station_id = Column(Integer, primary_key=True)
    station_name = Column(String)
    address = Column(String)
    A_95 = Column(Integer)
    A_92 = Column(Integer)
    Disel = Column(Integer)
    Gas = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)


