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
        gain = self.cargoValue(state2)
        distance = float(self.map.getDistancebyTuple((state[1],state[2]) ,(state2[1],state2[2]))[:-2])
        return distance - (gain*1.5)

    def cargoValue(self,state2):
        data = self.db.listCargosinNodes(state2[0])
        total = 0
        for cargo in data:
            total += cargo['Value']
        return total

class routeSearchHandler():
    def __init__(self,sourceNodeID,destinationNodeID) -> None:
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
        self.nodes_tpl.insert(0,self.s)
        self.nodes = [self.db.searchNodeByID(node[0]) for node in self.nodes_tpl ]
        print(self.nodes_tpl)
        print(self.nodes)


if __name__ == "__main__":
    routeSearchHandler(3,10)