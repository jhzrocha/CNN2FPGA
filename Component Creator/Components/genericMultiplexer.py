from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.type import Type

class Multiplexer(ComponentCommonMethods):
   
    def __init__(self, dataWidth=8, qtInputs = 64):
        self.dataWidth = dataWidth
        self.qtInputs = qtInputs
        self.createComponent()
    
    
    def createComponent(self):
        self.startInstance()
        self.minimalComponentFileName = f"Multiplexer_{self.qtInputs}_{self.dataWidth}b"
        self.selectionWidth = len(self.integerToBinary(self.qtInputs))-1
        self.defineTypeOnTypePackage(Type(f't_ARRAY_OF_LOGIC_VECTOR_mult{self.qtInputs}',f'std_logic_vector({self.dataWidth-1} downto 0)', self.qtInputs))
        self.portMap =   { 'in': [
                                Port('i_A',f'array (0 to {self.qtInputs-1}) of std_logic_vector({self.dataWidth-1} downto 0)', initialValue="(others => (others => '0'))"),
                                Port('i_SEL',f"std_logic_vector({self.selectionWidth-1} DOWNTO 0)",initialValue="(others => '0')")
                                ],
                            'out': [ Port('o_Q',f"std_logic_vector({self.dataWidth-1} DOWNTO 0)")]
                    }
        self.addInternalSignalWire(name='w_INDEX',dataType='integer',initialValue=0)
        self.internalOperations = f"""
            w_INDEX <= to_integer(unsigned(i_SEL));
            o_Q <= i_A(w_INDEX);
        """
        self.OutputEntityAndArchitectureFile()

    def integerToBinary(self, integer):
        return bin(integer)[2:]

