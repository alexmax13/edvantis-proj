from fastapi import FastAPI
from sql_app.database import DatabaseAccess


app = FastAPI()

@app.get("/")
def home(location={"latitude": 50.624613, "longitude":26.257870
}): # validation
    db = DatabaseAccess()
    stations = db.get_stations(location)
    return stations

