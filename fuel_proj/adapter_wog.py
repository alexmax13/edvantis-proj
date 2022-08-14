"""Module scrape and parse fuel and stations data from WOG network"""
import json
import requests
from sql_app import database, models

URL = "https://api.wog.ua/fuel_stations"

class WogScrapper:
    """WOG api scrapper that stores data in database"""
    def __init__(self, url: str=URL) -> None:
        self.url = url
        api_response = requests.get(self.url)
        if api_response.status_code == 200:
            print(f"Api request success")
            self.api_raw_json = json.loads(api_response.text)['data']
            self.db_accessor = database.DatabaseAccess()
        else:
            print(f"API request failed with code {api_response.status_code}")

    def save_stations_data(self):
        """parses stations data and stores to database"""
        count = 0
        for station_data in self.api_raw_json['stations']:
            station = models.Stations(
                station_name = "WOG",
                api_id = station_data['id'],
                address = station_data['name'],
                longitude = station_data['coordinates']['longitude'],
                latitude = station_data['coordinates']['latitude'])
            self.db_accessor.add_station(station)
            count+=1
        print(f"Seccessful data update of: {count} stations")

    def save_fuel_type_data(self):
        """method to get types fuel from json and save it to orm model"""
        for fuel_data in self.api_raw_json['fuel_filters']:
            if fuel_data['id'] == 3:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'])
            else:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'] + " " + fuel_data['brand'])
            self.db_accessor.add_fuel_type(fuel_type)

    def save_fuel_price_data(self):
        """method to get wog prices from json and save it to orm model"""
        with database.Sesssion() as sess:
            for fuel_data in self.api_raw_json['fuel_filters']:
                for type_id in sess.query(models.FuelType):
                    if fuel_data['id'] == type_id.api_id:
                        fuel_price = models.FuelPrice(
                            fuel_id = type_id.id,
                            price = round(float(fuel_data['price'] / 100), 2))
                        self.db_accessor.add_fuel_price(fuel_price)
                        break

    def save_fuel_avaiability_data(self):
        """method to get avaiable types and prices from api and save it to orm model"""
        list_of_current_stations = self.get_current_station_data()
        with database.Sesssion() as sess:
            for current_station_data in list_of_current_stations:
                for station in sess.query(models.Stations):
                    if current_station_data['id'] == station.api_id:
                        for fuel_type in sess.query(models.FuelType):
                            for fuel in current_station_data['fuels']:
                                if fuel_type.api_id == fuel['id']:
                                    fuel_availability = models.FuelAvailability(
                                        station_id = station.id,
                                        fuel_id = fuel_type.id)
                                    self.db_accessor.add_fuel_avaiability(fuel_availability)
                                    break
                            break

    def get_current_station_data(self):
        """method make request to wog api to get info about fuel and prices at current stations"""
        list_of_station_data = []
        for station_data in self.api_raw_json['stations']:
            station_link = station_data['link']
            response_station_id = requests.get(station_link)
            current_station_data = json.loads(response_station_id.text)['data']
            list_of_station_data.append(current_station_data)
        return list_of_station_data
