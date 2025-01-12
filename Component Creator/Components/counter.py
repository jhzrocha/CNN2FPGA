from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

    #Compilado
    #Testado
class Counter(ComponentCommonMethods):

    def __init__(self, dataWidth = 8, bitStep = 4):
        self.startInstance()
        self.minimalComponentFileName = f"Counter_{dataWidth}dw_{bitStep}bs"
        self.portMap =   { 'in': [
                                Port(name='i_CLK',dataType=f"std_logic"),
                                Port(name='i_RESET',dataType=f"std_logic"),
                                Port(name='i_INC',dataType=f"std_logic"),
                                Port(name='i_RESET_VAL',dataType=f"std_logic_vector({dataWidth-1} downto 0)",initialValue="(others => '0')")
                                ],
                            'out': [ Port('o_Q',f"std_logic_vector({dataWidth-1} downto 0)")]
                    }
        self.addInternalConstant(name='c_STEP',dataType=f'std_logic_vector ({dataWidth-1} downto 0)',value=f'std_logic_vector(to_unsigned({bitStep}, {dataWidth}))')
        self.addInternalSignalWire(name='r_CNT',dataType=f'std_logic_vector ({dataWidth-1} downto 0)',initialValue="(others => '0')")
        self.internalOperations = """
            process (i_CLK, i_RESET, i_INC, i_RESET_VAL)
            begin    
                if (rising_edge(i_CLK)) then
                if (i_RESET = '1') then
                    r_CNT <= i_RESET_VAL;
                elsif (i_INC = '1') then      
                    r_CNT <= std_logic_vector(unsigned(r_CNT) + unsigned(c_STEP));

                end if;    
                end if;
            end process;   
            
            o_Q <= r_CNT;
        """
        self.OutputEntityAndArchitectureFile()
