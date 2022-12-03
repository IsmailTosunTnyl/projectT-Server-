from dotenv import load_dotenv
import os
import googlemaps
from datetime import datetime
from functools import cache


load_dotenv()
class Map():
    def __init__(self) -> None:
        API_KEY = os.getenv('API_KEY')
        self.gmaps = googlemaps.Client(key=API_KEY)

    
    @cache
    def getDistance(self,origin,destination):
        now = datetime.now()
        directions_result = self.gmaps.directions(origin.cordinates,
                                         destination.cordinates,
                                         mode="driving",
                                         departure_time=now)
        return directions_result[0]['legs'][0]['distance']['text']

    @cache
    def getDistancebyTuple(self,origin,destination):
     now = datetime.now()
     directions_result = self.gmaps.directions(origin,
                                      destination,
                                      mode="driving",
                                      departure_time=now)
     return directions_result[0]['legs'][0]['distance']['text']
