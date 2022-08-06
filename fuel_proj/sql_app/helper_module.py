
import math

class CalculationsHelper:
    
    @staticmethod
    def calculate_distance(coord1, coord2):

        lon1, lat1 = coord1['longitude'], coord1['latitude']
        lon2, lat2 = coord2['longitude'], coord2['latitude']

        R = 6371000                             # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi/2.0)**2+\
            math.cos(phi_1)*math.cos(phi_2)*\
            math.sin(delta_lambda/2.0)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance_meters = R * c
        distance_km = distance_meters / 1000.0

        result = round(distance_km)

        return int(result)

