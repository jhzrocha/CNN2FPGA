from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Relu(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = f"Relu"
        self.portMap =   { 'in': [
                                Port('i_PIX',f"STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")
                                ],
                            'out': [ Port('o_PIX',f"STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")]
                    }
        self.addGenericByParameters(name='DATA_WIDTH',dataType='integer',initialValue=8)
        self.internalOperations = f"""
            -- atribui 0 aos numeros negativos, identificados pelo oitavo bit em 1
            o_PIX <= i_PIX; -- "00000000" when (i_PIX(DATA_WIDTH - 1) = '1') else i_PIX;
        """
        self.OutputEntityAndArchitectureFile()