
class Type:
    name = ''
    dataType = ''
    size = ''
    type = ''
    states = []
    def __init__(self, name, dataType='', size=0, type='array', states=[]):
        self.name = name
        self.dataType = dataType
        self.size = size
        self.type = type
        self.states = states
    
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
        if(self.type == 'array'):
            return f"        type {self.name} is array({self.size-1} downto 0) of {self.dataType};\n"

        if(self.type == 'state'):
            statesStrings = ''
            for state in self.states:
                statesStrings = statesStrings + f'          {state},\n'
            if statesStrings.endswith(',\n'):
                statesStrings = statesStrings[:-2]
            return f'''
        type {self.name} is (
{statesStrings}
        );\n'''