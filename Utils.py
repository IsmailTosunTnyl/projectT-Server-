from Crypto.Cipher import AES
import base64
from dotenv import load_dotenv
import os
load_dotenv()


class Node:
    def __init__(self, ID,nodeName,latitude,longitude) -> None:
        self.ID = ID
        self.nodeName = nodeName
        self.cordinates = (float(latitude),float(longitude))
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, __o: object) -> bool:
        return self.ID == __o.ID
    
    def __dict__(self):
        return {'ID':self.ID,'nodeName':self.nodeName,'latitude':self.latitude,'longitude':self.longitude}

class Encryptions:
    def __init__(self) -> None:
        self.key = os.getenv('ENCRYPTION_KEY')
        self.iv = os.getenv('ENCRYPTION_IV')

    def encrypt(self, data):
        return self.f.encrypt(data.encode())

    def decrypt(self, data):
        BS = 16
        def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        def unpad(s): return s[0:-(s[-1])]

        generator = AES.new(self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        data = base64.b64decode(data)
        recovery = generator.decrypt(data)

        return unpad(recovery).decode("utf8")

if __name__ == '__main__':
    print(Encryptions().decrypt("3I6pIcnsZobLkXctF+Glsg=="))