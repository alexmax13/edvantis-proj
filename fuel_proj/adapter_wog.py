"""Module scrape and parse fuel and stations data from WOG network"""
import json
import requests
from sql_app import database, models

URL = "https://api.wog.ua/fuel_stations"

class WogScrapper:
    """WogScrapper class use to scrape data from WOG api and send to database"""
    def __init__(self, url) -> None:
        self.url = url
        api_response = requests.get(self.url)
        if api_response.status_code == 200:
            self.data = json.loads(api_response.text)['data']
            self.data_base = database.DatabaseAccess()

        else:
            print("Data is empty")

    def save_stations_data(self):
        """method to get stations data from json and save it to orm model"""
        for station_data in self.data['stations']:
            stations = models.Stations(
                station_name = "WOG",
                api_id = station_data['id'],
                address = station_data['name'],
                longitude = station_data['coordinates']['longitude'],
                latitude = station_data['coordinates']['latitude'])
            self.data_base.add_station(stations)

    def save_fuel_type_data(self):
        """method to get types fuel from json and save it to orm model"""
        for fuel_data in self.data['fuel_filters']:
            if fuel_data['id'] == 3:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'])
            else:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'] + " " + fuel_data['brand'])
            self.data_base.add_fuel_type(fuel_type)

    def save_price_data(self):
        """method to get wog prices from json and save it to orm model"""
        with database.Sesssion() as sess:
            for fuel_data in self.data['fuel_filters']:
                for type_id in sess.query(models.FuelType):
                    if fuel_data['id'] == type_id.api_id:
                        fuel_price = models.FuelPrice(
                            fuel_id = type_id.id,
                            price = round(float(fuel_data['price'] / 100), 2))
                        self.data_base.add_fuel_price(fuel_price)
                        break

    def save_avaiability_data(self):
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
                                    self.data_base.add_fuel_avaiability(fuel_availability)
                                    break
                            break

    def get_current_station_data(self):
        """method make request to wog api to get info about fuel and prices at current stations"""
        list_of_station_data = []
        for station_data in self.data['stations']:
            station_link = station_data['link']
            response_station_id = requests.get(station_link)
            current_station_data = json.loads(response_station_id.text)['data']
            list_of_station_data.append(current_station_data)
        return list_of_station_data

if __name__ == "__main__":
    scrapper_wog = WogScrapper(URL)
    scrapper_wog.save_stations_data()
    scrapper_wog.save_fuel_type_data()
    scrapper_wog.save_price_data()
    scrapper_wog.save_avaiability_data()
