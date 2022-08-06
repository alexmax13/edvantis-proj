from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stations(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    station_name = Column(String)
    address = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)


class FuelType(Base):
    __tablename__ = "fuel_type"

    id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    fuel_name = Column(String)


class FuelPrice(Base):
    __tablename__ = "fuel_price"

    id = Column(Integer, primary_key = True)
    fuel_id = Column(ForeignKey(FuelType.id))
    price = Column(Float)


class FuelAvailability(Base):
    __tablename__ = "fuel_availability"

    id = Column(Integer, primary_key=True)
    station_id = Column(ForeignKey(Stations.id))
    fuel_id = Column(ForeignKey(FuelType.id))
