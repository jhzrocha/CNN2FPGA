from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Multiplexer(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self, qtInputs):
        self.startInstance()
        self.minimalComponentFileName = f"Multiplexer_{qtInputs}"
        self.selectionWidth = len(self.integerToBinary(qtInputs))-1

        self.portMap =   { 'in': [
                                Port('i_A',f"t_ARRAY_OF_LOGIC_VECTOR(0 to (2**NC_SEL_WIDTH)-1)(DATA_WIDTH-1 downto 0)", initialValue="(others => (others => '0')"),
                                Port('i_SEL',f"std_logic_vector(NC_SEL_WIDTH - 1 DOWNTO 0)")
                                ],
                            'out': [ Port('o_Q',f"std_logic_vector(DATA_WIDTH-1 DOWNTO 0)")]
                    }
        self.addGenericByParameters(name='NC_SEL_WIDTH',dataType='integer',initialValue=self.selectionWidth)
        self.addGenericByParameters(name='DATA_WIDTH',dataType='integer',initialValue=32)
        self.addInternalSignalWire(name='w_INDEX',dataType='integer',initialValue=0)
        self.internalOperations = f"""
            w_INDEX <= to_integer(unsigned(i_SEL));
            o_Q <= i_A(w_INDEX);
        """
        self.OutputEntityAndArchitectureFile()

    def integerToBinary(self, integer):
        return bin(integer)[2:]

