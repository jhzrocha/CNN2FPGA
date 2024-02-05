
class Wire:
    name = ''
    dataType = ''
    initialValue = ''

    def __init__(self, name, dataType, initialValue = ''):
        self.name = name
        self.dataType = dataType
        self.initialValue = initialValue
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setdataType(self,dataType):
        self.dataType = dataType
    
    def getdataType(self):
        return self.dataType
    
