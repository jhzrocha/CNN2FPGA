from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic
from Components.add1 import Add1
class Conv1Op(ComponentCommonMethods):

   
    def __init__(self, qt_bits):
        self.startInstance()
        self.minimalComponentFileName = 'conv1_op'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_IN_READ_ENA','std_logic'),
                                Port('i_IN_DATA','t_ARRAY_OF_LOGIC_VECTOR(0 to C-1)(DATA_WIDTH-1 downto 0)'),
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
                                Port('i_OUT_SEL','std_logic_vector(OUT_SEL_WIDTH-1 downto 0)',initialValue="(others => '0'"),
                                Port('i_OUT_WRITE_ENA','std_logic'),
                                Port('i_OUT_READ_ENA','std_logic'),
                                Port('i_OUT_READ_ADDR','std_logic_vector (9 downto 0)',initialValue="(others => '0')"),
                                Port('i_OUT_INC_ADDR','std_logic'),
                                Port('i_OUT_CLR_ADDR','std_logic')
                                ],
                            'out': [
                                    Port('o_OUT_DATA',f"t_ARRAY_OF_LOGIC_VECTOR(0 to M-1)(DATA_WIDTH-1 downto 0)"),
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
        self.addInternalSignalWire(name='w_o_MUX_NC',dataType='t_ARRAY_OF_LOGIC_VECTOR(0 to M - 1)(31 downto 0)')
        self.addInternalSignalWire(name='w_o_ADD',dataType='t_ARRAY_OF_LOGIC_VECTOR(0 to M - 1)(31 downto 0)',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_o_BIAS_ACC',dataType='t_ARRAY_OF_LOGIC_VECTOR(0 to M - 1)(31 downto 0)',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='r_OUT_ADDR',dataType='std_logic_vector(ADDR_WIDTH-1 downto 0)',initialValue="(others => '0')")
        self.addInternalSignalWire(name='w_RST_OUT_ADDR',dataType='std_logic')
        self.addInternalSignalWire(name='w_CONFIG0',dataType='std_logic')
        self.addInternalSignalWire(name='w_CONFIG1',dataType='std_logic')
        self.addInternalSignalWire(name='w_BIAS_REG_ENA',dataType='std_logic_vector(M-1 downto 0)')
        self.addInternalSignalWire(name='w_o_BIAS_REG',dataType='t_ARRAY_OF_LOGIC_VECTOR(0 to M - 1)(31 downto 0)')
        self.addInternalSignalWire(name='w_BIAS_WRITE_ENA',dataType='std_logic')









        self.internalOperations = """
        w_SUM_OUT(31) <= w_SIGNAL_BIT;           
        w_UNDERFLOW <= a(31) and b(31) and not w_SIGNAL_BIT;
        sum1 <= "10000000000000000000000000000000" when (w_UNDERFLOW = '1') else 
                "01111111111111111111111111111111" when (w_OVERFLOW= '1') else 
                w_SUM_OUT;
        overflow <=  w_OVERFLOW; 
        underflow <= w_UNDERFLOW;
        """
        self.OutputEntityAndArchitectureFile()