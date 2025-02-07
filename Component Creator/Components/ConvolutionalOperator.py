from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.io_buffer import IOBuffer
from Components.nucleoConvolucional import NucleoConvolucional
from Components.registrador import Registrador
from Components.genericMultiplexer import Multiplexer
from Components.add import Add
from Components.registrador import Registrador
from Components.demux_1x import Demux_1x
from Components.oneHotEncoder import OneHotEncoder
from Components.counter import Counter
from ComponentBases.type import Type
from Components.genericDemultiplexer import GenericDemultiplexer
#    Não testado
class ConvolutionalOperator(ComponentCommonMethods):

    # C : integer := 3;  -- iFMAP Chanels (filter Chanels also) qtChanels
    # R : integer := 3; -- filter Height 
    # S : integer := 3; -- filter Width     
    # M : integer := 6; -- Number of filters (oFMAP Chanels also)  qtFilters
    #NC_ADDRESS_WIDTH weightShiftAddrWidth
    #NC_OHE_WIDTH  oneHotEncoderWidthInput
    #DATA_WIDTH = dataWidth
    #ADDR_WIDTH = addrWidths
    #OUT_SEL_WIDTH = outputDataWidthSelBuffers
    #BIAS_ADDRESS_WIDTH biasAddressWidth

    def __init__(self,qtBlocks=3,qtRows=3, qtColumns=3, qtPixelsPerRow=3,qtChanels=3, qtFilters=3, weightShiftAddrWidth=5, 
                 oneHotEncoderWidthInput = 18, dataWidth =8, dataWidthNC = 32, addrWidths=10, outputDataWidthSelBuffers = 3, biasAddressWidth=5):
        
        self.qtBlocks = qtBlocks
        self.qtRows = qtRows
        self.qtColumns = qtColumns
        self.qtPixelsPerRow = qtPixelsPerRow
        self.qtFilters= qtFilters
        self.weightShiftAddrWidth=weightShiftAddrWidth
        self.oneHotEncoderWidthInput = oneHotEncoderWidthInput
        self.qtChanels = qtChanels        
        self.dataWidth = dataWidth
        self.dataWidthNC = dataWidthNC
        self.addrWidths = addrWidths
        self.outputDataWidthSelBuffers = outputDataWidthSelBuffers
        self.biasAddressWidth = biasAddressWidth

        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'ConvolutionalOperator_{self.qtBlocks}b_{self.qtRows}r_{self.qtColumns}c_{self.qtPixelsPerRow}ppr_{self.qtChanels}c_{self.qtFilters}f_{self.weightShiftAddrWidth}wsa_{self.oneHotEncoderWidthInput}ohe_{self.dataWidth}dw_{self.dataWidthNC}dwn_{self.addrWidths}adw_{self.outputDataWidthSelBuffers}odwsb_{self.biasAddressWidth}baw'

        #Adicionado antes das portas pelo tamanho de i_NC_O_SEL depender do tamanho de portas
        multiplexer = Multiplexer(qtInputs=4, dataWidth=self.dataWidthNC)
        self.convolutionalCoreSelectionWidth = multiplexer.selectionWidth
        self.addInternalComponent(component=multiplexer ,
                                  componentCallName='MUXX',
                                  portmap={ 'i_A'  : 'w_o_NC',
                                            'i_SEL': 'i_NC_O_SEL',
                                            'o_Q'  : 'w_o_MUX_NC(0)'})
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_inData',declaration=f"array(0 to {self.qtChanels-1}) of std_logic_vector({self.dataWidth-1} downto 0)"))
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_outData',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector({self.dataWidth-1} downto 0)"))

        self.demux = GenericDemultiplexer(selWidth=self.outputDataWidthSelBuffers, 
                                          dataWidth = self.dataWidthNC)
        self.addInternalComponent(component= self.demux,
                            componentCallName='u_DEMUX',
                            portmap={
                            'i_A'  : 'w_o_CAST',
                            'i_SEL'  : 'i_OUT_SEL',
                            'o_Q'  : 'w_DEMUX_OUT'
                            })

        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_IN_READ_ENA','std_logic'),
                                Port('i_IN_DATA',f'{self.minimalComponentFileName}_inData'),
                                Port('i_IN_WRITE_ENA','std_logic'),
                                Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                Port('i_IN_READ_ADDR0',f'std_logic_vector ({self.addrWidths-1}  downto 0)'),
                                Port('i_IN_READ_ADDR1',f'std_logic_vector ({self.addrWidths-1} downto 0)'),
                                Port('i_IN_READ_ADDR2',f'std_logic_vector ({self.addrWidths-1} downto 0)'),
                                Port('i_IN_WRITE_ADDR',f'std_logic_vector ({self.addrWidths-1} downto 0)'),
                                Port('i_WEIGHT','std_logic_vector(7 downto 0)'),
                                Port('i_BIAS','std_logic_vector (31 downto 0)'),
                                Port('i_BIAS_WRITE_ENA','std_logic'),
                                Port('i_SCALE_WRITE_ENA','std_logic'),
                                Port('i_PIX_SHIFT_ENA','std_logic'),
                                Port('i_WEIGHT_SHIFT_ENA','std_logic'),
                                Port('i_WEIGHT_SHIFT_ADDR',f'std_logic_vector({self.weightShiftAddrWidth-1} downto 0)'),
                                Port('i_WEIGHT_ROW_SEL','std_logic_vector(1 downto 0)'),
                                Port('i_NC_O_SEL', multiplexer.getPortDataType('i_SEL')),
                                Port('i_ACC_ENA','std_logic'),
                                Port('i_ACC_RST','std_logic'),
                                Port('i_ROW_SEL','std_logic_vector(1 downto 0)'),
                                Port('i_OUT_SEL',dataType=f'std_logic_vector({self.outputDataWidthSelBuffers-1} downto 0)', initialValue="(others => '0')"),
                                Port('i_OUT_WRITE_ENA','std_logic'),
                                Port('i_OUT_READ_ENA','std_logic'),
                                Port('i_OUT_READ_ADDR','std_logic_vector (9 downto 0)', initialValue="(others => '0')"),
                                Port('i_OUT_INC_ADDR','std_logic'),
                                Port('i_OUT_CLR_ADDR','std_logic')
                                ],
                            'out': [
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                   ] 
                    }
        
        self.defineTypeOnTypePackage(Type(name=f't_ARRAY_OF_INTEGER',declaration=f"array (integer range <>) of integer"))
        self.addGenericByParameters(name='SCALE_SHIFT',dataType='t_ARRAY_OF_INTEGER', initialValue='')
        self.addInternalSignalWire(name='w_NC_PES_ADDR',dataType=f'std_logic_vector ({self.oneHotEncoderWidthInput-1} downto 0)')
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_NC',declaration=f"array(0 to {2**self.convolutionalCoreSelectionWidth-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_NC',dataType=multiplexer.getPortDataType('i_A'),initialValue="(others => (others => '0'))")
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_MUX_NC',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_MUX_NC',dataType=f'{self.minimalComponentFileName}_w_o_MUX_NC')
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_ADD',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_ADD',dataType=f'{self.minimalComponentFileName}_w_o_ADD',initialValue="(others => (others => '0'))")

        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_BIAS_ACC',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_BIAS_ACC',dataType=f'{self.minimalComponentFileName}_w_o_BIAS_ACC',initialValue="(others => (others => '0'))")

        self.addInternalSignalWire(name='r_OUT_ADDR',dataType=f'std_logic_vector({self.addrWidths-1} downto 0)',initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_RST_OUT_ADDR',dataType='std_logic', initialValue="'0'")
        self.addInternalSignalWire(name='w_CONFIG0',dataType='std_logic')
        self.addInternalSignalWire(name='w_CONFIG1',dataType='std_logic')
        self.addInternalSignalWire(name='w_BIAS_REG_ENA',dataType=f'std_logic_vector({self.qtFilters-1} downto 0)')
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_BIAS_REG',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_BIAS_REG',dataType=f'{self.minimalComponentFileName}_w_o_BIAS_REG')
        
        self.addInternalSignalWire(name='w_BIAS_WRITE_ENA',dataType='std_logic')
        self.addInternalSignalWire(name='w_SCALE_WRITE_ENA',dataType='std_logic')
        self.addInternalSignalWire(name='w_SCALE_REG_ENA',dataType=f'std_logic_vector({self.qtFilters-1} downto 0)')
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_o_SCALE_REG',declaration=f"array(0 to {self.qtFilters-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_o_SCALE_REG',dataType=f'{self.minimalComponentFileName}_w_o_SCALE_REG')
        
        self.addInternalSignalWire(name='w_ADD_OUT',dataType='STD_LOGIC_VECTOR(31  downto 0)')
        self.addInternalSignalWire(name='w_o_SCALE_DOWN',dataType="std_logic_vector(63 downto 0)",initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_o_CAST',dataType="std_logic_vector(31 downto 0)",initialValue="(others => '0')")
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_DEMUX_OUT',declaration=f"array(0 to {2**self.outputDataWidthSelBuffers-1}) of std_logic_vector(31 downto 0)"))
        self.addInternalSignalWire(name='w_DEMUX_OUT',dataType=self.demux.getPortDataType('o_Q'),initialValue="(others => (others => '0'))")
        
        self.addInternalSignalWire(name='w_OUT_ADDR_ENA',dataType=f"std_logic_vector({self.qtFilters-1} downto 0)",initialValue="(others => '0')")
        

        self.internalOperations = """
        w_CONFIG0 <= '1' when (i_ROW_SEL = "00") else '0';
        w_CONFIG1 <= '1' when (i_ROW_SEL = "01") else '0';        
        """

        self.generateChanels(self.qtChanels, self.qtBlocks,self.qtRows, self.qtColumns, self.qtPixelsPerRow)
        self.addComponents()
        self.generateFilterOut(self.qtFilters)
        self.addOneHotEncodersAndCounter(self.qtFilters,self.qtChanels)
        self.OutputEntityAndArchitectureFile()



    def generateChanels(self, qtChanels, qtBlocks,qtRows, qtColumns, qtPixelsPerRow):
        
        self.defineTypeOnTypePackage(Type(name=f'{self.minimalComponentFileName}_w_MUX_I_VET',declaration=f"array(0 to {2**self.convolutionalCoreSelectionWidth-1}) of std_logic_vector(31 downto 0)"))
        for i in range(0,qtChanels-1):
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_1_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_2_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_3_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")

            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_1_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")
            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_2_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")
            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_3_{i}",dataType=f"STD_LOGIC_VECTOR ({self.dataWidth-1} downto 0)")

            self.addInternalSignalWire(name=f"w_o_PIX_{i}",dataType="STD_LOGIC_VECTOR (31 downto 0)", initialValue="(others => '0')")

            self.addInternalSignalWire(name=f"w_WEIGHT_SHIFT_ENABLE_{i}",dataType="std_logic", initialValue="'0'")

            self.addInternalSignalWire(name=f"w_MUX_I_VET_{i}",dataType=f'{self.minimalComponentFileName}_w_MUX_I_VET', initialValue="(others => (others => '0'))")

            self.addInternalComponent(component=IOBuffer(qtBlocks=qtBlocks,
                                               dataWidth=self.dataWidth,
                                               addrWidth=self.addrWidths),
                                               componentCallName=f"io_buffer_{i}",
                                               portmap= {'i_CLK'        :   'i_CLK',
                                                         'i_CLR'        :   'i_CLR',
                                                         'i_DATA'       :   f"i_IN_DATA({i})",
                                                         'i_READ_ENA'   :   'i_IN_READ_ENA',
                                                         'i_WRITE_ENA'  :   'i_IN_WRITE_ENA',
                                                         'i_SEL_LINE'   :   'i_IN_SEL_LINE',
                                                         'i_READ_ADDR_0' :   'i_IN_READ_ADDR0',
                                                         'i_READ_ADDR_1' :   'i_IN_READ_ADDR1',
                                                         'i_READ_ADDR_2' :   'i_IN_READ_ADDR2',
                                                         'i_WRITE_ADDR' :   'i_IN_WRITE_ADDR',
                                                         'o_DATA_ROW_0' :   f"w_RAM_PIX_ROW_1_{i}",
                                                         'o_DATA_ROW_1' :   f"w_RAM_PIX_ROW_2_{i}",
                                                         'o_DATA_ROW_2' :   f"w_RAM_PIX_ROW_3_{i}"})

            self.addInternalOperationLine(f'''     
                w_NC_PIX_ROW_1_{i} <= w_RAM_PIX_ROW_1_{i} when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_2_{i} when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_3_{i};
                w_NC_PIX_ROW_2_{i} <= w_RAM_PIX_ROW_2_{i} when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_3_{i} when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_1_{i};
                w_NC_PIX_ROW_3_{i} <= w_RAM_PIX_ROW_3_{i} when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_1_{i} when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_2_{i};''')
            
            self.addInternalOperationLine(f'w_WEIGHT_SHIFT_ENABLE_{i} <= w_NC_PES_ADDR({i}) AND i_WEIGHT_SHIFT_ENA;')

            self.addInternalComponent(component=NucleoConvolucional(qtRows=qtRows, 
                                                                    qtColumns=qtColumns,
                                                                    qtPixelsPerRow=qtPixelsPerRow, 
                                                                    outputDataWidth=self.dataWidthNC), 
                                      componentCallName=f'NCX_{i}',
                                      portmap={'i_CLK'               :'i_CLK',
                                               'i_CLR'               :'i_CLR',
                                               'i_PIX_SHIFT_ENA'     :'i_PIX_SHIFT_ENA',
                                               'i_WEIGHT_SHIFT_ENA'  :f'w_WEIGHT_SHIFT_ENABLE_{i}',
                                               'i_PIX_ROW_0'         :f'w_NC_PIX_ROW_1_{i}',
                                               'i_PIX_ROW_1'         :f'w_NC_PIX_ROW_2_{i}',
                                               'i_PIX_ROW_2'         :f'w_NC_PIX_ROW_3_{i}',
                                               'i_WEIGHT_ROW_SEL'    :'i_WEIGHT_ROW_SEL',
                                               'i_WEIGHT'            :'i_WEIGHT',
                                               'o_PIX'               : f"w_o_PIX_{i}"})

            self.addInternalComponent(component=Registrador(self.dataWidthNC), 
                                      componentCallName=f'registrador_{i}',
                                      portmap={'i_CLK':'i_CLK',
                                               'i_CLR':'i_CLR',
                                               'i_ENA':"'1'",
                                               'i_A'  :f"w_o_PIX_{i}",
                                               'o_Q'  :f'w_o_NC({i})'}
                                      )

    def addComponents(self):
        self.addInternalComponent(component= Add(qt_bits=self.dataWidthNC),
                                  componentCallName='ADDX',
                                  portmap={ 'a'     :'w_o_ADD(0)',
                                            'b'     :'w_o_MUX_NC(0)',
                                            'cin'   :"'0'",
                                            'sum1'  :'w_ADD_OUT'})

        self.addInternalComponent(component=Registrador(self.dataWidthNC),
                                  componentCallName='REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_ACC_RST',
                                            'i_ENA': 'i_ACC_ENA',
                                            'i_A'  : 'w_ADD_OUT',          
                                            'o_Q'  : 'w_o_ADD(0)'})
        
        self.addInternalOperationLine('w_BIAS_WRITE_ENA <= i_BIAS_WRITE_ENA;')
        
        self.addInternalComponent(component=Registrador(self.dataWidthNC),
                                  componentCallName='BIAS_REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_CLR',
                                            'i_ENA': 'w_BIAS_WRITE_ENA',
                                            'i_A'  : 'i_BIAS',          
                                            'o_Q'  : 'w_o_BIAS_REG(0)'})

        self.addInternalOperationLine('w_SCALE_WRITE_ENA <= i_SCALE_WRITE_ENA;')

        self.addInternalComponent(component=Registrador(self.dataWidthNC),
                                  componentCallName='SCALE_REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_CLR',
                                            'i_ENA': 'w_SCALE_WRITE_ENA',
                                            'i_A'  : 'i_BIAS',          
                                            'o_Q'  : 'w_o_SCALE_REG(0)'} 
                                  )
        
        self.addInternalOperationLine('w_o_BIAS_ACC(0) <= std_logic_vector(unsigned(w_o_ADD(0)) + unsigned(w_o_BIAS_REG(0)));')
        self.addInternalOperationLine(f"w_o_SCALE_DOWN <= (others => '0') when (w_o_BIAS_ACC(0)(31) = '1') else std_logic_vector(unsigned(w_o_BIAS_ACC(0)) * unsigned(w_o_SCALE_REG(0)));")
        self.addInternalOperationLine(f'w_o_CAST({self.dataWidthNC-1} downto 0) <= w_o_SCALE_DOWN({self.dataWidthNC*2-1}  downto {self.dataWidthNC} );')


    
    def generateFilterOut(self,qtFilters):
        for i in range(0,qtFilters-1):
            self.addInternalSignalWire(name=f"w_255_CLIP_{i}",dataType="std_logic_vector (7 downto 0)")
            self.addInternalSignalWire(name=f"w_OUT_WRITE_ENA_{i}",dataType="std_logic")
            self.addInternalSignalWire(name=f"w_GTHAN_255_{i}",dataType="std_logic")
            
            self.addInternalOperationLine(f"w_GTHAN_255_{i} <= '1' when (w_o_CAST(31 downto SCALE_SHIFT({i})) > std_logic_vector(to_unsigned(255, 32))) else '0';")
            self.addInternalOperationLine(f'w_255_CLIP_{i} <= "11111111" when (w_GTHAN_255_{i} = ' +  f"'1') else w_DEMUX_OUT({i})(SCALE_SHIFT({i})+7 downto SCALE_SHIFT({i}));")
            self.addInternalOperationLine(f"w_OUT_WRITE_ENA_{i} <= '1' when (i_OUT_WRITE_ENA = '1' and w_OUT_ADDR_ENA({i}) = '1') else '0';")

            IOBufferportmap = {'i_CLK':'i_CLK',
                               'i_DATA':f'w_255_CLIP_{i}',
                               'i_WRITE_ENA':f'w_OUT_WRITE_ENA_{i}',
                               'i_SEL_LINE':'"0"',
                               'i_READ_ADDR_0':'i_OUT_READ_ADDR',
                               'i_READ_ADDR_1':'i_OUT_READ_ADDR',
                               'i_READ_ADDR_2':'i_OUT_READ_ADDR',
                               'i_WRITE_ADDR':'r_OUT_ADDR',
                               'o_DATA_ROW_0':f'o_OUT_DATA({i})'}
            
            self.addInternalComponent(IOBuffer(qtBlocks=1,
                                               dataWidth= self.dataWidth,
                                                addrWidth=self.addrWidths),
                                      f"OUT_BUFFER_{i}",
                                      IOBufferportmap)



    def addOneHotEncodersAndCounter(self,qtFilters,qtChanels):
        self.addInternalComponent(component=OneHotEncoder(inputDataWidth=self.weightShiftAddrWidth,
                                                          outputDataWidth=self.oneHotEncoderWidthInput),
                                  componentCallName='u_OHE_PES',
                                  portmap={'i_DATA':'i_WEIGHT_SHIFT_ADDR',
                                           'o_DATA':'w_NC_PES_ADDR'})
        
        self.addInternalComponent(component=OneHotEncoder(inputDataWidth=self.outputDataWidthSelBuffers,
                                                          outputDataWidth=qtFilters),
                                  componentCallName='u_OHE_OUT_BUFF',
                                  portmap={'i_DATA':'i_OUT_SEL',
                                           'o_DATA':'w_OUT_ADDR_ENA'})
        
        self.addInternalOperationLine(f"w_RST_OUT_ADDR <= '1' when (i_CLR = '1' or i_OUT_CLR_ADDR = '1') else '0';")
        self.addInternalComponent(component=Counter(dataWidth=self.addrWidths, bitStep=1),
                                  componentCallName='u_OUT_ADDR',
                                  portmap={'i_CLK':'i_CLK',
                                             'i_RESET':'w_RST_OUT_ADDR',
                                             'i_INC':'i_OUT_INC_ADDR',
                                             'i_RESET_VAL':"(others => '0')",
                                             'o_Q':'r_OUT_ADDR'})