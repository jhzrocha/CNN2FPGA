from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic

class Multiplicator(ComponentCommonMethods):

    
    def __init__(self, qtBits = 8):
        self.minimalComponentFileName = f'multiplicator_{qtBits}b'
        self.portMap =   { 'in': [
                                Port('i_DATA',f'signed(0 to {qtBits-1})'),
                                Port('i_KERNEL',f'signed(0 to {qtBits-1})'),
                                Port('i_ENA','std_logic')
                            ],
                        'out': [Port('o_VALUE','integer')] 
                    }
        self.addInternalSignalWire(name='w_O_VALUE', 
                                   dataType='integer', 
                                   initialValue=0)
        
        self.internalOperations = """
            multi:
            process(i_DATA,i_KERNEL,i_ENA)
            
            begin
                if (i_ENA= '1') then
                    w_O_VALUE <= TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL))); 
                end if;
            end process multi;
            o_VALUE <= w_O_VALUE;
        """

        self.OutputEntityAndArchitectureFile()

