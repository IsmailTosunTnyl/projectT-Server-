from flask import Flask
from flask_restful import Api, Resource
from DataBase import DB

app = Flask(__name__)
api = Api(app)
db = DB()

# decorator for checking login


def login_required(f):
    def decorated_function(*args, **kwargs):
        user = db.logIn(kwargs['mail'], kwargs['password'])
        if user:
            return f(*args, **kwargs)
        else:
            return {'error': 'login failed'}, 500
    return decorated_function

# User SignUp


class Signup(Resource):
    def get(self):
        return {"data": ""}

    def post(self, firstname, lastname, password, email, address, phone, nationalID):
        print("Sigup Post: ", firstname, lastname, email,
              password, address, phone, nationalID)
        try:
            db.signUp(nationalID, email, password, firstname,
                      lastname, phone, address, 0, 0)
            return {"ok":{'succesfuly sign up':201}}, 201
        except Exception as e:
            return {"error":'User Exist'}, 500
        
        

# User Login


class Login(Resource):
    def get(self, id):
        return {"data": ""}

    def post(self, username, password):
        try:
            res = db.login(username, password)
            if res:
                return "ok", 200
            else:
                return "error", 500  # check if user exist in db
        except:
            return "error", 404


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
    def post(self, mail,password, OwnerID, ReceiverID, Type, Weight, Volume, NodeID, Status):
        Value = 6060 # this is a test value for price of cargo
        #calculate price of cargo

        try:
            db.cargoAdd(OwnerID, ReceiverID, Type, Weight,
                        Volume, NodeID, Status, Value)
            return {"ok":{"Cargo added":201}}, 201
        except Exception as e:
            return {"error",str(e)}, 500


class CargooListAll(Resource):
    @login_required
    def get(self,mail,password):
        res = db.listAllCargo()
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
            res = db.listAllNodes()
            if res[1]:
                return {'node': res[1]}, 200
            else:
                return "error", 500  # check if node exist in db
        except Exception as e:
            return e, 404


api.add_resource(Signup, "/signup/<string:firstname>/<string:lastname>/<string:password>/<string:email>/<string:address>/<string:phone>/<string:nationalID>")
api.add_resource(Login, "/login/<string:username>/<string:password>")
api.add_resource(Cargoo, "/cargoadd/<string:mail>/<string:password>/<string:OwnerID>/<string:ReceiverID>/<string:Type>/<string:Weight>/<string:Volume>/<string:NodeID>/<string:Status>")
api.add_resource(CargooListAll, "/cargoall/<string:mail>/<string:password>")
api.add_resource(NodeList, "/nodeall/<string:mail>/<string:password>")


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)