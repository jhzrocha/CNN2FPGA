from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class RAM(ComponentCommonMethods):

    def __init__(self, dataWidth=8, addrWidth=10, size = 128):
        self.startInstance()
        self.minimalComponentFileName = f'RAM_{addrWidth}_{dataWidth}b'
        self.portMap =  { 'in': [
                                    Port(name='i_CLK',dataType='std_logic'),
                                    Port(name='i_ADDR', dataType=f'std_logic_vector({addrWidth-1} downto 0)'),
                                    Port(name='i_DATA',dataType=f'std_logic_vector({dataWidth-1} downto 0)'),
                                    Port(name='i_WRITE',dataType='std_logic')

                                ],
                            'out': [Port(name='o_DATA', dataType=f'std_logic_vector({dataWidth-1} downto 0)')]
                        }
        

        self.addArrayTypeOnArchitecture(name='RAM_ARRAY',type=f'std_logic_vector ({dataWidth-1} downto 0)',size=size)
        
        self.addInternalSignalWire(name='RAM',dataType='RAM_ARRAY',initialValue="(others => (others => '0'))")

        self.internalOperations = """ 
        process(i_CLK)
        begin
            if(rising_edge(i_CLK)) then
                if(i_WRITE='1') then
                    RAM(to_integer(unsigned(i_ADDR))) <= i_DATA;
                end if;
            end if;
        end process;

        o_DATA <= RAM(to_integer(unsigned(i_ADDR)));
        
        """

        self.OutputEntityAndArchitectureFile()
    