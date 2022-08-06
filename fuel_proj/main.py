from fastapi import FastAPI
from sql_app.database import DatabaseAccess


app = FastAPI()


from pydantic import BaseModel

class Location(BaseModel):
    longitude: float 
    latitude: float


class Range(BaseModel):
    range: float


@app.get("/")
def home():
    return "go to /stations to see stations, go to /price to see prices"

@app.get("/stations")  # add parametrs
def stations(location: Location={"longitude":26.257870, "latitude": 50.624613}, range: Range=50.0): # validation
    db = DatabaseAccess()
    stations = db.get_stations(location, range)
    return stations

@app.get("/price")
def price():
    db = DatabaseAccess()
    price = db.get_price()
    return price