import DataBase
import Map
from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, limited_depth_first, iterative_limited_depth_first,astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math as Math

class RouteSearch(SearchProblem):
    def __init__(self, initial_state, goal, all):
        self.map = Map.Map()
        self.goal = goal
        self.all = all
        self.initial_state = initial_state
        self.db = DataBase.DB()
        wisited = []
        #later
        #self.main_distnce = float(self.map.getDistancebyTuple((self.initial_state[1],self.initial_state[2]) ,(self.goal[1],self.goal[2]))[:-2])

    def actions(self, state):
        actions = self.all
        return actions

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state.__eq__(self.goal)

    def cost(self, state, action, state2):
        print("\n",state,state2,"\n")
        if state.__eq__(self.initial_state) and state2.__eq__(self.goal):
            return 0
        
        gain = self.cargoValue(state,state2)
        waypoins = []
        if state.__eq__(self.initial_state):
            source = (state[1],state[2])
        else:
            source = (self.initial_state[1],self.initial_state[2])
            waypoins.append((state[1],state[2]))
            
        if state2.__eq__(self.goal):
            destination = (state2[1],state2[2])
        else:
            destination = (self.goal[1],self.goal[2])
            waypoins.append((state2[1],state2[2]))
        
        #distance = float(self.map.getDistancebyTuple((state[1],state[2]) ,(state2[1],state2[2]))[:-2])
        distance = float(self.map.getDistanceWaypoint(source,destination,waypoins))
        return distance - (gain*2.5)

    def cargoValue(self,state,state2):
        data2 = []
        if not state2.__eq__(self.goal):
            data2 = self.db.searchCargobySourceIDandDestinationID(state2[0],self.goal[0])
        data = self.db.searchCargobySourceIDandDestinationID(state[0],state2[0])
        data.extend(data2)
        
        total = 0
        for cargo in data:
            total += cargo['Value']

        print('total ',total)
        return total

class routeSearchHandler():
    def __init__(self,sourceNodeID,destinationNodeID):
        self.db = DataBase.DB()
        self.allnodes = self.db.listAllNodes()[:-1][0]
        print('allnodes ',self.allnodes)
        self.sourceNode = self.db.searchNodeByID_tpl(sourceNodeID)
        self.destinationNode = self.db.searchNodeByID_tpl(destinationNodeID)

        self.s = (self.sourceNode['ID'], self.sourceNode['latitude'], self.sourceNode['longitude'])
        self.d = (self.destinationNode['ID'], self.destinationNode['latitude'], self.destinationNode['longitude'])
        self.al = [(node.ID, node.latitude, node.longitude)for node in self.allnodes if node.ID != self.sourceNode['ID']]
        self.viewer = BaseViewer()
        self.problem = RouteSearch(self.s, self.d, self.al)
        self.result = uniform_cost(self.problem, viewer=self.viewer, graph_search=True)
        self.nodes_tpl = [node[0] for node in self.result.path()]
        self.nodes_tpl.pop(0)

        self.nodedict = []
        self.nodes_tpl.insert(0,self.s)
        for i in self.nodes_tpl:
            self.nodedict.append({'ID':i[0],'latitude':i[1],'longitude':i[2]})
          
        
        self.nodes = [self.db.searchNodeByID(node[0]) for node in self.nodes_tpl ]
        print('Nod_tpl ',self.nodes_tpl)
        
    
    def getNodes(self):
      
        return self.nodedict

    def getCargos(self):
        db=DataBase.DB()
        
        cargos = []
        for i in range(len(self.nodes_tpl)-1):
            
            if (i+1) == self.destinationNode['ID']:
                cargos.append((db.searchCargobySourceIDandDestinationID(self.nodes_tpl[i][0],self.nodes_tpl[i+1][0])))
            cargos.append((db.searchCargobySourceIDandDestinationID(self.nodes_tpl[i][0],self.destinationNode['ID'])))


        print('cargos ',cargos)

        cargos_all = []
        for i in cargos:
            cargos_all.extend(i)
       
        return cargos_all
        

if __name__ == "__main__":
    s = routeSearchHandler(3,20)
    node = s.getNodes()
    print(node)
    print('--------------------------------')
    print()
    cargo = s.getCargos()
    print(cargo)
"""    print('*************************')
    for i in node:
        print(i)
    print('--------------------------------')
    print('len ',len(cargo))
    for i in cargo:
        print(i)"""



