from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from MemoryInitializationComponents.memoryInitializationComponent import MemoryInitializationComponent
from Components.ConvolutionalControl import ConvolutionalControl
from Components.ConvolutionalOperator import ConvolutionalOperator


class ConvolutionalLayer(ComponentCommonMethods):
    
    
    # DATA_WIDTH - dataWidth
    #ADDR_WIDTH  addrWidth
    #H  imageHeight
    #W  imageWidth
    #C  channels
    #R   filterHeight                  
    #S   filterWidth                  
    #M   quantityFilters
    #NUM_WEIGHT_FILTER_CHA qtFiltersPerChannel
    #LAST_WEIGHT   lastWeight
    #LAST_BIAS  lastBias
    #LAST_ROW   lastRow           
    #LAST_COL  lastColumn
    #NC_SEL_WIDTH    ncSelectionWidth
    #NC_ADDRESS_WIDTH     ncAddressWidth
    #NC_OHE_WIDTH     ncOheWidth
    #BIAS_OHE_WIDTH        
    #WEIGHT_ADDRESS_WIDTH  weightAdressWidth
    #BIAS_ADDRESS_WIDTH    biasAdressWidth
    #SCALE_SHIFT      scaleShift     
    #WEIGHT_FILE_NAME    weightsFileName  
    #BIAS_FILE_NAME     biasFileName   
    #OUT_SEL_WIDTH      outSelectionWidth   
    #USE_REGISTER      useRegister    
    
    
    def __init__(self, dataWidth=8, addrWidth = 10, imageHeight = 34, imageWidth=26, channels=3, filterHeight=3, filterWidth=3, quantityFilters=6, qtFiltersPerChannel='"1000"',
                 lastWeight = '"10100010"', lastBias='"1100"', lastRow = '"100010"', lastColumn = '"11010"', ncSelectionWidth=2, ncAddressWidth=55, ncOheWidth =18, weightAdressWidth=10, biasAdressWidth=6,
                 scaleShift = [8, 8, 7, 8, 8, 9], weightsFileName='weights.txt', biasFileName='bias.txt', outSelectionWidth = 3,useRegister = 0):
        self.dataWidth = dataWidth
        self.addrWidth = addrWidth
        self.imageHeight = imageHeight
        self.imageWidth = imageWidth
        self.channels = channels
        self.filterHeight = filterHeight
        self.filterWidth = filterWidth
        self.quantityFilters = quantityFilters
        self.qtFiltersPerChannel = qtFiltersPerChannel
        self.lastWeight = lastWeight
        self.lastBias = lastBias
        self.lastRow = lastRow
        self.lastColumn = lastColumn
        self.ncSelectionWidth = ncSelectionWidth
        self.ncAddressWidth = ncAddressWidth
        self.ncOheWidth = ncOheWidth
        self.weightAdressWidth = weightAdressWidth
        self.biasAdressWidth = biasAdressWidth
        self.scaleShift = scaleShift
        self.weightsFileName = weightsFileName
        self.biasFileName = biasFileName
        self.outSelectionWidth = outSelectionWidth
        self.useRegister = useRegister
        self.createComponent()
    

    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'ConvolutionalLayer'
        self.portMap =   { 'in': [
                                Port(f'i_CLK', 'std_logic'),
                                Port(f'i_CLR', 'std_logic'),
                                Port(f'i_IN_DATA', f'array (0 to {self.channels-1}) of std_logic_vector({self.dataWidth-1} downto 0)'),
                                Port(f'i_IN_WRITE_ENA', 'std_logic'),
                                Port(f'i_IN_SEL_LINE', 'std_logic_vector (1 downto 0)'),
                                Port(f'i_IN_READ_ADDR0', f'std_logic_vector ({self.addrWidth-1} downto 0)'),
                                Port(f'i_IN_READ_ADDR1', f'std_logic_vector ({self.addrWidth-1} downto 0)'),
                                Port(f'i_IN_READ_ADDR2', f'std_logic_vector ({self.addrWidth-1}downto 0)'),
                                Port(f'i_IN_WRITE_ADDR', f'std_logic_vector ({self.addrWidth-1} downto 0)'),
                                Port(f'i_WEIGHT', 'std_logic_vector(7 downto 0)'),
                                Port(f'i_BIAS', 'std_logic_vector (31 downto 0)'),
                                Port(f'i_BIAS_WRITE_ENA', 'std_logic'),
                                Port(f'i_SCALE_WRITE_ENA', 'std_logic'),
                                Port(f'i_PIX_SHIFT_ENA', 'std_logic'),
                                Port(f'i_WEIGHT_SHIFT_ENA', 'std_logic'),
                                Port(f'i_WEIGHT_SHIFT_ADDR', f'std_logic_vector({self.ncAddressWidth-1} downto 0)'),
                                Port(f'i_WEIGHT_ROW_SEL', 'std_logic_vector(1 downto 0)'),
                                Port(f'i_NC_O_SEL', f'std_logic_vector({self.ncSelectionWidth-1} downto 0)'),
                                Port(f'i_ACC_ENA', 'std_logic'),
                                Port(f'i_ACC_RST', 'std_logic'),
                                Port(f'i_ROW_SEL', 'std_logic_vector(1 downto 0)'),
                                Port(f'i_OUT_SEL', f"std_logic_vector({self.outSelectionWidth} downto 0) := (others => '0')"),
                                Port(f'i_OUT_WRITE_ENA', 'std_logic'),
                                Port(f'i_OUT_READ_ADDR', "std_logic_vector (9 downto 0) := (others => '0')"),
                                Port(f'i_OUT_INC_ADDR', 'std_logic'),
                                Port(f'i_OUT_CLR_ADDR', 'std_logic')
                                ],
                            'out': [
                                Port('o_OUT_DATA', f'array (0 to {self.quantityFilters-1}) of std_logic_vector({self.dataWidth-1} downto 0)')
                                   ] 
                    }
        
        self.addInternalSignalWire('w_IN_READ_ADDR0', dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)')
        self.addInternalSignalWire('w_IN_READ_ADDR1', dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)')
        self.addInternalSignalWire('w_IN_READ_ADDR2', dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)')
        self.addInternalSignalWire('w_WEIGHT_READ_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_WEIGHT_READ_ADDR', dataType=f'std_logic_vector ({self.weightAdressWidth-1} downto 0)')
        self.addInternalSignalWire('w_i_WEIGHT', dataType=f'std_logic_vector ({self.dataWidth} downto 0)')
        self.addInternalSignalWire('w_BIAS_READ_ADDR', dataType=f'std_logic_vector ({self.biasAdressWidth-1} downto 0)')
        self.addInternalSignalWire('w_BIAS_READ_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_BIAS_WRITE_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_SCALE_WRITE_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_BIAS', dataType='std_logic_vector (31 downto 0)')
        self.addInternalSignalWire('w_PIX_SHIFT_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_WEIGHT_SHIFT_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_NC_ADDR', dataType=f'std_logic_vector ({self.ncAddressWidth-1} downto 0)')
        self.addInternalSignalWire('w_WEIGHT_ROW_SEL', dataType='std_logic_vector (1 downto 0)')
        self.addInternalSignalWire('w_NC_O_SEL', dataType=f'std_logic_vector ({self.ncSelectionWidth-1} downto 0)')
        self.addInternalSignalWire('w_ACC_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_ACC_RST', dataType='std_logic')
        self.addInternalSignalWire('w_ROW_SEL', dataType='std_logic_vector (1 downto 0)')
        self.addInternalSignalWire('w_OUT_SEL', dataType=f'std_logic_vector ({self.outSelectionWidth-1} downto 0)')
        self.addInternalSignalWire('w_OUT_WRITE_ENA', dataType='std_logic')
        self.addInternalSignalWire('w_OUT_INC_ADDR', dataType='std_logic')
        self.addInternalSignalWire('w_OUT_CLR_ADDR', dataType='std_logic')


        self.addInternalComponent(component=MemoryInitializationComponent(type='conv_weights',
                                                                          initFileName= self.weightsFileName,
                                                                         dataWidth=8,
                                                                         dataDepth=self.weightAdressWidth),
                                    componentCallName='u_ROM_WEIGHTS',
                                    portmap={'address':'w_WEIGHT_READ_ADDR',
                                             'clock':'i_CLK',
                                             'rden':"'1'",
                                             'q':'w_ROM_OUT'})
        
        self.addInternalComponent(component=MemoryInitializationComponent(type='conv_bias',
                                                                          initFileName= self.biasFileName,
                                                                         dataWidth=32,
                                                                         dataDepth=self.biasAdressWidth),
                                    componentCallName='u_ROM_BIAS',
                                    portmap={'address':'w_BIAS_READ_ADDR',
                                             'clken':"'1'",
                                             'clock':"i_CLK",
                                             'q':'w_BIAS_SCALE'})
        
        self.addInternalComponent(component= ConvolutionalControl(addWidth=self.addrWidth,
                                                                  ncAddrWidth=self.ncAddressWidth,
                                                                  ncSelWidth=self.ncSelectionWidth, 
                                                                  ifMapWidth=self.imageWidth, 
                                                                  lengthWeightAddress=self.qtFiltersPerChannel, 
                                                                  lengthBiasAddress=self.biasAdressWidth, 
                                                                  outSelWidthBuffers=self.outSelectionWidth, 
                                                                  qtFiltersPerChannel= self.qtFiltersPerChannel, 
                                                                  qtWeights= self.lastWeight, 
                                                                  qtBias=self.lastBias, 
                                                                  qtRows= self.lastRow, 
                                                                  qtCols= self.lastColumn, 
                                                                  qtChannels=self.channels, 
                                                                  qtFilters=self.quantityFilters),
                                  componentCallName='u_CONTROLE',
                                  portmap={
                                        "i_CLK": "i_CLK",
                                        "i_CLR": "i_CLR",
                                        "i_GO": "i_GO",
                                        "o_READY": "o_READY",
                                        "o_IN_READ_ADDR0": "w_IN_READ_ADDR0",
                                        "o_IN_READ_ADDR1": "w_IN_READ_ADDR1",
                                        "o_IN_READ_ADDR2": "w_IN_READ_ADDR2",
                                        "o_WEIGHT_READ_ENA": "w_WEIGHT_READ_ENA",
                                        "o_WEIGHT_READ_ADDR": "w_WEIGHT_READ_ADDR",
                                        "o_BIAS_READ_ADDR": "w_BIAS_READ_ADDR",
                                        "o_BIAS_READ_ENA": "w_BIAS_READ_ENA",
                                        "o_BIAS_WRITE_ENA": "w_BIAS_WRITE_ENA",
                                        "o_SCALE_WRITE_ENA": "w_SCALE_WRITE_ENA",
                                        "o_PIX_SHIFT_ENA": "w_PIX_SHIFT_ENA",
                                        "o_WEIGHT_SHIFT_ENA": "w_WEIGHT_SHIFT_ENA",
                                        "o_NC_ADDR": "w_NC_ADDR",
                                        "o_WEIGHT_ROW_SEL": "w_WEIGHT_ROW_SEL",
                                        "o_NC_O_SEL": "w_NC_O_SEL",
                                        "o_ACC_ENA": "w_ACC_ENA",
                                        "o_ACC_RST": "w_ACC_RST",
                                        "o_ROW_SEL": "w_ROW_SEL",
                                        "o_OUT_SEL": "w_OUT_SEL",
                                        "o_OUT_WRITE_ENA": "w_OUT_WRITE_ENA",
                                        "o_OUT_INC_ADDR": "w_OUT_INC_ADDR",
                                        "o_OUT_CLR_ADDR": "w_OUT_CLR_ADDR",
                                    })

    # DATA_WIDTH - dataWidth
    #ADDR_WIDTH  addrWidth
    #H  imageHeight
    #W  imageWidth
    #C  channels
    #R   filterHeight                  
    #S   filterWidth                  
    #M   quantityFilters
    #NUM_WEIGHT_FILTER_CHA qtFiltersPerChannel
    #LAST_WEIGHT   lastWeight
    #LAST_BIAS  lastBias
    #LAST_ROW   lastRow           
    #LAST_COL  lastColumn
    #NC_SEL_WIDTH    ncSelectionWidth
    #NC_ADDRESS_WIDTH     ncAddressWidth
    #NC_OHE_WIDTH     ncOheWidth
    #BIAS_OHE_WIDTH        
    #WEIGHT_ADDRESS_WIDTH  weightAdressWidth
    #BIAS_ADDRESS_WIDTH    biasAdressWidth
    #SCALE_SHIFT      scaleShift     
    #WEIGHT_FILE_NAME    weightsFileName  
    #BIAS_FILE_NAME     biasFileName   
    #OUT_SEL_WIDTH      outSelectionWidth   
    #USE_REGISTER      useRegister            
        self.addInternalComponent(component= ConvolutionalOperator(qtBlocks=self.qtFiltersPerChannel,
                                                                   qtRows=self.imageHeight, 
                                                                   qtColumns=self.imageWidth, 
                                                                   qtPixelsPerRow=self.s,
                                                                   qtChanels=self.channels, 
                                                                   qtFilters=self.quantityFilters, 
                                                                   weightShiftAddrWidth= self.weightAdressWidth,
                                                                   oneHotEncoderWidthInput = self.ncOheWidth, 
                                                                   dataWidth =self.dataWidth, 
                                                                   dataWidthNC = self.ncOheWidth, 
                                                                   addrWidths=self.addrWidth, 
                                                                   outputDataWidthSelBuffers = self.outSelectionWidth, 
                                                                   biasAddressWidth=self.biasAdressWidth),
                                componentCallName='u_OPERACIONAL',
                                portmap={
                                    "i_CLK": "i_CLK",
                                    "i_CLR": "i_CLR",
                                    "i_IN_DATA": "i_IN_DATA",  # dado buffer entrada
                                    "i_IN_WRITE_ENA": "i_IN_WRITE_ENA",  # escrita buffer entrada
                                    "i_IN_SEL_LINE": "i_IN_SEL_LINE",  # linha buffer entrada
                                    "i_IN_READ_ADDR0": "w_IN_READ_ADDR0",
                                    "i_IN_READ_ADDR1": "w_IN_READ_ADDR1",
                                    "i_IN_READ_ADDR2": "w_IN_READ_ADDR2",
                                    "i_WEIGHT": "w_i_WEIGHT",
                                    "i_BIAS": "w_BIAS",
                                    "i_BIAS_WRITE_ENA": "w_BIAS_WRITE_ENA",
                                    "i_SCALE_WRITE_ENA": "w_SCALE_WRITE_ENA",
                                    "i_WEIGHT_SHIFT_ADDR": "w_NC_ADDR",
                                    "i_WEIGHT_ROW_SEL": "w_WEIGHT_ROW_SEL",
                                    "i_IN_WRITE_ADDR": "i_IN_WRITE_ADDR",  # endereco escrita buffer entrada
                                    "i_PIX_SHIFT_ENA": "w_PIX_SHIFT_ENA",
                                    "i_WEIGHT_SHIFT_ENA": "w_WEIGHT_SHIFT_ENA",
                                    "i_NC_O_SEL": "w_NC_O_SEL",
                                    "i_ACC_ENA": "w_ACC_ENA",
                                    "i_ACC_RST": "w_ACC_RST",
                                    "i_ROW_SEL": "w_ROW_SEL",
                                    "i_OUT_SEL": "w_OUT_SEL",
                                    "i_OUT_WRITE_ENA": "w_OUT_WRITE_ENA",
                                    "i_OUT_READ_ADDR": "i_OUT_READ_ADDR",  # endereco leitura buffer saida
                                    "i_OUT_INC_ADDR": "w_OUT_INC_ADDR",
                                    "i_OUT_CLR_ADDR": "w_OUT_CLR_ADDR",
                                    "o_OUT_DATA": "o_OUT_DATA",  # dado buffer saída
                                })
        self.internalOperations = """

        """
        self.OutputEntityAndArchitectureFile()



