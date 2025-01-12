
class Port:
    name = ''
    dataType = ''
    connection = ''
    initialValue=''

    def __init__(self, name,dataType, connection = '', initialValue = ''):
        self.name = name
        self.dataType = dataType
        self.connection = connection
        self.initialValue = initialValue
    
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
    
    def __str__(self):
        return f'''
                name: {self.name}
                dataType: {self.dataType}
                connection: {self.connection}
                initialValue: {self.initialValue}'''
    