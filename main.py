from flask import Flask
from flask_restful import Api, Resource
from DataBase import DB
import RouteFinder as rf

app = Flask(__name__)
api = Api(app)
db = DB()

# decorator for checking login


def login_required(f):
    def decorated_function(*args, **kwargs):
        # / is a problem in the url
        password =  kwargs['password']
        for i in range(password.count(';')):
            password = password.replace(';', '/')
        user = DB().logIn(kwargs['mail'], password)
        if user:
            return f(*args, **kwargs)
        else:
            return {'error': {'login failed':"User not in db"}}, 500
    return decorated_function

# User SignUp


class Signup(Resource):
    def get(self):
        return {"data": ""}

    def post(self, firstname, lastname, password, email, address, phone, nationalID):
        print("Sigup Post: ", firstname, lastname, email,
              password, address, phone, nationalID)
        #/ is a propblem in url
        for i in range(password.count(';')):
            password = password.replace(';', '/')
        
        try:
            db.signUp(nationalID, email, password, firstname,
                      lastname, phone, address, 0, 0)
            return {"ok":{'succesfuly sign up':201}}, 201
        except Exception as e:
            return {"error":{'User Exist':"nt"}}, 500
        
        

# User Login


class Login(Resource):
    
    def get(self, mail, password):
         
        for i in range(password.count(';')):
            password = password.replace(';', '/')
        user = DB().logIn(mail, password)
        if user:
            return {"user":user}, 200
        else:
            return {"error":{'login failed':"User not in db"}}, 500
        

    @login_required
    def post(self, mail, password):
        return {"ok":{"Login Succesful":mail}}, 201


class Cargoo(Resource):
    #Cargo list
    def get(self):
        try:
            res = db.listAllCargo()
            if res:
                return res, 200
            else:
                return "error", 500  # check if user exist in db
        except:
            return "error", 404
    #Cargoo Add
    @login_required
    def post(self, mail,password, ReceiverMail, Type, Weight, Volume, NodeID,DestNodeID, Status):
        Value = (Weight + Volume)  # this is a test value for price of cargo
        #calculate price of cargo

      
        
        try:
            OwnerID = db.searchUserbyEmail(mail)['ID']
            ReceiverID = db.searchUserbyEmail(ReceiverMail)['ID']
            db.cargoAdd(OwnerID, ReceiverID, Type, Weight,
                        Volume, NodeID,DestNodeID, Status, Value)
            return {"ok":{"Cargo added":'201'}}, 201
        except Exception as e:
            return {"error",str(e)}, 500


class CargooListAll(Resource):
    @login_required
    def get(self,mail,password):
        res = DB().listAllCargo()
        if res:
            print(res)
            return {"Cargos":res}, 200
        else:
            print("error", res)
            return {"error no cargo":res}, 500  


class NodeList(Resource):
    @login_required
    def get(self, mail, password):
        try:
            res = DB().listAllNodes()
            if res[1]:
                return {'node': res[1]}, 200
            else:
                return "error", 500  # check if node exist in db
        except Exception as e:
            return e, 404

class Route(Resource):
    @login_required
    def get(self, mail, password, sourceNodeID,destinationNodeID):
        try:
            route = rf.routeSearchHandler(sourceNodeID,destinationNodeID)
            res = route.getNodes()
            cargos = route.getCargos()
            
            if res:
                return {'route': res,'cargos':cargos}, 200
            else:
                return {"error":{'route error':'no possible route'}}, 500  # check if node exist in db
        except Exception as e:
            return {'error':{"error":str(e)+' node not valid'}}, 500


class Node(Resource):

    # node request
    def get(self, id):
        try:
            res = DB().checkNodes(id)
            if res:
                return res, 200
            else:
                return "error", 500  # check if node exist in db
        except:
            return "error", 404

# TODO Test post method : Add resources : write closeBox method
class cargoDroptoSource(Resource):
    @login_required
    def post(self, mail, password, cargoID, NodeID):
        try:
            # check if cargo exist
            try:
                cargo = db.getCargoByID(cargoID)
                if cargo['NodeID'] == NodeID:
                    # get empty boxes in the Node
                    boxes = db.getEmptyBoxes(NodeID)
                    if boxes:
                        box = boxes[0]
                        # update cargo
                        db.updateCargo(cargoID, box['ID'])
                        # update box
                        db.updateBoxStatus(box['ID'],1)
                        # update cargo status
                        db.updateCargoStatus(cargoID,'readyfordrop')
                        # open box
                        db.updateNodeandBox(NodeID,box['ID'],1)

                        return {"ok":{'cargo ready for drop to start node':cargoID}}, 201
            except Exception as e:
                return {"error":{'cargo not found Or Else':str(e)}}, 500
          
        except Exception as e:
            return {"error":str(e)}, 500
    


api.add_resource(Signup, "/signup/<string:firstname>/<string:lastname>/<string:password>/<string:email>/<string:address>/<string:phone>/<string:nationalID>")
api.add_resource(Login, "/login/<string:mail>/<string:password>")
api.add_resource(Cargoo, "/cargoadd/<string:mail>/<string:password>/<string:ReceiverMail>/<string:Type>/<string:Weight>/<string:Volume>/<string:NodeID>/<string:DestNodeID>/<string:Status>")
api.add_resource(CargooListAll, "/cargoall/<string:mail>/<string:password>")
api.add_resource(NodeList, "/nodeall/<string:mail>/<string:password>")
api.add_resource(Route, "/route/<string:mail>/<string:password>/<string:sourceNodeID>/<string:destinationNodeID>")
api.add_resource(Node, "/node/<int:id>")


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)