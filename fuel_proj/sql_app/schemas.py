from pydantic import BaseModel
from . import models


class Location(BaseModel):
    
    longitude: float
    latitude: float

class Stations(BaseModel):

    station_name: str
    address: str
    location: Location
    avaiable_fuels_id: list

class Price(BaseModel):

    name: str
    price: float
    id: int
