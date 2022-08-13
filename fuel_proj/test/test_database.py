import sys
import os.path
# Import from sibling directory 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from sql_app import database, models

class TestDatabaseAccess:
    def setup(self):
        self.database_accessor = database.DatabaseAccess()

    def test_search_stations(self):
        location = {
            'longitude': 26.257870, 
            'latitude': 50.624613}
        dist = 2
        result_search = self.database_accessor.search_stations(location, dist)
        with database.Sesssion() as sess:
            result_db = sess.query(models.Stations).filter(models.Stations.id == 124).first()

        assert result_search[0].address == result_db.address

    def test_get_all_stations(self):
        stations = self.database_accessor.get_all_stations()
        with database.Sesssion() as sess:
            result_db = sess.query(models.Stations)
        for station in stations:
            for station_db in result_db:
                if station.id == station_db.id:
                    assert station.address == station_db.address
                    assert station.api_id == station_db.api_id

    def test_get_station_by_id(self):
        id = 124
        result_search = self.database_accessor.get_station_by_id(id)
        with database.Sesssion() as sess:
            result_db = sess.query(models.Stations).filter(models.Stations.id == id).first()

        assert result_search.id == result_db.id

    def test_get_station_by_name(self):
        name = 'WOG'
        result_search = self.database_accessor.get_stations_by_name(name)
        with database.Sesssion() as sess:
            result_db = sess.query(models.Stations).filter(models.Stations.station_name == name)
        for station in result_search:
            for station_db in result_db:
                if station.id == station_db.id:
                    assert station.station_name == station_db.station_name

    def test_get_prices(self):
        prices = self.database_accessor.get_prices()
        with database.Sesssion() as sess:
            result_db = sess.query(models.FuelPrice)
        for price in prices:
            for price_db in result_db:
                if price.id == price_db.fuel_id:
                    assert price.price == price_db.price

    def test_get_fuel_price_by_id(self):
        id = 3
        result_search = self.database_accessor.get_fuel_price_by_id(id)
        with database.Sesssion() as sess:
            result_db = sess.query(models.FuelPrice).filter(models.FuelPrice.fuel_id == id).first()

        assert result_search.price == result_db.price
