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

class Conv1Op(ComponentCommonMethods):

#    Não testado

    # H : integer := 32; -- iFMAP Height 
    # W : integer := 24; -- iFMAP Width 
    # C : integer := 3;  -- iFMAP Chanels (filter Chanels also) qtChanels
    # R : integer := 3; -- filter Height 
    # S : integer := 3; -- filter Width     
    # M : integer := 6; -- Number of filters (oFMAP Chanels also)  qtFilters
    def __init__(self, qtChanels, qtBlocks,qtRows, qtColumns, qtPixelsPerRow,qtFilters=3):
        self.startInstance()
        self.minimalComponentFileName = 'conv1_op'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_IN_READ_ENA','std_logic'),
                                Port('i_IN_DATA',f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChanels-1})(DATA_WIDTH-1 downto 0)'),
                                Port('i_IN_WRITE_ENA','std_logic'),
                                Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                Port('i_IN_READ_ADDR0','std_logic_vector (ADDR_WIDTH - 1 downto 0)'),
                                Port('i_IN_READ_ADDR1','std_logic_vector (ADDR_WIDTH - 1 downto 0)'),
                                Port('i_IN_READ_ADDR2','std_logic_vector (ADDR_WIDTH - 1 downto 0)'),
                                Port('i_IN_WRITE_ADDR','std_logic_vector (ADDR_WIDTH - 1 downto 0)'),
                                Port('i_WEIGHT','std_logic_vector(7 downto 0)'),
                                Port('i_BIAS_WRITE_ADDR','STD_LOGIC_VECTOR (BIAS_ADDRESS_WIDTH-1 DOWNTO 0)'),
                                Port('i_BIAS','std_logic_vector (31 downto 0)'),
                                Port('i_BIAS_WRITE_ENA','std_logic'),
                                Port('i_SCALE_WRITE_ENA','std_logic'),
                                Port('i_PIX_SHIFT_ENA','std_logic'),
                                Port('i_WEIGHT_SHIFT_ENA','std_logic'),
                                Port('i_WEIGHT_SHIFT_ADDR','std_logic_vector(NC_ADDRESS_WIDTH-1 downto 0)'),
                                Port('i_WEIGHT_ROW_SEL','std_logic_vector(1 downto 0)'),
                                Port('i_NC_O_SEL','std_logic_vector(NC_SEL_WIDTH - 1 DOWNTO 0)'),
                                Port('i_ACC_ENA','std_logic'),
                                Port('i_ACC_RST','std_logic'),
                                Port('i_ROW_SEL','std_logic_vector(1 downto 0)'),
                                Port('i_OUT_SEL','std_logic_vector(OUT_SEL_WIDTH-1 downto 0)', initialValue="(others => '0'"),
                                Port('i_OUT_WRITE_ENA','std_logic'),
                                Port('i_OUT_READ_ENA','std_logic'),
                                Port('i_OUT_READ_ADDR','std_logic_vector (9 downto 0)', initialValue="(others => '0')"),
                                Port('i_OUT_INC_ADDR','std_logic'),
                                Port('i_OUT_CLR_ADDR','std_logic')
                                ],
                            'out': [
                                    Port('o_OUT_DATA',f"t_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(DATA_WIDTH-1 downto 0)"),
                                   ] 
                    }
        self.addGenericByParameters('H','integer',32)
        self.addGenericByParameters('W','integer',24)
        self.addGenericByParameters('C','integer',3)
        self.addGenericByParameters('R','integer',3)
        self.addGenericByParameters('S','integer',3)
        self.addGenericByParameters('M','integer',3)
        self.addGenericByParameters('NC_SEL_WIDTH','integer',2)
        self.addGenericByParameters('NC_ADDRESS_WIDTH','integer',5)
        self.addGenericByParameters('NC_OHE_WIDTH','integer',18)
        self.addGenericByParameters('BIAS_OHE_WIDTH','integer',12)
        self.addGenericByParameters('WEIGHT_ADDRESS_WIDTH','integer',8)
        self.addGenericByParameters('BIAS_ADDRESS_WIDTH','integer',5)
        self.addGenericByParameters('DATA_WIDTH','integer',8)
        self.addGenericByParameters('ADDR_WIDTH','integer',10)
        self.addGenericByParameters('OUT_SEL_WIDTH','integer',3)
        self.addGenericByParameters('SCALE_SHIFT','t_ARRAY_OF_INTEGER','')

        self.addInternalSignalWire(name='w_NC_PES_ADDR',dataType='std_logic_vector (NC_OHE_WIDTH - 1 downto 0)')
        self.addInternalSignalWire(name='w_BIAS_SCALE_ADDR',dataType='std_logic_vector (BIAS_OHE_WIDTH-1 downto 0)')
        self.addInternalSignalWire(name='w_o_NC',dataType='t_ARRAY_OF_LOGIC_VECTOR(0 to (2**NC_SEL_WIDTH - 1))(31 downto 0)',initialValue="(others => (others => '0')")
        self.addInternalSignalWire(name='w_o_MUX_NC',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(31 downto 0)')
        self.addInternalSignalWire(name='w_o_ADD',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(31 downto 0)',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_o_BIAS_ACC',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(31 downto 0)',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='r_OUT_ADDR',dataType='std_logic_vector(ADDR_WIDTH-1 downto 0)',initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_RST_OUT_ADDR',dataType='std_logic')
        self.addInternalSignalWire(name='w_CONFIG0',dataType='std_logic')
        self.addInternalSignalWire(name='w_CONFIG1',dataType='std_logic')
        self.addInternalSignalWire(name='w_BIAS_REG_ENA',dataType=f'std_logic_vector({qtFilters-1} downto 0)')
        self.addInternalSignalWire(name='w_o_BIAS_REG',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(31 downto 0)')
        self.addInternalSignalWire(name='w_BIAS_WRITE_ENA',dataType='std_logic')
        self.addInternalSignalWire(name='w_SCALE_WRITE_ENA',dataType='std_logic')
        self.addInternalSignalWire(name='w_SCALE_REG_ENA',dataType=f'std_logic_vector({qtFilters-1} downto 0)')
        self.addInternalSignalWire(name='w_o_SCALE_REG',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtFilters-1})(31 downto 0)')
        self.addInternalSignalWire(name='w_ADD_OUT',dataType='STD_LOGIC_VECTOR(31  downto 0)')
        self.addInternalSignalWire(name='w_o_SCALE_DOWN',dataType="std_logic_vector(63 downto 0)",initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_o_CAST',dataType="std_logic_vector(31 downto 0)",initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_DEMUX_OUT',dataType="t_ARRAY_OF_LOGIC_VECTOR(0 to (2**OUT_SEL_WIDTH-1))(31 downto 0)",initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_OUT_ADDR_ENA',dataType=f"std_logic_vector({qtFilters-1} downto 0)",initialValue="(others => '0')")
        

        self.internalOperations = """
        w_CONFIG0 <= '1' when (i_ROW_SEL = "00") else '0';
        w_CONFIG1 <= '1' when (i_ROW_SEL = "01") else '0';        
        """

        self.generateChanels(qtChanels, qtBlocks,qtRows, qtColumns, qtPixelsPerRow)
        self.addComponents()
        self.generateFilterOut(qtFilters)
        self.addOneHotEncodersAndCounter(qtFilters,qtChanels)
        self.OutputEntityAndArchitectureFile()



    def generateChanels(self, qtChanels, qtBlocks,qtRows, qtColumns, qtPixelsPerRow):
        for i in range(0,qtChanels-1):
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_1_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_2_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")
            self.addInternalSignalWire(name=f"w_RAM_PIX_ROW_3_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")

            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_1_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")
            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_2_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")
            self.addInternalSignalWire(name=f"w_NC_PIX_ROW_3_{i}",dataType="STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0)")

            self.addInternalSignalWire(name=f"w_o_PIX_{i}",dataType="STD_LOGIC_VECTOR (31 downto 0)", initialValue="(others => '0')")

            self.addInternalSignalWire(name=f"w_WEIGHT_SHIFT_ENABLE_{i}",dataType="std_logic", initialValue="'0'")

            self.addInternalSignalWire(name=f"w_MUX_I_VET_{i}",dataType="t_ARRAY_OF_LOGIC_VECTOR(0 to (2**NC_SEL_WIDTH)-1)(31 downto 0)", initialValue="(others => (others => '0'))")

            IOBufferportmap = {'i_CLK'        :'i_CLK',
                                'i_CLR'        :'i_CLR',
                                'i_DATA'       :f"i_IN_DATA({i})",
                                'i_READ_ENA'   :'i_IN_READ_ENA',
                                'i_WRITE_ENA'  :'i_IN_WRITE_ENA',
                                'i_READ_ADDR0' :'i_IN_READ_ADDR0',
                                'i_READ_ADDR1' :'i_IN_READ_ADDR1',
                                'i_READ_ADDR2' :'i_IN_READ_ADDR2',
                                'i_WRITE_ADDR' :'i_IN_WRITE_ADDR',
                                'o_DATA_ROW_0' :f"w_RAM_PIX_ROW_1_{i}",
                                'o_DATA_ROW_1' :f"w_RAM_PIX_ROW_2_{i}",
                                'o_DATA_ROW_2' :f"w_RAM_PIX_ROW_3_{i}"}
            
            IOBufferGenerics = {'NUM_BLOCKS' : qtBlocks,
                                'DATA_WIDTH' : 'DATA_WIDTH',
                                'ADDR_WIDTH' : 'ADDR_WIDTH'}

            self.addInternalComponent(IOBuffer(),f"io_buffer_{i}",IOBufferportmap,IOBufferGenerics)

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

            nucleoConvolucionalPortmap =   {'i_CLK'               :'i_CLK',
                                            'i_CLR'               :'i_CLR',
                                            'i_PIX_SHIFT_ENA'     :'i_PIX_SHIFT_ENA',
                                            'i_WEIGHT_SHIFT_ENA'  :'w_WEIGHT_SHIFT_ENABLE',
                                            'i_PIX_ROW_1'         :f'w_NC_PIX_ROW_1_{i}',
                                            'i_PIX_ROW_2'         :f'w_NC_PIX_ROW_2_{i}',
                                            'i_PIX_ROW_3'         :f'w_NC_PIX_ROW_3_{i}',
                                            'i_WEIGHT_ROW_SEL'    :'i_WEIGHT_ROW_SEL',
                                            'i_WEIGHT'            :'i_WEIGHT',
                                            'o_PIX'               :'w_o_PIX'}
            
            self.addInternalComponent(NucleoConvolucional(qtRows, qtColumns, qtPixelsPerRow), f'NCX_{i}',nucleoConvolucionalPortmap)


            registradorPortmap = {'i_CLK':'i_CLK',
                                    'i_CLR':'i_CLR',
                                    'i_ENA':'1',
                                    'i_A'  :'w_o_PIX',
                                    'o_Q'  :f'w_o_NC({i})' }
            
            self.addInternalComponent(Registrador(), f'registrador_{i}',registradorPortmap,{'DATA_WIDTH':32})

    def addComponents(self):

        self.addInternalComponent(component= Multiplexer(4),
                                  componentCallName='MUXX',
                                  portmap={ 'i_A'  : 'w_o_NC',
                                            'i_SEL': 'i_NC_O_SEL',
                                            'o_Q'  : 'w_o_MUX_NC(0)'},
                                  generics={'NC_SEL_WIDTH':'NC_SEL_WIDTH',
                                            'DATA_WIDTH': 32})

        self.addInternalComponent(component= Add(qt_bits=32),
                                  componentCallName='ADDX',
                                  portmap={ 'a'     :'w_o_ADD(0)',
                                            'b'     :'w_o_MUX_NC(0)',
                                            'cin'   :'0',
                                            'sum1'  :'w_ADD_OUT'})

        self.addInternalComponent(component=Registrador(),
                                  componentCallName='REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_ACC_RST',
                                            'i_ENA': 'i_ACC_ENA',
                                            'i_A'  : 'w_ADD_OUT',          
                                            'o_Q'  : 'w_o_ADD(0)'}, 
                                  generics={'DATA_WIDTH':'32'})
        
        self.addInternalOperationLine('w_BIAS_WRITE_ENA <= i_BIAS_WRITE_ENA;')
        
        self.addInternalComponent(component=Registrador(),
                                  componentCallName='BIAS_REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_CLR',
                                            'i_ENA': 'w_BIAS_WRITE_ENA',
                                            'i_A'  : 'i_BIAS',          
                                            'o_Q'  : 'w_o_BIAS_REG(0)'}, 
                                  generics={'DATA_WIDTH':'32'})

        self.addInternalOperationLine('w_SCALE_WRITE_ENA <= i_SCALE_WRITE_ENA;')

        self.addInternalComponent(component=Registrador(),
                                  componentCallName='SCALE_REGX',
                                  portmap={ 'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_CLR',
                                            'i_ENA': 'w_SCALE_WRITE_ENA',
                                            'i_A'  : 'i_BIAS',          
                                            'o_Q'  : 'w_o_SCALE_REG(0)'}, 
                                  generics={'DATA_WIDTH':'32'})
        
        self.addInternalOperationLine('w_o_BIAS_ACC(0) <= w_o_ADD(0) + w_o_BIAS_REG(0);')
        self.addInternalOperationLine("w_o_SCALE_DOWN <= (others => '0') when (w_o_BIAS_ACC(0)(31) = '1') else w_o_BIAS_ACC(0) * w_o_SCALE_REG(0);")
        self.addInternalOperationLine('w_o_CAST(31 downto 0) <= w_o_SCALE_DOWN(63 downto 32);')

        self.addInternalComponent(component= Demux_1x(3),
                                  componentCallName='u_DEMUX',
                                  portmap={
                                    'i_A  '  : 'w_o_CAST',
                                    'i_SEL'  : 'i_OUT_SEL',
                                    'o_Q  '  : 'w_DEMUX_OUT'
                                  },
                                  generics={
                                     'i_WIDTH': 32
                                  })
    
    def generateFilterOut(self,qtFilters):
        for i in range(0,qtFilters-1):
            self.addInternalSignalWire(name=f"w_255_CLIP_{i}",dataType="std_logic_vector (7 downto 0)")
            self.addInternalSignalWire(name=f"w_OUT_WRITE_ENA_{i}",dataType="std_logic")
            self.addInternalSignalWire(name=f"w_GTHAN_255_{i}",dataType="std_logic")
            
            self.addInternalOperationLine(f"w_GTHAN_255_{i} <= '1' when (w_o_CAST(31 downto SCALE_SHIFT({i})) > std_logic_vector(to_unsigned(255, 32))) else '0';")
            self.addInternalOperationLine(f'w_255_CLIP_{i} <= "11111111" when (w_GTHAN_255_{i} = ' +  f"'1') else w_DEMUX_OUT({i})(SCALE_SHIFT({i})+7 downto SCALE_SHIFT({i}));")
            self.addInternalOperationLine(f"w_OUT_WRITE_ENA_{i} <= '1' when (i_OUT_WRITE_ENA_{i} = '1' and w_OUT_ADDR_ENA({i}) = '1') else '0';")

            IOBufferportmap = {'i_CLK':'i_CLK',
                               'i_CLR':'i_CLR',
                               'i_DATA':f'w_255_CLIP_{i}',
                               'i_READ_ENA':'i_OUT_READ_ENA',
                               'i_WRITE_ENA':f'w_OUT_WRITE_ENA_{i}',
                               'i_SEL_LINE':"00",
                               'i_READ_ADDR0':'i_OUT_READ_ADDR',
                               'i_READ_ADDR1':'i_OUT_READ_ADDR',
                               'i_READ_ADDR2':'i_OUT_READ_ADDR',
                               'i_WRITE_ADDR':'r_OUT_ADDR',
                               'o_DATA_ROW_0':f'o_OUT_DATA({i})'}
            
            IOBufferGenerics = {'NUM_BLOCKS' : 1,
                                'DATA_WIDTH' : 'DATA_WIDTH',
                                'ADDR_WIDTH' : 'ADDR_WIDTH'}

            self.addInternalComponent(IOBuffer(),f"OUT_BUFFER_{i}",IOBufferportmap,IOBufferGenerics)



    def addOneHotEncodersAndCounter(self,qtFilters,qtChanels):
        self.addInternalComponent(component=OneHotEncoder(),
                                  componentCallName='u_OHE_PES',
                                  portmap={'i_DATA':'i_WEIGHT_SHIFT_ADDR',
                                           'o_DATA':'w_NC_PES_ADDR'},
                                  generics={'DATA_WIDTH':'NC_ADDRESS_WIDTH',
                                            'OUT_WIDTH': qtChanels})
        self.addInternalComponent(component=OneHotEncoder(),
                                  componentCallName='u_OHE_OUT_BUFF',
                                  portmap={'i_DATA':'i_OUT_SEL',
                                           'o_DATA':'w_OUT_ADDR_ENA'},
                                   generics={'DATA_WIDTH':'OUT_SEL_WIDTH',
                                             'OUT_WIDTH': qtFilters})
        self.addInternalOperationLine(f"w_RST_OUT_ADDR <= '1' when (i_CLR = '1' or i_OUT_CLR_ADDR = '1') else '0'")
        self.addInternalComponent(component=Counter(),
                                  componentCallName='u_OUT_ADDR',
                                  portmap={'i_DATA':'i_OUT_SEL',
                                           'o_DATA':'w_OUT_ADDR_ENA'},
                                   generics={'i_CLK':'i_CLK',
                                             'i_RESET':'w_RST_OUT_ADDR',
                                             'i_INC':'i_OUT_INC_ADDR',
                                             'i_RESET_VAL':"(others => '0')",
                                             'o_Q':'r_OUT_ADDR'})