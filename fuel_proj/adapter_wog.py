import requests
import json
import uuid
from sql_app import database, models

URL = "https://api.wog.ua/fuel_stations"

def adapter(url):
    api_response = requests.get(url)
    data = json.loads(api_response.text)['data']
    db = database.DatabaseAccess()
    
    fuel_info_dict = data['fuel_filters']
    fuel_prices = {}
    
    for fuel_info in fuel_info_dict:
        if fuel_info['id'] == 3:
            fuel_prices['Gas'] = fuel_info['price']

        if fuel_info['id'] == 9:
            fuel_prices['Disel'] = fuel_info['price']

        if fuel_info['id'] == 8:
            fuel_prices['A_92'] = fuel_info['price']

        if fuel_info['id'] == 2:
            fuel_prices['A_95'] = fuel_info['price']

            
    for station_data in data['stations']:


        record = models.Stations(

            station_name = "WOG",
            address = station_data['name'],
            A_95 = fuel_prices['A_95'],
            A_92 = fuel_prices['A_92'],
            Disel = fuel_prices['Disel'],
            Gas = fuel_prices['Gas'],
            longitude = station_data['coordinates']['longitude'],
            latitude = station_data['coordinates']['latitude']
            )

        db.push_data(record)

        
adapter(URL)
