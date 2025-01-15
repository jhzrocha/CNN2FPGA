from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.io_buffer import IOBuffer
from Components.maxPooling import MaxPooling
class PoolingOperator(ComponentCommonMethods):

    def __init__(self, dataWidth=8, addrWidth=10, qtChannels=6):
        self.dataWidth = dataWidth
        self.addrWidth = addrWidth
        self.qtChannels = qtChannels
        self.createComponent()
        
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = 'poolingController'
        self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                  Port('i_CLR','STD_LOGIC'),
                                  Port('i_PIX_SHIFT_ENA','STD_LOGIC'),
                                  Port('i_IN_DATA',f't_ARRAY_OF_LOGIC_VECTOR(0 to {self.qtChannels-1})({self.dataWidth-1} downto 0)'),
                                  Port('i_IN_READ_ENA','STD_LOGIC'),
                                  Port('i_IN_WRITE_ENA','STD_LOGIC'),
                                  Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_IN_READ_ADDR_0',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_READ_ADDR_1',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_READ_ADDR_2',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_WRITE_ADDR',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_READ_ENA','STD_LOGIC'),
                                  Port('i_OUT_WRITE_ENA','STD_LOGIC'),
                                  Port('i_OUT_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_OUT_READ_ADDR0',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_WRITE_ADDR',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')")],
                           'out': [Port('o_BUFFER_OUT',f't_ARRAY_OF_LOGIC_VECTOR(0 to {self.qtChannels-1})({self.dataWidth-1} downto 0)')] 
                         }
        
        self.addInternalSignalWire(name='w_PIX_ROW_1',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {self.qtChannels-1})({self.dataWidth-1} downto 0)',initialValue="(others => (others => '0')")
        self.addInternalSignalWire(name='w_PIX_ROW_2',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {self.qtChannels-1})({self.dataWidth-1} downto 0)',initialValue="(others => (others => '0')")
        self.addInternalSignalWire(name='w_o_PIX',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {self.qtChannels-1})({self.dataWidth-1} downto 0)',initialValue="(others => (others => '0')")
        self.setInternalComponents()
        self.internalOperations = f""" """
        self.OutputEntityAndArchitectureFile()

    def setInternalComponents(self):
        for i in range(self.qtChannels-1):
            self.addInternalComponent(component=IOBuffer(qtBlocks=2,dataWidth=8,addrWidth=10),
                                      componentCallName=f'u_BUFFER_IN_{i}',
                                      portmap={      'i_CLK'        : f"i_CLK",
                                                     'i_DATA'       : f"i_IN_DATA({i})", 
                                                     'i_WRITE_ENA'  : f"i_IN_WRITE_ENA",
                                                     'i_SEL_LINE'   : f"i_IN_SEL_LINE",
                                                     'i_READ_ADDR_0' : f"i_IN_READ_ADDR_0",
                                                     'i_READ_ADDR_1' : f"i_IN_READ_ADDR_1",
                                                     'i_WRITE_ADDR' : f"i_IN_WRITE_ADDR",
                                                     'o_DATA_ROW_0' : f"w_PIX_ROW_1({i})",
                                                     'o_DATA_ROW_1' : f"w_PIX_ROW_2({i})"
                                      })
            self.addInternalComponent(component=IOBuffer(qtBlocks=2,dataWidth=8,addrWidth=10),
                            componentCallName=f'u_BUFFER_IN_{i}',
                            portmap={      'i_CLK'        : f"i_CLK",
                                            'i_DATA'       : f"i_IN_DATA({i})", 
                                            'i_WRITE_ENA'  : f"i_IN_WRITE_ENA",
                                            'i_SEL_LINE'   : f"i_IN_SEL_LINE",
                                            'i_READ_ADDR_0' : f"i_IN_READ_ADDR_0",
                                            'i_READ_ADDR_1' : f"i_IN_READ_ADDR_1",
                                            'i_WRITE_ADDR' : f"i_IN_WRITE_ADDR",
                                            'o_DATA_ROW_0' : f"w_PIX_ROW_1({i})",
                                            'o_DATA_ROW_1' : f"w_PIX_ROW_2({i})"
                            })

