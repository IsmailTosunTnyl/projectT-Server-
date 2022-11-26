import mysql.connector

class DB():

    def __init__(self):
        self.mydb = mysql.connector.connect(user='root', password='3131',
                                    host='172.104.150.113',
                                    database='CargooDB'
        )

        self.mycursor = self.mydb.cursor()

    def signUp(self,NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star):
        
        sql = "INSERT INTO tblUser (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (NationalId,Mail,Password,Name,LastName,Phone,Adress,Balance,Star)
        self.mycursor.execute(sql, val)
        self.mydb.commit()