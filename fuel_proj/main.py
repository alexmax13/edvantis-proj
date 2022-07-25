from fastapi import FastAPI
from sql_app.database import DatabaseAccess



app = FastAPI()

@app.get("/")
def home():
    db = DatabaseAccess()
    stations = db.get_stations()
    return stations