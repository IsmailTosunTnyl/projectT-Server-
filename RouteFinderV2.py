import DataBase
from Map import Map
from Utils import Node
import requests
from bs4 import BeautifulSoup

class RouteFinderV2:
    def __init__(self,sourceNodeID,destinationNodeID) -> None:
        self.map = Map()
        self.db = DataBase.DB()
        self.allnodes =self.db.listAllNodes()[:-1][0]
        self.nodes = []
        self.rewards = {}
        
        self.sourceNode = self.db.searchNodeByID(sourceNodeID)
        self.destNode = self.db.searchNodeByID(destinationNodeID)
        
        self.source_coordinates = (self.sourceNode.latitude,self.sourceNode.longitude)
        self.destination_coordinates = (self.destNode.latitude,self.destNode.longitude)
        self.baseDistance = self.map.getDistanceWaypoint(self.source_coordinates,self.destination_coordinates)
        
        self.route=[]
        
        for node in self.allnodes:
            self.nodes.append((node.ID,node.latitude,node.longitude))
            
        for node in self.allnodes:
            self.rewards[node.ID] = {}
            for node2 in self.allnodes:
                self.rewards[node.ID][node2.ID] = self.cargoValue(node.ID,node2.ID)
        
        for i in self.rewards:
            print(i,self.rewards[i])
        
    def cargoValue(self,state,state2):
        cargos = self.db.searchCargobySourceIDandDestinationID(state,state2)
        total = 0
        for cargo in cargos:
            total += cargo['Value']

        return total
    
    def callculate_route(self):
        for node1 in range(len(self.allnodes)):
            for node2 in range(node1,len(self.allnodes)):
                 
                waypoints = [(self.allnodes[node1].latitude,self.allnodes[node1].longitude),(self.allnodes[node2].latitude,self.allnodes[node2].longitude)]
                distance = self.map.getDistanceWaypoint(self.source_coordinates,self.destination_coordinates,waypoints=tuple(waypoints))
                
                
                reward = self.rewards[self.allnodes[node1].ID][self.allnodes[node2].ID]
                # secret formula
                petrol_prices = self.petrol_price()
                val = reward - (abs(self.baseDistance - distance)*petrol_prices) 
                print("Distance between",self.sourceNode.nodeName,"and",self.destNode.nodeName,"with waypoints",self.allnodes[node1].nodeName,"and",self.allnodes[node2].nodeName,"is",distance,"Reward:",reward,'val:',val)
                if val > 0:
                    print("Distance between",self.sourceNode.nodeName,"and",self.destNode.nodeName,"with waypoints",self.allnodes[node1].nodeName,"and",self.allnodes[node2].nodeName,"is",distance,"Reward:",reward)
                    print("Value:",val)
                    self.route.append((val,self.allnodes[node1].ID,self.allnodes[node2].ID))
        self.route = set(self.route)
           
    def get_route(self):
        self.callculate_route()

        return self.route
    
    def get_cargos(self):
        cargos =[]
        for trip in self.route:
            cc=self.db.searchCargobySourceIDandDestinationID(trip[1],trip[2])
            for cargo in cc:
                cargos.append(cargo)

        for cargo in cargos:
            print(cargo)
        return cargos
    
    def petrol_price(self):
        # Make a request to the website
        response = requests.get('https://www.globalpetrolprices.com/Turkey/gasoline_prices/')

        # Parse the HTML of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element on the page
        element = soup.find_all('td', {'height': '30', 'align': 'center'})

        return float(element[2].text)

    
if __name__ == "__main__":
    rf = RouteFinderV2(3,20)
    rf.get_route()
    print(len(rf.get_cargos()))
    print(rf.route)