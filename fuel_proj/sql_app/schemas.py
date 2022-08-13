"""module with pydantic models"""
from pydantic import BaseModel, validator

def positive_digit(value):
    if value < 0:
        raise ValueError('id must be positive')
    return value

def value_len(value):
    if len(value) < 1:
        raise ValueError("Value can't be empty")
    return value


class Location(BaseModel):
    longitude: float
    latitude: float

    @validator('longitude')
    def longitude_range(cls, value):
        if -90 <= value <= 90:
            return value
        else:
            raise ValueError('Coordinates must be from -90 to 90 degrees')

    @validator('latitude')
    def latitude_range(cls, value):
        if -180 <= value <= 180:
            return value
        else:
            raise ValueError('Coordinates must be from -180 to 180 degrees')

class Stations(BaseModel):
    id: int
    api_id: int
    station_name: str
    address: str
    location: Location
    avaiable_fuels_id: list[int]

    @validator('id')
    def positive_id(cls, value):
        return positive_digit(value)
     
    @validator('api_id')
    def positive_api_id(cls, value):
        return positive_digit(value)

    @validator('station_name')
    def station_name_len(cls, value):
        return value_len(value)

    @validator('address')
    def name_must_contain_space(cls, value):
        return value_len(value)

    @validator('avaiable_fuels_id')
    def list_of_int(cls, value):
        for i in value:
            positive_digit(i)
        return value
    

class Price(BaseModel):
    name: str
    price: float
    id: int

    @validator('name')
    def fuel_name_len(cls, value):
        return value_len(value)

    @validator('price')
    def positive_price(cls, value):
        return positive_digit(value)

    @validator('id')
    def positive_id(cls, value):
        return positive_digit(value)
