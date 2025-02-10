from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Conv1Op(ComponentCommonMethods):
    def __init__(self):
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'conv1_op_{self.qtBlocks}b_{self.qtRows}r_{self.qtColumns}c_{self.qtPixelsPerRow}ppr_{self.qtChanels}c_{self.qtFilters}f_{self.weightShiftAddrWidth}wsa_{self.oneHotEncoderWidthInput}ohe_{self.dataWidth}dw_{self.dataWidthNC}dwn_{self.addrWidths}adw_{self.outputDataWidthSelBuffers}odwsb_{self.biasAddressWidth}baw'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),

                                ],
                            'out': [
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                   ] 
                    }
        
   
        self.internalOperations = """

        """
        self.OutputEntityAndArchitectureFile()



