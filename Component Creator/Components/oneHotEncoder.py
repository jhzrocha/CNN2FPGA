from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class OneHotEncoder(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = f"One_Hot_Encoder"
        self.portMap =   { 'in': [
                                Port('i_DATA',f"std_logic_vector(DATA_WIDTH-1 downto 0)")
                                ],
                            'out': [ Port('o_DATA',f"std_logic_vector(OUT_WIDTH-1 downto 0)")]
                    }
        self.addGenericByParameters(name='DATA_WIDTH',dataType='integer',initialValue=5)
        self.addGenericByParameters(name='OUT_WIDTH',dataType='integer',initialValue=18)

        self.internalOperations = f"""
            process (i_DATA)
            begin
                for i in 0 to OUT_WIDTH-1 loop
                
                if (i = to_integer(unsigned(i_DATA))) then 
                    o_DATA(i) <= '1'; -- caso valor selecionado
                else
                    o_DATA(i) <= '0'; -- caso valor não selecionado
                end if;
                end loop;
            end process;
        """
        self.OutputEntityAndArchitectureFile()
