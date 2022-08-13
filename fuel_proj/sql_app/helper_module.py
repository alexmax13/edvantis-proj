"""module with additional helping features"""
import math

class CalculationsHelper:
    """class to manage calculation in database app"""
    @staticmethod
    def calculate_distance(coord1, coord2):
        """method takes two params with coordinates and calculate distance between them"""
        lon1, lat1 = coord1['longitude'], coord1['latitude']
        lon2, lat2 = coord2['longitude'], coord2['latitude']
        earth_radius = 6371000                             # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        var_a = math.sin(delta_phi/2.0)**2+\
            math.cos(phi_1)*math.cos(phi_2)*\
            math.sin(delta_lambda/2.0)**2
        var_c = 2 * math.atan2(math.sqrt(var_a), math.sqrt(1 - var_a))
        distance_meters = earth_radius * var_c
        distance_km = distance_meters / 1000.0
        result = round(distance_km, 2)
        return float(result)
