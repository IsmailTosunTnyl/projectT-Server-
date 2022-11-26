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
    def get(self):
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
        return {"data": ""}
    
    def post(self,ownerID,):
        




api.add_resource(Signup, "/signup/<string:firstname>/<string:lastname>/<string:password>/<string:email>/<string:address>/<string:phone>/<string:nationalID>")
api.add_resource(Login, "/login/<string:username>/<string:password>")




if __name__ == "__main__":
    app.run("0.0.0.0",port=80,debug=True)