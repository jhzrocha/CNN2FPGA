from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class OneHotEncoder(ComponentCommonMethods):

#Testado
    def __init__(self, inputDataWidth=5, outputDataWidth=18):
        self.startInstance()
        self.minimalComponentFileName = f"One_Hot_Encoder_{inputDataWidth}x{outputDataWidth}"
        self.portMap =   { 'in': [
                                Port('i_DATA',f"std_logic_vector({inputDataWidth-1} downto 0)")
                                ],
                            'out': [ Port('o_DATA',f"std_logic_vector({outputDataWidth-1} downto 0)")]
                    }

        self.internalOperations = f"""
            process (i_DATA)
            begin
                for i in 0 to {outputDataWidth-1} loop
                    if (i = to_integer(unsigned(i_DATA))) then 
                        o_DATA{f'(i)' if outputDataWidth > 1 else ''} <= '1';
                    else
                        o_DATA{f'(i)' if outputDataWidth > 1 else ''} <= '0'; 
                    end if;
                end loop;
            end process;
        """
        self.OutputEntityAndArchitectureFile()
