import requests
from math import radians, cos, sin, asin, sqrt
import math
from unidecode import unidecode

import config
from .sms_app import SmsApp
import gsm_module


geocode_api_url = "https://maps.google.com/maps/api/geocode/json"


class Navigator(SmsApp):
    def should_handle(self, sms):
        return sms.msg_body.lower().startswith("navigate")

    def get_response(self, sms):
        sms_text_splitted = sms.msg_body.split("\"")
        origin = sms_text_splitted[1]
        destination = sms_text_splitted[3]

        origin_info = self.get_address_info(origin)
        destination_info = self.get_address_info(destination)

        origin_coord = (origin_info["geometry"]["location"]["lat"], origin_info["geometry"]["location"]["lng"])
        destination_coord = (destination_info["geometry"]["location"]["lat"], destination_info["geometry"]["location"]["lng"])

        distance = int(haversine(origin_coord, destination_coord))
        compass_bearing = int(get_compass_bearing(origin_coord, destination_coord))

        return "Dist: " + distance_to_str(distance) + "\r\nHead: " + str(compass_bearing) + " deg\r\nOrig: " + unidecode(origin_info["formatted_address"][:42]) + "\r\nDest: " + unidecode(destination_info["formatted_address"][:42])

    def get_address_info(self, address):
        response = requests.get(geocode_api_url, {
            "address": address,
            "key": config.geocode_api_key,
        }).json()
        
        return response["results"][0]


def distance_to_str(distance_in_m):
    if distance_in_m > 1000:
        return str(round(distance_in_m / 1000, 1)) + " km"

    else:
        return str(distance_in_m) + " m"


def haversine(point_1, point_2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = point_1
    lat2, lon2 = point_2

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371000 * c
    return m


def get_compass_bearing(point_1, point_2):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(point_1) != tuple) or (type(point_2) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_1[0])
    lat2 = math.radians(point_2[0])

    diffLong = math.radians(point_2[1] - point_1[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
