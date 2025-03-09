from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.registers import Registers
from Components.oneHotEncoder import OneHotEncoder
class RegisterFile(ComponentCommonMethods):
    
    def __init__(self, qtRegisters, dataWidth):
        self.qtRegisters = qtRegisters
        self.dataWidth = dataWidth
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'conv1_op_{self.qtBlocks}b_{self.qtRows}r_{self.qtColumns}c_{self.qtPixelsPerRow}ppr_{self.qtChanels}c_{self.qtFilters}f_{self.weightShiftAddrWidth}wsa_{self.oneHotEncoderWidthInput}ohe_{self.dataWidth}dw_{self.dataWidthNC}dwn_{self.addrWidths}adw_{self.outputDataWidthSelBuffers}odwsb_{self.biasAddressWidth}baw'
        
        self.oneHotEncoder = OneHotEncoder(outputDataWidth=self.qtRegisters)
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_A', f'std_logic_vector ({self.dataWidth-1} downto 0)'),
                                Port('i_ADDR_ENA', self.oneHotEncoder.getPortDataType('i_DATA'))
                                ],
                            'out': [
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                   ] 
                    }
        # self.addMultipleGeneratedInputPorts(qtPorts=self.qtRegisters,
        #                                     dataType=f'std_logic_vector ({self.dataWidth-1} downto 0)',
        #                                     name='i_A')
        

        self.addInternalSignalWire(name='w_REGISTERS_ENA_SEL',
                                      dataType=self.oneHotEncoder.getPortDataType('o_DATA'))
        
        self.addInternalSignalWire(name='w_REGISTERS_OUTPUT',
                                dataType= f'std_logic_vector({self.dataWidth -1} DOWNTO 0)')

        self.addInternalComponent(OneHotEncoder(outputDataWidth=self.qtRegisters),
                                  portmap={'i_DATA':'i_ADDR_ENA',
                                           'o_DATA':'w_REGISTERS_ENA_SEL'})
        self.addRegisters()
        self.internalOperations = """

        """
        self.OutputEntityAndArchitectureFile()


    def addRegisters(self):
        for i in range(0, self.qtRegisters):
            self.addInternalComponent(Registers(dataWidth=self.dataWidth),
                                      portmap={'i_CLK': 'i_CLK',
                                               'i_CLR': 'i_CLR',
                                               'i_ENA' : 'w_REGISTERS_ENA_SEL({i})',
                                               'i_A':f'i_A'})


