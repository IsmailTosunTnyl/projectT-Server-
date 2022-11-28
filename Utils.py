
class Node:
    def __init__(self, ID,nodeName,latitude,longitude) -> None:
        self.ID = ID
        self.nodeName = nodeName
        self.cordinates = (float(latitude),float(longitude))
        self.latitude = latitude
        self.longitude = longitude