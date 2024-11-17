from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.io_buffer import IOBuffer

class PoolingOperator(ComponentCommonMethods):

    # Não testado
    def __init__(self, qtChannels=6,qtAddrs=2, dataWidth = 8, addrWidth = 10, maxAddr='0110000000'):
        self.startInstance()
        self.minimalComponentFileName = 'poolingController'
        self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                  Port('i_CLR','STD_LOGIC'),
                                  Port('i_PIX_SHIFT_ENA','STD_LOGIC'),
                                  Port('i_IN_DATA',f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChannels-1})({dataWidth-1} downto 0)'),
                                  Port('i_IN_READ_ENA','STD_LOGIC'),
                                  Port('i_IN_WRITE_ENA','STD_LOGIC'),
                                  Port('i_IN_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_IN_WRITE_ADDR',f'std_logic_vector ({addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_READ_ENA','STD_LOGIC'),
                                  Port('i_OUT_WRITE_ENA','STD_LOGIC'),
                                  Port('i_OUT_SEL_LINE','std_logic_vector (1 downto 0)'),
                                  Port('i_OUT_READ_ADDR0',f'std_logic_vector ({addrWidth-1} downto 0)',initialValue="(others => '0')"),
                                  Port('i_OUT_WRITE_ADDR',f'std_logic_vector ({addrWidth-1} downto 0)',initialValue="(others => '0')")],
                           'out': [Port('o_BUFFER_OUT',f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChannels-1})({dataWidth-1} downto 0)')] 
                         }
        self.addMultipleGeneratedInputPorts(qtPorts=qtAddrs,dataType=f'std_logic_vector ({addrWidth-1} downto 0)',initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_PIX_ROW_1',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChannels-1})({dataWidth-1} downto 0)',initialValue="(others => (others => '0')")
        self.addInternalSignalWire(name='w_PIX_ROW_2',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChannels-1})({dataWidth-1} downto 0)',initialValue="(others => (others => '0')")
        self.addInternalSignalWire(name='w_o_PIX',dataType=f't_ARRAY_OF_LOGIC_VECTOR(0 to {qtChannels-1})({dataWidth-1} downto 0)',initialValue="(others => (others => '0')")

        self.internalOperations = f""" """
        self.OutputEntityAndArchitectureFile()

    def setInternalComponents(self,qtChannels):
        for i in range(qtChannels-1):
            self.addInternalComponent(component=IOBuffer(qtBlocks=2,dataWidth=8,addrWidth=10),
                                      componentCallName=f'u_BUFFER_IN_{i}',
                                      portmap=,
                                      generics=
                                      )

