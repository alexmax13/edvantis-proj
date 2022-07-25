from gc import get_stats
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models

DATABASE_URI = 'postgresql://oleksandr:fuel123@localhost:5432/fuel_stations'
engine = create_engine(DATABASE_URI)
Sesssion = sessionmaker(bind=engine)

# models.Base.metadata.create_all(bind=engine)   -- create base if not exist

class DatabaseAccess:
        # schema_model = schemas.Record()


    def get_stations(self):
         with Sesssion() as sess:
            result = []
            for i in sess.query(models.Stations):
                result.append(i)
            return result


