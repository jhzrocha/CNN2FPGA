
class Type:
    name = ''
    dataType = ''
    size = ''

    def __init__(self, name, dataType, size):
        self.name = name
        self.dataType = dataType
        self.size = size
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setdataType(self,dataType):
        self.dataType = dataType
    
    def getdataType(self):
        return self.dataType
    
    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def getDeclaration(self):
        return f"        type {self.name} is array({self.size-1} downto 0) of {self.dataType};\n"