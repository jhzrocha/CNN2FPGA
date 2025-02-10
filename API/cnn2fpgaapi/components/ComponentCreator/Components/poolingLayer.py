from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.type import Type
from Components.poolingControl import PoolingController
from Components.poolingOperator import PoolingOperator

class PoolingLayer(ComponentCommonMethods):

    def __init__(self, qtChannels=6,qtAddrs=2, dataWidth = 8, addrWidth = 10, maxAddr='0110000000', 
                 poolingType='Max', qtPixelRows=2, qtPixelsPerRow=2, qtBlocksBufferIn=2,qtBlocksBufferOut=1):
        self.qtChannels = qtChannels
        self.qtAddrs = qtAddrs
        self.dataWidth = dataWidth
        self.addrWidth = addrWidth
        self.maxAddr = maxAddr
        self.createComponent()
        
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = f'PoolingLayer_{self.qtChannels}_{self.qtAddrs}_{self.dataWidth}_{self.addrWidth}_{self.maxAddr}'        
        poolingOperator = PoolingOperator(dataWidth=self.dataWidth,
                                          addrWidth=self.addrWidth,
                                          qtChannels=self.qtChannels)
        self.portMap =   { 'in': [
                                  Port('i_CLK','std_logic'),
                                  Port('i_CLR','std_logic'),
                                  Port('i_GO','std_logic'),
                                  Port('i_IN_DATA',poolingOperator.getPortDataType('i_IN_DATA'), initialValue="(others => (others => '0'))"),
                                  Port('i_IN_WRITE_ENA','std_logic'),
                                  Port('i_IN_WRITE_ADDR',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_OUT_READ_ADDR_0',f'std_logic_vector ({self.addrWidth-1} downto 0)',initialValue="(others => '0')")
                                  ],
                           'out': [
                                  Port('o_READY','std_logic'),
                                  Port('o_BUFFER_OUT',poolingOperator.getPortDataType('o_BUFFER_OUT'))
                                  ] 
                         }

        self.addInternalSignalWire(name='w_IN_READ_ADDR_0',
                                   dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)')
        self.addInternalSignalWire(name='w_IN_READ_ADDR_1',
                                   dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)')
        self.addInternalSignalWire(name='w_PIX_SHIFT_ENA',
                                   dataType=f'std_logic')
        self.addInternalSignalWire(name='w_OUT_WRITE_ENA',
                                   dataType=f'std_logic')
        self.addInternalSignalWire(name='w_OUT_WRITE_ADDR',
                                   dataType=f'std_logic_vector ({self.addrWidth-1} downto 0)',
                                   initialValue="(others => '0')")
        
        self.addInternalComponent(component=PoolingController(dataWidth=self.dataWidth,
                                                              addWidth=self.addrWidth,
                                                              maxAddr=self.maxAddr),
                                  componentCallName='u_CONTROLE',
                                  portmap= {'i_CLK'            : 'i_CLK',
                                            'i_CLR'            : 'i_CLR',
                                            'i_GO'             : 'i_GO',
                                            'o_READY'          : 'o_READY',
                                            'o_IN_READ_ADDR_0'  : 'w_IN_READ_ADDR_0',
                                            'o_IN_READ_ADDR_1'  : 'w_IN_READ_ADDR_1',
                                            'o_PIX_SHIFT_ENA'  : 'w_PIX_SHIFT_ENA',
                                            'o_OUT_WRITE_ENA'  : 'w_OUT_WRITE_ENA',
                                            'o_OUT_WRITE_ADDR' : 'w_OUT_WRITE_ADDR'})
        
        self.addInternalComponent(component= poolingOperator,
                            componentCallName='u_OPERACIONAL',
                            portmap= {'i_CLK'            : 'i_CLK',
                                      'i_CLR'            : 'i_CLR',
                                      'i_PIX_SHIFT_ENA'  : 'w_PIX_SHIFT_ENA',
                                      'i_IN_DATA'        : 'i_IN_DATA',
                                      'i_IN_WRITE_ENA'   : 'i_IN_WRITE_ENA',
                                      'i_IN_WRITE_ADDR'  : 'i_IN_WRITE_ADDR',
                                      'i_IN_SEL_LINE'    : 'i_IN_SEL_LINE',
                                      'i_IN_READ_ADDR_0' :  'w_IN_READ_ADDR_0',
                                      'i_IN_READ_ADDR_1' :  'w_IN_READ_ADDR_1',
                                      'i_IN_READ_ADDR_2' :  "(others => '0')",
                                      'i_OUT_WRITE_ENA'  : 'w_OUT_WRITE_ENA',
                                      'i_OUT_WRITE_ADDR' : 'w_OUT_WRITE_ADDR',
                                      'i_OUT_SEL_LINE'   : '"00"',
                                      'i_OUT_READ_ADDR_0':  'i_OUT_READ_ADDR_0',
                                      'o_BUFFER_OUT'     : 'o_BUFFER_OUT'})
        self.internalOperations = f""" """
        self.OutputEntityAndArchitectureFile()


