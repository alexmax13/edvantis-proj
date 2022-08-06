import requests
import json
from sql_app import database, models

URL = "https://api.wog.ua/fuel_stations"

def adapter(url):
    api_response = requests.get(url)
    data = json.loads(api_response.text)['data']
    db = database.DatabaseAccess()
    
    with database.Sesssion() as sess:        
        for station_data in data['stations']:

            stations = models.Stations(
                station_name = "WOG",
                api_id = station_data['id'],
                address = station_data['name'],
                longitude = station_data['coordinates']['longitude'],
                latitude = station_data['coordinates']['latitude'])

            db.push_data(stations)

        for fuel_data in data['fuel_filters']:
            if fuel_data['id'] == 3:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'])
                    
            else:
                fuel_type = models.FuelType(
                    api_id = fuel_data['id'],
                    fuel_name = fuel_data['name'] + " " + fuel_data['brand'])
            
            db.push_data(fuel_type)

        for fuel_data in data['fuel_filters']:
                for id in sess.query(models.FuelType):
                    if fuel_data['id'] == id.api_id:
                        fuel_price = models.FuelPrice(
                            fuel_id = id.id,
                            price = round(float(fuel_data['price'] / 100), 2))
                        db.push_data(fuel_price)
                        break


        
        for station_data in data['stations']:

            station_link = station_data['link']
            response_station_id = requests.get(station_link)
            current_station_data = json.loads(response_station_id.text)['data']

            for statation in sess.query(models.Stations):
                if current_station_data['id'] == statation.api_id:
                    for type in sess.query(models.FuelType):
                        for fuel in current_station_data['fuels']:
                            if type.api_id == fuel['id']:

                                fuel_availability = models.FuelAvailability(
                                    station_id = statation.id,
                                    fuel_id = type.id)
                                    
                                db.push_data(fuel_availability)
                                break
                    break
                    
                            
adapter(URL)
