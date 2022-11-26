import mysql.connector
from dotenv import load_dotenv
import os
from collections import defaultdict
load_dotenv()
class DB():

    def __init__(self):
        self.mydb = mysql.connector.connect(user=os.getenv('dbUser'), password=os.getenv('dbPassword'),
                                    host=os.getenv('dbHost'),
                                    database=os.getenv('dbDatabase'))
        

        

    def signUp(self,NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star):
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO tblUser (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def logIn(self,Mail,Password):
        self.mycursor = self.mydb.cursor()
        sql = "select * from tblUser where Mail=%s and Password=%s"
        val = (Mail,Password)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result[0]
        else:
            return False

    def cargoAdd(self,OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price):
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO tblCargo (OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def listAllCargo(self):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Kg,Volume,Price FROM tblCargo where Status='startbox'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result
    
    def listDriverCargo(self,DriverID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Kg,Volume,Price FROM tblCargo where DriverID=%s and Status!='done'"
        val = (DriverID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False
    
    def listOwnerCargo(self,OwnerID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Kg,Volume,Price FROM tblCargo where OwnerID=%s and Status!='done'"
        val = (OwnerID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result

    def listReceiverCargo(self,ReceiverID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Kg,Volume,Price FROM tblCargo where ReceiverID=%s and Status!='done'"
        val = (ReceiverID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False


if __name__=="__main__":
   db = DB()
   print(db.listAllCargo())
   print(db.listDriverCargo("2"))
   print(db.listOwnerCargo("1"))
   print(db.listReceiverCargo("3"))
