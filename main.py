from flask import Flask
from flask_restful import Api, Resource
from DataBase import DB

app = Flask(__name__)
api = Api(app)
db = DB()

# User SignUp
class Signup(Resource):
    def get(self):
        return {"data": ""}
    
    def post(self,firstname,lastname,password,email,address,phone,nationalID):
        print("Sigup Post: ",firstname,lastname,email,password,address,phone,nationalID)
        try:
            db.signUp(nationalID,email,password,firstname,lastname,phone,address,0,0)
            return "ok" , 201
        except:
            return "error" , 500

#User Login      
class Login(Resource):
    def get(self,id):
        return {"data": ""}
    
    def post(self,username,password):
        try:
            res = db.login(username,password)
            if res:
                return "ok" , 200
            else:
                return "error" , 500 #check if user exist in db
        except:
            return "error" , 404

class Cargoo(Resource):
    def get(self):
        try:
            res = db.listAllCargo()
            if res:
                return res, 200
            else:
                return "error" , 500 #check if user exist in db
        except:
            return "error" , 404
    
    def post(self,OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price):
        try:
            db.cargoAdd(OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price)
            return "ok" , 201
        except:
            return "error" , 500
        

class CargooListAll(Resource):
    def get(self):
        
            res = db.listAllCargo()
            if res:
                print(res)
                return res, 200
            else:
                print("error",res)
                return res , 500 #check if user exist in db

class NodeList(Resource):
    def get(self):
        try:
            res = db.listAllNodes()
            if res[1]:
                return res[1], 200
            else:
                return "error" , 500 #check if node exist in db
        except:
            return "error" , 404

       


api.add_resource(Signup, "/signup/<string:firstname>/<string:lastname>/<string:password>/<string:email>/<string:address>/<string:phone>/<string:nationalID>")
api.add_resource(Login, "/login/<string:username>/<string:password>")
api.add_resource(Cargoo, "/cargo/<string:OwnerID>/<string:DriverID>/<string:ReceiverID>/<string:Type>/<string:KG>/<string:Volume>/<string:NodeID>/<string:Status>/<string:DateCargo>/<string:Price>")
api.add_resource(CargooListAll, "/cargoall")
api.add_resource(NodeList, "/nodeall")



if __name__ == "__main__":
    app.run("0.0.0.0",port=80,debug=True)