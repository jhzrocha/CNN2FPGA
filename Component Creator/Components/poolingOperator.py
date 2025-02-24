from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.type import Type
from Components.io_buffer import IOBuffer
from Components.poolingComputer import PoolingComputer


#Compilado
class PoolingOperator(ComponentCommonMethods):

    def __init__(self, dataWidth=8, addrWidth=10, qtChannels=6, qtRows=2, qtCols=2, poolingType='MAX'):
        self.dataWidth = dataWidth
        self.addrWidth = addrWidth
        self.qtChannels = qtChannels
        self.qtRows = qtRows
        self.qtCols = qtCols
        self.poolingType = poolingType
        self.createComponent()
        
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = f'poolingOperator_{self.qtChannels}_{self.dataWidth}_{self.addrWidth}'
        
        self.defineTypeOnTypePackage(Type(f't_i_IN_DATA_{self.minimalComponentFileName}',declaration=f'array (0 to {self.qtChannels-1}) of std_logic_vector({self.dataWidth-1} downto 0)'))

        self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                  Port('i_CLR','STD_LOGIC'),
                                  Port('i_PIX_SHIFT_ENA','STD_LOGIC'),
                                  Port('i_IN_DATA',f't_i_IN_DATA_{self.minimalComponentFileName}'),
                                  Port('i_IN_WRITE_ENA','STD_LOGIC'),
                                  Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_IN_READ_ADDR_0',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_READ_ADDR_1',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_READ_ADDR_2',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_WRITE_ADDR',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_WRITE_ENA','STD_LOGIC'),
                                  Port('i_OUT_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_OUT_READ_ADDR_0',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_WRITE_ADDR',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')")],
                           'out': [Port('o_BUFFER_OUT',f't_i_IN_DATA_{self.minimalComponentFileName}')] 
                         }
        
        self.addMultipleInternalSignalWires(self.qtRows, {'name': 'w_PIX_ROW', 'dataType': f't_i_IN_DATA_{self.minimalComponentFileName}', 'initialValue': "(others => (others => '0'))"})
        self.addInternalSignalWire(name='w_o_PIX',dataType=f't_i_IN_DATA_{self.minimalComponentFileName}',initialValue="(others => (others => '0'))")
        self.setInternalComponents()
        self.internalOperations = f""" """
        self.OutputEntityAndArchitectureFile()

    def setInternalComponents(self):
        for i in range(self.qtChannels-1):
            self.addInternalComponent(component=IOBuffer(qtBlocks=self.qtRows,dataWidth=8,addrWidth=10),
                                      componentCallName=f'u_BUFFER_IN_{i}',
                                      portmap= self.getInputBufferPortmap(i)                                      
                                      )
            
            self.addInternalComponent(component=PoolingComputer(dataWidth=self.dataWidth, 
                                                                qtRows=self.qtRows,
                                                                qtCols=self.qtCols,
                                                                poolingType= self.poolingType),
                                      componentCallName=f'u_MAX_POOL_{i}',
                                      portmap= self.getPoolingComputerPortmap(i))
            
            self.addInternalComponent(component=IOBuffer(qtBlocks=self.qtRows,dataWidth=8,addrWidth=10), #Alterado para 2 blocos para satisfazer o i_SEL_LINE < 'i_OUT_SEL_LINE'
                            componentCallName=f'u_BUFFER_OUT_{i}',
                            portmap={'i_CLK'         :  'i_CLK',
                                     'i_DATA'        :  f'w_o_PIX({i})', 
                                     'i_WRITE_ENA'   :  'i_OUT_WRITE_ENA',
                                     'i_SEL_LINE'    :  'i_OUT_SEL_LINE',
                                     'i_READ_ADDR_0' :  'i_OUT_READ_ADDR_0',
                                     'i_READ_ADDR_1' :  "(others => '0')",
                                     'i_READ_ADDR_2' :  "(others => '0')",
                                     'i_WRITE_ADDR'  :  'i_OUT_WRITE_ADDR',
                                     'o_DATA_ROW_0'  :  f'o_BUFFER_OUT({i})'
                                    })

    def getPoolingComputerPortmap(self, nrChannel):
        portmap = { 'i_CLK'           : 'i_CLK',
                    'i_CLR'           : 'i_CLR',
                    'i_PIX_SHIFT_ENA' : 'i_PIX_SHIFT_ENA',
                    'o_PIX'           : f'w_o_PIX({nrChannel})'}
        
        for i in range (0, self.qtRows):
            portmap[f'i_PIX_ROW_{i}'] = f'w_PIX_ROW_{i}({nrChannel})'
        return portmap
    
    def getInputBufferPortmap(self, nrChannel):
        portmap = { 'i_CLK'        : f"i_CLK",
                    'i_DATA'       : f"i_IN_DATA({nrChannel})", 
                    'i_WRITE_ENA'  : f"i_IN_WRITE_ENA",
                    'i_SEL_LINE'   : f"i_IN_SEL_LINE",
                    'i_READ_ADDR_0' : f"i_IN_READ_ADDR_0",
                    'i_READ_ADDR_1' : f"i_IN_READ_ADDR_1",
                    'i_WRITE_ADDR' : f"i_IN_WRITE_ADDR"}

        for i in range(0, self.qtRows):
            portmap[f'o_DATA_ROW_{i}'] = f"w_PIX_ROW_{i}({nrChannel})"
        return portmap