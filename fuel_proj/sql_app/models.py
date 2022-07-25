from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stations(Base):
    __tablename__ = "stations"

    station_id = Column(Integer, primary_key=True)
    station_name = Column(String)
    address = Column(String)
    A_95 = Column(String)
    A_92 = Column(String)
    Disel = Column(String)
    Gas = Column(String)

