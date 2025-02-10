from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic

class Switcher(ComponentCommonMethods):

    
    def __init__(self, qtOptions):
        self.qtOptions = qtOptions
        self.minimalComponentFileName = f"Switcher_{qtOptions}"
        self.portMap =   { 'in': [Port('i_OPTION',f"unsigned(0 to {self.getQtBitsInputOption()}-1)"),
                                  Port('i_ENA','std_logic'),
                                  Port('i_VALUE','integer')],
                        'out': [] 
                    }
        

        self.internalOperations = """
            switch:
            process (i_ENA)
            begin
                if (i_ENA = '1') then
                    {}
                end if;
            end process switch;
{}
        """
        self.setInternalOperations()
        self.addMultipleGeneratedOutputPorts(qtOptions, 'integer')
       
        super().__init__()

        self.addMultipleInternalSignalWires(qtOptions, {'name':'w_VALUE' ,
                                                        'dataType': 'integer',
                                                        'initialValue': 0})
        
        self.OutputEntityAndArchitectureFile()
    

    def getIntegerInBinary(self, integer):
        return '{0:b}'.format(integer)
    
    def getQtBitsInputOption(self):
        return len(self.getIntegerInBinary(self.qtOptions))
        
    def setInternalOperations(self):
        self.internalOperations = self.internalOperations.format(self.getInternalConditions(),self.getInternalWireConnections())

    def getInternalWireConnections(self):
        internalConnection = ''
        for i in range(self.qtOptions):
            internalConnection = internalConnection + f"            o_PORT_{i} <= w_VALUE_{i}; \n"

        return internalConnection

    def getInternalConditions(self):
        condition = f'''if (i_OPTION = {self.getIntegerInBinary(0).zfill(self.getQtBitsInputOption())}) then
                        w_VALUE_0 <=  i_VALUE;\n  '''
        if self.qtOptions > 1 :
            for i in range(1, self.qtOptions):
                condition = condition + f'''            elsif (i_OPTION = {self.getIntegerInBinary(i).zfill(self.getQtBitsInputOption())}) then
                    w_VALUE_{i} <=  i_VALUE;\n  '''
            condition = condition + 'end if;'
        else:
            condition = condition + '                    end if;'
        return condition
            
    def getInternalConditions(self):
        condition = 'case i_OPTION is\n'
        
        for i in range(0, self.qtOptions):
            condition = condition + f'''                  when "{self.getIntegerInBinary(i).zfill(self.getQtBitsInputOption())}" =>
                    w_VALUE_{i} <= i_VALUE;\n'''            
        
        condition = condition + '''                  when others => 
                      null;
                end case;'''
        
        return condition
            