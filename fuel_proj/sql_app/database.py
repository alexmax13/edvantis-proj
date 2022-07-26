from operator import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models
import os
from dotenv import load_dotenv

load_dotenv()
USER = os.environ.get('DATABASE_USER')
PASSWORD = os.environ.get('DATABASE_PASSWORD')
HOST = os.environ.get('DATABASE_HOST')
NAME = os.environ.get('DATABASE_NAME')

DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:5432/{NAME}'

engine = create_engine(DATABASE_URI)
Sesssion = sessionmaker(bind=engine)

models.Base.metadata.create_all(bind=engine)   # -- create base if not exist

class DatabaseAccess:

    def get_stations(self, locations): # add location 
        latitude_min = locations['latitude'] - 0.5
        latitude_max = locations['latitude'] + 0.5

        longitude_min = locations['longitude'] - 0.5
        longitude_max = locations['longitude'] + 0.5

        with Sesssion() as sess:
            result = []
            for i in sess.query(
                models.Stations).filter(
                    latitude_min <= models.Stations.latitude, 
                    models.Stations.latitude <= latitude_max, 
                    longitude_min <= models.Stations.longitude, 
                    models.Stations.longitude <= longitude_max
                    ).group_by(models.Stations.station_id):
                result.append(i)
            return result

    def push_data(self, data):
        with Sesssion() as sess:
            sess.add(data)
            sess.commit()
