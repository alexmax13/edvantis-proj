import sys
import os.path
# Import from sibling directory 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from sql_app import database, models
import adapter_wog

class TestWogScrapper:
    def setup(self):
        self.wog_scrapper = adapter_wog.WogScrapper()
        self.database_accessor = database.DatabaseAccess()

    def test_save_stations_data(self):
        db_data = self.database_accessor.get_all_stations()

        for station_json in self.wog_scrapper.api_raw_json['stations']:
            for station_db in db_data:
                if station_json['id'] == station_db.api_id:
                    assert station_json['name'] == station_db.address
                    assert station_json['coordinates']['longitude'] == station_db.location.longitude
                    assert station_json['coordinates']['latitude'] == station_db.location.latitude

    def test_save_fuel_type_data(self):
        with database.Sesssion() as sess: 
            result = sess.query(models.FuelType)
            for fuel_json in self.wog_scrapper.api_raw_json['fuel_filters']:
                for fuel_api in result:
                    if fuel_json['id'] == fuel_api.api_id:
                        if fuel_json['id'] == 3:
                            assert fuel_json['name'] == fuel_api.fuel_name
                        else:
                            name = fuel_json['name'] + ' ' + fuel_json['brand']
                            assert  name == fuel_api.fuel_name

    def test_save_fuel_price_data(self):
        db_data = self.database_accessor.get_prices()
        for fuel_json in self.wog_scrapper.api_raw_json['fuel_filters']:
            for fuel_api in db_data:
                if fuel_json['id'] == 3:
                    if fuel_json['name'] == fuel_api.name:
                        price = round(float(fuel_json['price'] / 100), 2)
                        assert fuel_api.price == price
                else:
                    name = fuel_json['name'] + ' ' + fuel_json['brand']
                    if name == fuel_api.name:
                        price = round(float(fuel_json['price'] / 100), 2)
                        assert fuel_api.price == price
        
    def test_get_current_station_data(self):
        json_stations_data = self.wog_scrapper.get_current_station_data()
        db_data = self.database_accessor.get_all_stations()
        for station_json in json_stations_data:
            for station_db in db_data:
                if station_json['name'] == station_db.address:
                    assert station_json['coordinates'] == station_db.location

