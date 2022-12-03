import mysql.connector
from dotenv import load_dotenv
import os
from collections import defaultdict
from Utils import *
from functools import cache

load_dotenv()


class DB():

    def __init__(self):
        self.mydb = mysql.connector.connect(user=os.getenv('dbUser'), password=os.getenv('dbPassword'),
                                    host=os.getenv('dbHost'),
                                    database=os.getenv('dbDatabase'))

    def signUp(self, NationalId, Mail, Password, Name, LastName, Phone, Adress, Balance, Star):
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO tblUser (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (NationalId, Mail, Password, Name,
               LastName, Phone, Adress, Balance, Star)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def logIn(self, Mail, Password):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "select * from tblUser where Mail=%s and Password=%s"
        val = (Mail, Password)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result[0]
        else:
            return False

    def cargoAdd(self, OwnerID, ReceiverID, Type, Weight, Volume, NodeID,DestNodeID, Status, Value):
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO tblCargo (OwnerID,ReceiverID,Type,Weight,Volume,NodeID,destNodeID,Status,Value) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s, %s)"
        val = (OwnerID, ReceiverID, Type, Weight,
               Volume, NodeID, DestNodeID, Status, Value)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def listAllCargo(self):

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT ID,Type,Weight,Volume,Value FROM tblCargo where Status='startbox'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result

    def listDriverCargo(self, DriverID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Weight,Volume,Value FROM tblCargo where DriverID=%s and Status!='done'"
        val = (DriverID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False

    def listOwnerCargo(self, OwnerID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Weight,Volume,Value FROM tblCargo where OwnerID=%s and Status!='done'"
        val = (OwnerID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result

    def listReceiverCargo(self, ReceiverID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT Type,Weight,Volume,Value FROM tblCargo where ReceiverID=%s and Status!='done'"
        val = (ReceiverID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        if result:
            return result
        else:
            return False

    def listAllNodes(self):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblNode"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        nodes = []
        for node in result:
            nodes.append(Node(node['ID'], node['nodeName'],
                         node['latitude'], node['longitude']))

        return (nodes, result)

    @cache
    def listCargosinNodes(self, nodeID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where Status='startbox' and NodeID=%s"
        val = (nodeID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result

    @cache
    def searchNodeByID_tpl(self,nodeID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblNode where ID=%s"
        val = (nodeID,)
        self.mycursor.execute(sql,val)
        result = self.mycursor.fetchall()
        return result[0]
        
    @cache
    def searchNodeByID(self,nodeID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblNode where ID=%s"
        val = (nodeID,)
        self.mycursor.execute(sql,val)
        result = self.mycursor.fetchall()
        return Node(result[0]['ID'],result[0]['nodeName'],result[0]['latitude'],result[0]['longitude'])
    
    def searchCargobySourceIDandDestinationID(self, SourceID, DestinationID):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where NodeID=%s and destNodeID=%s"
        val = (SourceID, DestinationID)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
        return result

    
    def checkNodes(self,NodeID):
        """check if node is in database Node itself use this function"""

        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM nodeControl WHERE NodeID = %s", (NodeID,))
        myresult = mycursor.fetchall()
        return myresult

    def updateNodeandBox(self,NodeID,BoxID,BoxStatus):
        mycursor = self.mydb.cursor()
        sql = "UPDATE nodeControl SET BoxStatus = %s WHERE NodeID = %s and BoxID = %s"
        val = (BoxStatus,NodeID,BoxID)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def searchUserbyEmail(self, Mail):
        """Search user by email"""

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblUser where Mail=%s"
        val = (Mail,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result[0]

    def getCargoByID(self, ID):
        """Get cargo by ID"""

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where ID=%s"
        val = (ID,)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result[0]

    def getEmptyBoxes(self, NodeID):
        """" Returns the number of empty boxes in a node """

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblBoxes where NodeID=%s and BoxStatus=%s"
        val = (NodeID,0)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result

    def updateCargoBox(self, CargoID, BoxID):
        """Update cargo box"""

        self.mycursor = self.mydb.cursor()
        sql = "UPDATE tblCargo SET BoxID = %s WHERE ID = %s"
        val = (BoxID, CargoID)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def updateBoxStatus(self,BoxID,BoxStatus):
        """Update box status"""

        self.mycursor = self.mydb.cursor()
        sql = "UPDATE tblBoxes SET BoxStatus = %s WHERE ID = %s"
        val = (BoxStatus,BoxID)
        self.mycursor.execute(sql, val)
        self.mydb.commit()



if __name__=="__main__":
    db = DB()
    #print(db.listAllCargo())
    #print(db.listDriverCargo("2"))
    #print(db.listOwnerCargo("1"))
    #print(db.listReceiverCargo("3"))
    #db.cargoAdd(22,22,'food',35,3535,2,'startbox',1000)
    #print(len(db.listCargosinNodes(2)))
    #print(db.searchNodeByID_tpl(2))
    #print(db.searchCargobySourceIDandDestinationID(2,11))
    #db.updateNode(1,1,0)
    #print(db.searchUserbyEmail("mail60")['ID'])
    #print(db.getCargoByID(26))
    print(db.getEmptyBoxes(5))

