from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Demux_1x(ComponentCommonMethods):

   #Testado
    def __init__(self, qtOutputs, inputDataWidth = 8):
        self.startInstance()
        self.minimalComponentFileName = f"demux1x{qtOutputs}_{inputDataWidth}b"
        self.selectionWidth = len(self.integerToBinary(qtOutputs))
        self.portMap =   { 'in': [
                                Port('i_A',f"std_logic_vector({inputDataWidth-1} DOWNTO 0)"),
                                Port('i_SEL',f"std_logic_vector ({self.getOptionLength()-1} DOWNTO 0)")
                                ],
                            'out': []
                    }
        self.addMultipleGeneratedOutputPorts(qtOutputs,f"std_logic_vector({inputDataWidth-1} DOWNTO 0)")
        self.internalOperations = f"""
{self.setInternalOperations()}
        """
        self.OutputEntityAndArchitectureFile()

    def integerToBinary(self, integer):
        return bin(integer)[2:]

    def setInternalOperations(self):
        cont = 0
        internalOperation = ''
        for outputPort in self.portMap['out']:
            internalOperation = internalOperation + '        {} <= i_A when (i_SEL ="{}") else (others => '.format(outputPort.name,self.integerToBinary(cont).zfill(self.selectionWidth) ) + " '0');\n"
            cont = cont + 1
        return internalOperation
    
    def getIntegerInBinaryOption(self, integer):
        return self.integerToBinary(integer).zfill(self.selectionWidth)

    def getOptionLength(self):
        return len(self.integerToBinary(0).zfill(self.selectionWidth))