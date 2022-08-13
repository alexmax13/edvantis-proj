from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sql_app.database import DatabaseAccess

app = FastAPI()

@app.get("/")
def home():
    return "go to /stations to see stations, go to /prices to see prices"

@app.get("/stations")
def get_stations(longitude: float = 26.257870, latitude: float = 50.624613, range: float = 50.0):
    location = {
        'longitude': longitude,
        'latitude': latitude
    }
    database = DatabaseAccess()
    stations = database.search_stations(location, range)
    return stations

@app.get("/station/{id}")
def get_stations(id: int):
    database = DatabaseAccess()
    stations = database.get_station_by_id(id)
    return stations

@app.get("/stations/{name}")
def get_stations(name: str):
    database = DatabaseAccess()
    stations = database.get_stations_by_name(name)
    return stations

@app.get("/all_stations")
def get_all_stations():
    database = DatabaseAccess()
    stations = database.get_all_stations()
    return stations


@app.get("/fuel_prices")
def get_prices():
    db = DatabaseAccess()
    price = db.get_prices()
    return price

@app.get("/fuel_prices/{id}")
def get_fuel_prices(id: int):
    db = DatabaseAccess()
    price = db.get_fuel_price_by_id(id)
    return price
