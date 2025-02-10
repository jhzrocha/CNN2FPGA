
class Constant:
    name = ''
    dataType = ''
    value = ''

    def __init__(self, name, dataType, value = ''):
        self.name = name
        self.dataType = dataType
        self.value = value
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setdataType(self,dataType):
        self.dataType = dataType
    
    def getdataType(self):
        return self.dataType
    
    def getConstantDeclaration(self):
        return f"constant {self.name} : {self.dataType} := {self.value};\n"
    
