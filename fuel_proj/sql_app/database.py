"""Module to access to database postgresql"""
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from . import models
from . import helper_module as hp
from . import schemas

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
    """class has methods to write and read from database"""
    def search_stations(self, location, distance):
        """methods get stations nearby by distance param"""
        result = []
        with Sesssion() as sess:
            for station in sess.query(models.Stations):
                location_2 = {}
                location_2['longitude'] = station.longitude
                location_2['latitude'] = station.latitude
                result_distance = hp.CalculationsHelper.calculate_distance(location, location_2)
                if result_distance <= distance:
                    price_list_id = []
                    for avaiable_fuel in sess.query(models.FuelAvailability):
                        if station.id == avaiable_fuel.station_id:
                            price_list_id.append(avaiable_fuel.fuel_id)
                    loc = schemas.Location(
                        longitude = station.longitude,
                        latitude = station.latitude)
                    dict_ = schemas.Stations(
                        id = station.id,
                        api_id = station.api_id,
                        station_name = station.station_name,
                        address = station.address,
                        location = loc,
                        avaiable_fuels_id = price_list_id)
                    result.append(dict_)
        return result

    def get_all_stations(self):
        """get all fuel stations """
        result = []
        with Sesssion() as sess:
            for station in sess.query(models.Stations):
                price_list_id = []
                for avaiable_fuel in sess.query(models.FuelAvailability):
                    if station.id == avaiable_fuel.station_id:
                        price_list_id.append(avaiable_fuel.fuel_id)
                loc = schemas.Location(
                    longitude = station.longitude,
                    latitude = station.latitude)
                dict_ = schemas.Stations(
                    id = station.id,
                    api_id = station.api_id,
                    station_name = station.station_name,
                    address = station.address,
                    location = loc,
                    avaiable_fuels_id = price_list_id)
                result.append(dict_)
        return result

    def get_station_by_id(self, id):
        """get station by id """
        with Sesssion() as sess:
            for station in sess.query(models.Stations).where(models.Stations.id == id):
                price_list_id = []
                for avaiable_fuel in sess.query(models.FuelAvailability):
                    if station.id == avaiable_fuel.station_id:
                        price_list_id.append(avaiable_fuel.fuel_id)
                loc = schemas.Location(
                    longitude = station.longitude,
                    latitude = station.latitude)
                dict_ = schemas.Stations(
                    id = station.id,
                    api_id = station.api_id,
                    station_name = station.station_name,
                    address = station.address,
                    location = loc,
                    avaiable_fuels_id = price_list_id)
                return dict_
        return {}

    def get_stations_by_name(self, name):
        """get station by name"""
        result = []
        with Sesssion() as sess:
            for station in sess.query(models.Stations).where(func.lower(models.Stations.station_name) == func.lower(name)):
                price_list_id = []
                for avaiable_fuel in sess.query(models.FuelAvailability):
                    if station.id == avaiable_fuel.station_id:
                        price_list_id.append(avaiable_fuel.fuel_id)
                loc = schemas.Location(
                    longitude = station.longitude,
                    latitude = station.latitude)
                dict_ = schemas.Stations(
                    id = station.id,
                    api_id = station.api_id,
                    station_name = station.station_name,
                    address = station.address,
                    location = loc,
                    avaiable_fuels_id = price_list_id)
                result.append(dict_)
        return result

    def get_prices(self):
        """method to get prices"""
        with Sesssion() as sess:
            price_list = []
            for fuel_type in sess.query(models.FuelType):
                for fuel_price in sess.query(models.FuelPrice):
                    if fuel_type.id == fuel_price.fuel_id:
                        price_dict = schemas.Price(
                            name = fuel_type.fuel_name,
                            price = fuel_price.price,
                            id = fuel_type.id)
                        price_list.append(price_dict)
                        break
        return price_list

    def get_fuel_price_by_id(self, id):
        """get prices by id"""
        with Sesssion() as sess:
            for fuel_type in sess.query(models.FuelType).where(models.FuelType.id == id):
                for fuel_price in sess.query(models.FuelPrice):
                    if fuel_type.id == fuel_price.fuel_id:
                        price_dict = schemas.Price(
                            name = fuel_type.fuel_name,
                            price = fuel_price.price,
                            id = fuel_type.id)
                        return price_dict
        return {}

    def add_station(self, data):
        """write data to table stations in database"""
        with Sesssion() as sess:
            result = sess.query(models.Stations).where(models.Stations.api_id == data.api_id)
            if len([*result]) > 0:
                data.id = result.first().id
                sess.merge(data)
                sess.commit()
            else:
                sess.add(data)
                sess.commit()

    def add_fuel_type(self, fuel_type):
        """write data to table fuel_type in database"""
        with Sesssion() as sess:
            result = sess.query(models.FuelType).where(models.FuelType.api_id == fuel_type.api_id)
            if len([*result]) > 0:
                fuel_type.id = result.first().id
                sess.merge(fuel_type)
                sess.commit()
            else:
                sess.add(fuel_type)
                sess.commit()

    def add_fuel_price(self, fuel_price):
        """write data to table fuel_price in database"""
        with Sesssion() as sess:
            result = sess.query(models.FuelPrice).where(
                models.FuelPrice.fuel_id == fuel_price.fuel_id)
            if len([*result]) > 0:
                fuel_price.id = result.first().id
                sess.merge(fuel_price)
                sess.commit()
            else:
                sess.add(fuel_price)
                sess.commit()

    def add_fuel_avaiability(self, fuel_avaiability):
        """write data to table fuel_avaiability in database"""
        with Sesssion() as sess:
            result = sess.query(models.FuelAvailability).filter(
                models.FuelAvailability.station_id == fuel_avaiability.station_id,
                models.FuelAvailability.fuel_id == fuel_avaiability.fuel_id,)
            if len([*result]) > 0:
                fuel_avaiability.id = result.first().id
                sess.merge(fuel_avaiability)
                sess.commit()
            else:
                sess.add(fuel_avaiability)
                sess.commit()
