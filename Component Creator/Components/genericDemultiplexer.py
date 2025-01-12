from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.type import Type

class GenericDemultiplexer(ComponentCommonMethods):

#Testado
    def __init__(self, selWidth=2, dataWidth = 8):
        self.startInstance()
        self.minimalComponentFileName = f"GenericDemultiplexer_{selWidth}_{dataWidth}b"
        self.defineTypeOnTypePackage(Type(f't_ARRAY_OF_LOGIC_VECTOR_{self.minimalComponentFileName}',declaration=f"array (0 to (2 ** {selWidth}) - 1) of std_logic_vector({dataWidth} downto 0)"))
        self.portMap =   { 'in': [
                                Port('i_A',f'std_logic_vector({dataWidth- 1}  downto 0)'),
                                Port('i_SEL',f'std_logic_vector({selWidth- 1}  downto 0)'),
                                ],
                            'out': [ Port('o_Q',dataType=f't_ARRAY_OF_LOGIC_VECTOR_{self.minimalComponentFileName}', initialValue="(others => (others => '0'))")]
                    }
        self.addInternalSignalWire(name='w_INDEX',dataType='integer',initialValue=0)
        self.internalOperations = f"""
            process (i_A, i_SEL)
            begin
                for i in 0 to ((2 ** {selWidth}) - 1) loop
                if (i = to_integer(unsigned(i_SEL))) then
                    o_Q(i) <= i_A; -- caso valor selecionado
                else
                    o_Q(i) <= (others => '0'); -- caso valor não selecionado
                end if;
                end loop;
            end process;
        """
        self.OutputEntityAndArchitectureFile()
