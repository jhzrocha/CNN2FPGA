from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic

class Multiplexer(ComponentCommonMethods):

    
    def __init__(self, qtOptions):
        self.minimalComponentFileName = f"Multiplexer_{qtOptions}"
        self.portMap =   { 'in': [
                                Port('i_DATA','signed(0 to p_QT_BITS-1)'),
                                Port('i_KERNEL','signed(0 to p_QT_BITS-1)'),
                                Port('i_ENA','std_logic')
                            ],
                        'out': [Port('o_VALUE','integer')] 
                    }
        

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
        super().__init__()
        self.addInternalSignalWire('w_O_VALUE', 'integer', 0)

        self.generics = [Generic('p_QT_BITS','natural','p_QT_BITS')]
        self.OutputEntityAndArchitectureFile()
