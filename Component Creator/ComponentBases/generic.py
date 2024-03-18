
class Generic:

    name = ''
    dataType = ''
    initialValue = ''

    def __init__(self, name, dataType, initialValue, value =None):
        self.name = name
        self.dataType = dataType
        self.initialValue = initialValue
        if(value):
            self.value = value
        else:
            self.value = self.initialValue

    def getDeclaration(self):
        return f"{self.name} : {self.dataType} := {self.value};\n"
        
    