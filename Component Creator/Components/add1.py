from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Add1(ComponentCommonMethods):

    
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = 'add1'
        self.portMap =   { 'in': [
                                Port('a','std_logic'),
                                Port('b','std_logic'),
                                Port('cin','std_logic')
                            ],
                            'out': [Port('sum','std_logic'),
                                    Port('cout','std_logic')] 
                    }
        
        self.addInternalSignalWire('w_A_XOR_B ', 'std_logic')
        self.internalOperations = """
            w_A_XOR_B <= (a xor b);
                
            -- resultado
            sum <= w_A_XOR_B xor cin;   
            -- carry out
            cout <= (a and b) or (w_A_XOR_B and cin);
        """
        self.OutputEntityAndArchitectureFile()

