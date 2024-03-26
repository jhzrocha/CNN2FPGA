from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Counter(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = f"Counter"
        self.portMap =   { 'in': [
                                Port(name='i_CLK',dataType=f"std_logic"),
                                Port(name='i_RESET',dataType=f"std_logic"),
                                Port(name='i_INC',dataType=f"std_logic"),
                                Port(name='i_RESET_VAL',dataType=f"std_logic_vector(DATA_WIDTH-1 downto 0)",initialValue="(others => '0'")
                                ],
                            'out': [ Port('o_Q',f"std_logic_vector(DATA_WIDTH-1 downto 0)")]
                    }
        self.addGenericByParameters(name='DATA_WIDTH',dataType='integer',initialValue=8)
        self.addGenericByParameters(name='STEP',dataType='integer',initialValue=4)
        self.addInternalConstant(name='c_STEP',dataType='std_logic_vector (DATA_WIDTH-1 downto 0)',value='std_logic_vector(to_unsigned(STEP, DATA_WIDTH))')
        self.addInternalSignalWire(name='r_CNT',dataType='std_logic_vector (DATA_WIDTH-1 downto 0)',initialValue="(others => '0')")
        self.internalOperations = f"""
            process (i_CLK, i_RESET, i_INC, i_RESET_VAL)
            begin    
                if (rising_edge(i_CLK)) then
                if (i_RESET = '1') then
                    r_CNT <= i_RESET_VAL;
                elsif (i_INC = '1') then      
                    r_CNT <= r_CNT + c_STEP;     
                end if;    
                end if;
            end process;   
            
            o_Q <= r_CNT;
        """
        self.OutputEntityAndArchitectureFile()
