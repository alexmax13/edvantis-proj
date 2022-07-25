from pydantic import BaseModel

class Record(BaseModel):
    station_id: int
    station_name: str
    adress: str
    A_95: bool
    A_92: bool
    Disel: bool
    Gas: bool


    class Config:
        orm_mode = True
