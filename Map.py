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
    def getDistanceWaypoint(self,origin,destination,waypoints):
        now = datetime.now()
        directions_result = self.gmaps.directions(origin,
                                         destination,
                                        waypoints=waypoints,
                                         mode="driving",
                                         departure_time=now)
        distance = 0
        print(directions_result[0].keys())
        print(directions_result[0]['waypoint_order'])
        for i in directions_result[0]['legs']:
            distance += float(i['distance']['text'][:-2])
            print(i['distance']['text'])
        return distance
    
    # get distance between multiple waypoints
    @cache
    def getDistanceWaypoints(self,waypoints):
        now = datetime.now()
        directions_result = self.gmaps.directions(waypoints[0],
                                         waypoints[-1],
                                        waypoints=waypoints[1:-1],
                                         mode="driving",
                                         departure_time=now)
        distance = 0
        print(directions_result[0].keys())
        print(directions_result[0]['waypoint_order'])
        for i in directions_result[0]['legs']:
            distance += float(i['distance']['text'][:-2])
            print(i['distance']['text'])
        return distance

if __name__ == '__main__':
    map = Map()
    waypoints = (38.4638, 27.1642137201)
    waypoints = tuple(waypoints)
    waypoints = ((38.4544, 27.0966848000),(38.6753, 27.3088680784),(38.6753, 27.3088680784),(38.4638, 27.1642137201))
    #print(map.getDistancebyTuple((38.4544, 27.0966848000),(38.6753, 27.3088680784))) 
    #print(map.getDistanceWaypoint((38.4544, 27.0966848000),(38.6753, 27.3088680784),waypoints))
    print(map.getDistanceWaypoints(waypoints)) 