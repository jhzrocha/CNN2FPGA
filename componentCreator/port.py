
class port:
    name = ''
    dataType = ''
    connection = ''

    def __init__(self, name, dataType, connection = ''):
        self.name = name
        self.dataType = dataType
        self.connection = connection
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setdataType(self,dataType):
        self.dataType = dataType
    
    def getdataType(self):
        return self.dataType

    def setConnection(self, connection):
        self.connection = connection
    
    def getConnection(self):
        return self.getConnection