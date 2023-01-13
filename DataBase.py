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
        sql = "SELECT * FROM tblCargo where Status='startbox'"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
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

    def listOwnerCargo(self, OwnerID, Status):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where OwnerID=%s and Status = %s"
        val = (OwnerID,Status)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
        return result

    def listReceiverCargo(self, ReceiverID, Status):
        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where ReceiverID=%s and Status = %s"
        val = (ReceiverID,Status)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
        return result

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
        sql = "SELECT * FROM tblNode where ID=%s "
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
        sql = "SELECT * FROM tblCargo where NodeID=%s and destNodeID=%s and Status=%s and DriverID = 0"
        val = (SourceID, DestinationID,"startbox")
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
        
        return result

    
    def checkNodes(self,NodeID):
        """check if node is in database Node itself use this function"""

        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM nodeControl2 WHERE (NodeID = %s and (Status=%s or Status=%s or Status=%s or Status=%s))", (NodeID,'startbox','readyforDTS','readyfordrop','readyfordriver'))
        myresult1 = mycursor.fetchall()
        mycursor.execute("SELECT * FROM nodeControl2 WHERE destNodeID = %s and (Status=%s or Status=%s)", (NodeID,'endbox','transporting'))
        myresult2 = mycursor.fetchall()
        
        result = myresult1 + myresult2
        return result

    def updateNodeandBox(self,NodeID,BoxID,BoxStatus,isdestNode=False):
        if isdestNode:
            sql = "UPDATE nodeControl SET BoxStatus = %s WHERE destNodeID = %s and BoxID = %s"
        else:
            sql = "UPDATE nodeControl SET BoxStatus = %s WHERE NodeID = %s and BoxID = %s"
        print("updateNodeandBox")
        print('NodeID: ',NodeID,'BoxID: ',BoxID,'BoxStatus: ',BoxStatus)
        
        mycursor = self.mydb.cursor()
        val = (BoxStatus,NodeID,BoxID)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def updatedestNodeandBox(self,NodeID,BoxID,BoxStatus):
        mycursor = self.mydb.cursor()
        sql = "UPDATE nodeControl SET BoxStatus = %s WHERE destNodeID = %s and BoxID = %s"
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
        print('Cargo: ',result)
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

    def updateCargoStatus(self, CargoID, Status):
        """Update cargo status"""

        self.mycursor = self.mydb.cursor()
        sql = "UPDATE tblCargo SET Status = %s WHERE ID = %s"
        val = (Status, CargoID)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def updateDriverID(self, CargoID, DriverID):
        """Update driver ID"""

        self.mycursor = self.mydb.cursor()
        sql = "UPDATE tblCargo SET DriverID = %s WHERE ID = %s"
        val = (DriverID, CargoID)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def getCargobyReceiverID(self, ReceiverID):
        """Get cargo by receiver ID"""

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where ReceiverID=%s and Status=%s"
        val = (ReceiverID,"endbox")
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        return result
    
    def getCargobyDriverID(self, DriverID,status):
        """Get cargo by driver ID"""

        self.mycursor = self.mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tblCargo where DriverID=%s and Status=%s"
        val = (DriverID,status)
        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchall()
        for i in result:
            del i['DateCargo']
        print('Cargo: ',result)
        return result

 

if __name__=="__main__":
    db = DB()
    #print(db.listAllCargo())
    #print(db.listDriverCargo("2"))
    #print(db.listOwnerCargo("1"))
    #print(db.listReceiverCargo("3"))
    #db.cargoAdd(22,22,'food',35,3535,2,'startbox',1000)
    #print(len(db.listCargosinNodes(2)))
    #print(db.searchNodeByID_tpl(2))
    #print(db.searchCargobySourceIDandDestinationID(3,20))
    #db.updateNode(1,1,0)
    #print(db.searchUserbyEmail("mail60")['ID'])
    #print(db.getCargoByID(26))
    #print(db.getEmptyBoxes(5))
    #print(db.listOwnerCargo(72,"readyforDTS"),"readyforDTS")
    #print(db.checkNodes(3))
    #print(db.getCargobyDriverID(72,"transporting"))
    #print(db.updatedestNodeandBox(3,1,2))
    #print(db.searchUserbyEmail("mail60")['ID'])
    #print(db.searchUserbyEmail("mail60")['ID'])
    print(db.signUp(334324234,"mail@mailsss","3435eg","name","surname60",34534536,"address60",555,2))
    #NationalId, Mail, Password, Name, LastName, Phone, Adress, Balance, Star