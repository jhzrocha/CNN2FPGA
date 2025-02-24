from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

    #Compilado
    #Testado
class Relu(ComponentCommonMethods):

    def __init__(self, dataWidth = 8):
        self.startInstance()
        self.minimalComponentFileName = f"Relu_{dataWidth}dw"
        self.portMap =   { 'in': [
                                Port('i_PIX',f"STD_LOGIC_VECTOR ({dataWidth-1} downto 0)")
                                ],
                            'out': [ Port('o_PIX',f"STD_LOGIC_VECTOR ({dataWidth-1} downto 0)")]
                    }
        self.internalOperations = f"""
            o_PIX <= (others => '0') when (i_PIX({dataWidth} - 1) = '1') else i_PIX;
        """
        self.OutputEntityAndArchitectureFile()