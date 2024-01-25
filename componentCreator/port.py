
class Port:
    name = ''
    dataType = ''
    # type = ''
    connection = ''

    def __init__(self, name, 
                #  type, 
                 dataType, connection = ''):
        self.name = name
        # self.type = type
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
    
    # def setType(self,type):
    #     self.type = type
    
    # def getType(self):
    #     return self.type

    def setConnection(self, connection):
        self.connection = connection
    
    def getConnection(self):
        return self.getConnection