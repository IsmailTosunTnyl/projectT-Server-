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

    @cache
    def getDistanceWaypoint(self,origin,destination,waypoints=[]):

        now = datetime.now()

        origin_ = {'lat': origin[0], 'lng': origin[1]} 
        destination_ = {'lat': destination[0], 'lng': destination[1]}
        
       
        waypoints_ = []
        for i in waypoints:
            waypoints_.append({'lat': i[0], 'lng': i[1]})
        
       
        result = self.gmaps.directions(origin_, destination_, waypoints=waypoints_, optimize_waypoints=True)
        
        x = 0
        for i in result[0]['legs']:
            x += float(i['distance']['text'][:-2])
       
        return x

if __name__ == '__main__':
    map = Map()
    origin = (38.4544, 27.0966848000)  
    destination = (38.6753, 27.3088680784)
    waypoints = [(38.4393, 27.1478358578),(38.3701,27.2062576759)]
   
    #print(map.getDistancebyTuple((38.4544, 27.0966848000),(38.6753, 27.3088680784))) 
    #print(map.getDistanceWaypoint((38.4544, 27.0966848000),(38.6753, 27.3088680784),waypoints))
    print(map.getDistanceWaypoint(origin,destination,waypoints)) 