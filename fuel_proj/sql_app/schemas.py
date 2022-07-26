from pydantic import BaseModel
from . import models

class Record(BaseModel):
    station_id: int
    station_name: str
    address: str
    A_95: int
    A_92: int
    Disel: int
    Gas: int
    longitude: float
    latitude: float


    class Config():
        orm_mode = True
        orm_model = models.Stations
