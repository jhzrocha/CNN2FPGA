from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic

class Registrador(ComponentCommonMethods):

    
    def __init__(self, dataWidth = 8):
        self.minimalComponentFileName = 'registrador'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_ENA','std_logic'),
                                Port('i_A',f'std_logic_vector({dataWidth -1} DOWNTO 0)')
                            ],
                            'out': [Port('o_Q',f'std_logic_vector({dataWidth -1} DOWNTO 0)')] 
                    }
        
        self.addInternalSignalWire('r_A', f'std_logic_vector({dataWidth -1} DOWNTO 0)')
        self.internalOperations = """
            process (i_CLK, i_CLR, i_ENA, i_A)
            begin 
                -- reset
                if (i_CLR = '1') then
                    r_A <= (others => '0');    
                -- subida clock
                elsif (rising_edge(i_CLK)) then 
                -- enable ativo
                    if (i_ENA = '1') then
                        r_A <= i_A;      
                    end if;
                end if;
            end process;  
            o_Q <= r_A;
        """
        self.OutputEntityAndArchitectureFile()

