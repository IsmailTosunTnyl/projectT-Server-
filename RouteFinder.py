import DataBase
import Map
from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, limited_depth_first, iterative_limited_depth_first
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer

class RouteSearch(SearchProblem):
    def __init__(self, initial_state, goal, all):
        self.map = Map.Map()
        self.goal = goal
        self.all = all
        self.initial_state = initial_state
        self.db = DataBase.DB()

    def actions(self, state):
        actions = self.all
        return actions

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state.__eq__(self.goal)

    def cost(self, state, action, state2):
        gain = self.cargoValue(state,state2)
        distance = float(self.map.getDistancebyTuple((state[1],state[2]) ,(state2[1],state2[2]))[:-2])
        return distance - (gain*1.5)

    def cargoValue(self,state,state2):
        data = self.db.searchCargobySourceIDandDestinationID(state[0],state2[0])
        total = 0
        for cargo in data:
            total += cargo['Value']
        return total

class routeSearchHandler():
    def __init__(self,sourceNodeID,destinationNodeID):
        self.db = DataBase.DB()
        self.allnodes = self.db.listAllNodes()[:-1][0]
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
        
    
    def getNodes(self):
      
        return self.nodedict

    def getCargos(self):
        cargos = []
        for i in range(len(self.nodes_tpl)-1):
            cargos.append((self.db.searchCargobySourceIDandDestinationID(self.nodes_tpl[i][0],self.nodes_tpl[i+1][0])))

       
        return cargos[0]
        

if __name__ == "__main__":
    s = routeSearchHandler(3,10)
    node = s.getNodes()
    cargo = s.getCargos()
    print('*************************')
    for i in node:
        print(i)
    print('--------------------------------')
   
    for i in cargo:
        print(i)



