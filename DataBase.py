import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
class DB():

    def __init__(self):
        self.mydb = mysql.connector.connect(user=os.getenv('dbUser'), password=os.getenv('dbPassword'),
                                    host=os.getenv('dbHost'),
                                    database=os.getenv('dbDatabase'))
        

        self.mycursor = self.mydb.cursor()

    def signUp(self,NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star):
        
        sql = "INSERT INTO tblUser (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def logIn(self,Mail,Password):
        sql = "select * from tblUser where Mail=%s and Password=%s"
        val = (Mail,Password)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result[0]
        else:
            return False

    def cargoAdd(self,OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price):
        sql = "INSERT INTO tblCargo (OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo,Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (OwnerID,DriverID,ReceiverID,Type,KG,Volume,NodeID,Status,DateCargo)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def listAllCargo(self):
        sql = "SELECT (Type,Kg,Volume,Price) FROM tblCargo where Status=startbox"
        self.mycursor.execute(sql)
    
    def listDriveCargo(self,DriverID):
        sql = "SELECT (Type,Kg,Volume,Price) FROM tblCargo where DriverID=%s Status<>done"
        val = (DriverID)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False
    
    def listOwnerCargo(self,OwnerID):
        sql = "SELECT (Type,Kg,Volume,Price) FROM tblCargo where OwnerID=%s Status<>done"
        val = (OwnerID)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False

    def listReceiverCargo(self,ReceiverID):
        sql = "SELECT (Type,Kg,Volume,Price) FROM tblCargo where ReceiverID=%s and Status<>done"
        val = (ReceiverID)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False