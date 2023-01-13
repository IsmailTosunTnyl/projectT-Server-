from flask import Flask, request
from flask_restful import Api, Resource
from DataBase import DB
import RouteFinder as rf
import RouteFinderV2
import time

app = Flask(__name__)
api = Api(app)
db = DB()

# decorator for checking login


def login_required(f):
    def decorated_function(*args, **kwargs):
        # / is a problem in the url
        password = kwargs['password']
        for i in range(password.count(';')):
            password = password.replace(';', '/')
        user = DB().logIn(kwargs['mail'], password)
        if user:
            return f(*args, **kwargs)
        else:
            return {'error': {'login failed': "User not in db"}}, 500
    return decorated_function

# User SignUp


class Signup(Resource):
    def get(self):
        return {"data": ""}

    def post(self, firstname, lastname, password, email, address, phone, nationalID):
        print("Sigup Post: ", firstname, lastname, email,
              password, address, phone, nationalID)
        # / is a propblem in url
        for i in range(password.count(';')):
            password = password.replace(';', '/')

        try:
            db.signUp(nationalID, email, password, firstname,
                      lastname, phone, address, 0, 0)
            return {"ok": {'succesfuly sign up': 201}}, 201
        except Exception as e:
            return {"error": {'User Exist': "nt"}}, 500


# User Login


class Login(Resource):

    def get(self, mail, password):

        for i in range(password.count(';')):
            password = password.replace(';', '/')
        user = DB().logIn(mail, password)
        if user:
            return {"user": user}, 200
        else:
            return {"error": {'login failed': "User not in db"}}, 500

    @login_required
    def post(self, mail, password):
        return {"ok": {"Login Succesful": mail}}, 201


class Cargoo(Resource):
    # Cargo list
    def get(self):
        try:
            res = db.listAllCargo()
            if res:
                return res, 200
            else:
                return "error", 500  # check if user exist in db
        except:
            return "error", 404
    # Cargoo Add

    @login_required
    def post(self, mail, password, ReceiverMail, Type, Weight, Volume, NodeID, DestNodeID, Status):
        Value = (Weight + Volume)  # this is a test value for price of cargo
        # calculate price of cargo

        try:
            OwnerID = db.searchUserbyEmail(mail)['ID']
            ReceiverID = db.searchUserbyEmail(ReceiverMail)['ID']
            db.cargoAdd(OwnerID, ReceiverID, Type, Weight,
                        Volume, NodeID, DestNodeID, Status, Value)
            return {"ok": {"Cargo added": '201'}}, 201
        except Exception as e:
            return  500


class CargooListAll(Resource):
    @login_required
    def get(self, mail, password):
        res = DB().listAllCargo()
        if res:
            print(res)
            return {"Cargos": res}, 200
        else:
            print("error", res)
            return {"error no cargo": res}, 500


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
    def get(self, mail, password, sourceNodeID, destinationNodeID):
        rf2 = RouteFinderV2.RouteFinderV2(sourceNodeID, destinationNodeID)
        try:
            db = DB()

            rf2.get_route()
            res = rf2.route
            cargos = rf2.get_cargos()
            nodes = []
            for i in res:
                nodes.append(db.searchNodeByID_tpl(i[1]))

            if res:
                return {'nodes': nodes, 'cargos': cargos}, 200
            else:
                # check if node exist in db
                return {"error": {'route error': 'no possible route'}}, 500
        except Exception as e:
            return {'error': {"error": str(e)+' node not valid'}}, 500


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
    def get(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            # close the box
            db.updateNodeandBox(NodeID, boxID, 2)

            db.updateCargoStatus(cargoID, 'startbox')
            return {"ok": {'Box Closed': cargoID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500

    @login_required
    def post(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            # check if cargo exist
            try:
                cargo = db.getCargoByID(cargoID)
                if int(cargo['NodeID']) == int(NodeID):
                    # get empty boxes in the Node
                    boxes = db.getEmptyBoxes(NodeID)
                    if boxes:
                        box = boxes[0]
                        # update cargo
                        db.updateCargoBox(cargoID, box['ID'])
                        # update box
                        db.updateBoxStatus(box['ID'], 1)
                        # update cargo status
                        db.updateCargoStatus(cargoID, 'readyfordrop')
                        # open box
                        db.updateNodeandBox(NodeID, box['ID'], 1)

                        return {"ok": {'cargo ready for drop to start node': cargoID}}, 201
                    else:
                        return {"error": {'no empty box': NodeID}}, 500
                else:
                    return {"error": {'cargo not define for this node': {NodeID: cargo['NodeID']}}}, 500
            except Exception as e:
                return {"error": {'cargo not found Or Else': str(e)}}, 500

        except Exception as e:
            return {"error": str(e)}, 500


class CargoListOwn(Resource):
    @login_required
    def get(self, mail, password):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            res = db.listOwnerCargo(user['ID'], "readyforDTS")
            if res:
                return {"Cargos": res}, 200
            else:
                return {"error": {'no cargo': mail}}, 500
        except Exception as e:
            return {"error": str(e)}, 500

    @login_required
    def post(self, mail, password):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            res = db.listReceiverCargo(user['ID'], "endbox")
            if res:
                return {"Cargos": res}, 200
            else:
                return {"error": {'no cargo': mail}}, 500
        except Exception as e:
            return {"error": str(e)}, 500


class CargoTakeFromSource(Resource):
    @login_required
    def get(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            # close the box
            db.updatedestNodeandBox(NodeID, boxID, 2)

            db.updateCargoStatus(cargoID, 'done')
            return {"ok": {'Box Closed': cargoID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500

    @login_required
    def post(self, mail, password, cargoID, NodeID):

        try:
            db = DB()
            cargo = db.getCargoByID(cargoID)
            user = db.searchUserbyEmail(mail)
            if (int(cargo['destNodeID']) == int(NodeID)) and (user['ID'] == cargo['ReceiverID']):

                boxID = cargo['BoxID']
                # update cargo
                db.updateCargoBox(cargoID, boxID)
                # update box
                db.updateBoxStatus(boxID, 0)
                # update cargo status
                db.updateCargoStatus(cargoID, 'done')
                # open box
                db.updatedestNodeandBox(NodeID, boxID, 1)

                return {"ok": {'cargo ready for Take from start node': cargoID}}, 201

            else:
                return {"error": {'cargo not define for this node': {NodeID: cargo['NodeID']}}}, 500
        except Exception as e:
            return {"error": {'cargo not found Or Else': str(e)}}, 500





class SelectedCargos(Resource):
    @login_required
    def post(self, mail, password,cargos):
       # get json data which sended from client
        data = cargos.split('/')[-1].split('-')[:-1]
        #db.getCargoByID(data['cargoID'])
        user = db.searchUserbyEmail(mail)
        for cargoID in data:
            db.updateCargoStatus(cargoID, 'readyfordriver')
            db.updateDriverID(cargoID, user['ID'])
        
        
        print("-----------------")
        return {"ok": data}, 201

class listDriverCargos(Resource):
    @login_required
    def get(self, mail, password):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            res = db.getCargobyDriverID(user['ID'],"readyfordriver")
            if res:
                return {"Cargos": res}, 200
            else:
                return {"error": {'no cargo': user}}, 500
        except Exception as e:
            return {"error": str(e)}, 500
    
    @login_required
    def post(self, mail, password):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            res = db.getCargobyDriverID(user['ID'], "transporting")
            if res:
                return {"Cargos": res}, 200
            else:
                return {"error": {'no cargo': user}}, 500
        except Exception as e:
            return {"error": str(e)}, 500
        
class driverTakeCargo(Resource):
    @login_required
    def get(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            if (user['ID'] == cargo['DriverID']):
                db.updateNodeandBox(NodeID, boxID, 1)
                #db.updateCargoStatus(cargoID, 'transporting')
                # update box
                db.updateBoxStatus(boxID, 0)
                return {"ok": {'Box Opened': boxID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500
        
    @login_required
    def post(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            if (user['ID'] == cargo['DriverID']):
                db.updateNodeandBox(NodeID, boxID, 2)
                time.sleep(6)
                db.updateCargoStatus(cargoID, 'transporting')
                # update box
                db.updateBoxStatus(boxID, 0)
                return {"ok": {'Box closed': boxID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500


class driverDropCargo(Resource):
    @login_required
    def get(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            if (user['ID'] == cargo['DriverID']):
                db.updateNodeandBox(NodeID, boxID, 1,True)
                #db.updateCargoStatus(cargoID, 'endbox')
                # update box
                db.updateBoxStatus(boxID, 0)
                return {"ok": {'Box Opened': boxID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500
        
    @login_required
    def post(self, mail, password, cargoID, NodeID):
        db = DB()
        try:
            user = db.searchUserbyEmail(mail)
            cargo = db.getCargoByID(cargoID)
            boxID = cargo['BoxID']
            if (user['ID'] == cargo['DriverID']):
                db.updateNodeandBox(NodeID, boxID, 2,True)
                db.updateCargoStatus(cargoID, 'endbox')
                # update box
                db.updateBoxStatus(boxID, 0)
                return {"ok": {'Box closed': boxID}}, 201
        except Exception as e:
            return {"error": {"err": str(e)}}, 500
        
                
                
            

api.add_resource(
    Signup, "/signup/<string:firstname>/<string:lastname>/<string:password>/<string:email>/<string:address>/<string:phone>/<string:nationalID>")
api.add_resource(Login, "/login/<string:mail>/<string:password>")
api.add_resource(Cargoo, "/cargoadd/<string:mail>/<string:password>/<string:ReceiverMail>/<string:Type>/<string:Weight>/<string:Volume>/<string:NodeID>/<string:DestNodeID>/<string:Status>")
api.add_resource(CargooListAll, "/cargoall/<string:mail>/<string:password>")
api.add_resource(NodeList, "/nodeall/<string:mail>/<string:password>")
api.add_resource(
    Route, "/route/<string:mail>/<string:password>/<string:sourceNodeID>/<string:destinationNodeID>")
api.add_resource(Node, "/node/<int:id>")
# To close (GET) box and openforDTS (POST)
api.add_resource(cargoDroptoSource,
                 "/cargoDTS/<string:mail>/<string:password>/<string:cargoID>/<string:NodeID>")
api.add_resource(CargoListOwn, "/cargoownDTS/<string:mail>/<string:password>")
api.add_resource(CargoTakeFromSource,
                 "/cargoTFS/<string:mail>/<string:password>/<string:cargoID>/<string:NodeID>")
api.add_resource(SelectedCargos, "/selectedcargos/<string:mail>/<string:password>/<string:cargos>")
api.add_resource(listDriverCargos, "/listDriverCargos/<string:mail>/<string:password>")
api.add_resource(driverTakeCargo, "/driverTakeCargo/<string:mail>/<string:password>/<string:cargoID>/<string:NodeID>")
api.add_resource(driverDropCargo, "/driverDropCargo/<string:mail>/<string:password>/<string:cargoID>/<string:NodeID>")

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
