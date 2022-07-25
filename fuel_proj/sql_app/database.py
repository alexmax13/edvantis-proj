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

# models.Base.metadata.create_all(bind=engine)   -- create base if not exist

class DatabaseAccess:
        # schema_model = schemas.Record()


    def get_stations(self): # add location 
         with Sesssion() as sess:
            result = []
            for i in sess.query(models.Stations):
                result.append(i)
            return result
