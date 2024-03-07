from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class ArvoreSomaConv(ComponentCommonMethods):

#    Não concluido
    def __init__(self, qtInputs):
        self.startInstance()
        self.minimalComponentFileName = f"arvore_soma_conv"
        self.portMap =   { 'in': [],
                            'out': [Port('o_DATA','out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)')]
                    }
        self.addGenericByParameters('i_DATA_WIDTH','INTEGER',16)
        self.addGenericByParameters('o_DATA_WIDTH','INTEGER',32)
        self.addMultipleGeneratedInputPorts(qtInputs,'STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)')
        self.addMultipleInternalSignalWires(qtInputs-1,{'name': 'w_SUM_OUT',
                                                        'dataType': 'STD_LOGIC_VECTOR(o_DATA_WIDTH -1 downto 0)',
                                                        'initialValue':''})
        self.addArrayTypeOnArchitecture('t_MAT','STD_LOGIC_VECTOR(o_DATA_WIDTH - 1 downto 0)',qtInputs)
        self.addInternalSignalWire('w_ENTRADAS','t_MAT',"(others =>  ( others => '0'))")
        
        self.internalOperations = f"""
{self.getSignalInitialization(qtInputs)}
        """
        self.OutputEntityAndArchitectureFile()



    def getSignalInitialization(self,qtInputs):
        initialization = ''
        for x in range(qtInputs):
            initialization = initialization + f"            w_ENTRADAS({x})(i_DATA_WIDTH-1 downto 0) <= i_PORT_{x};\n"
        initialization = initialization + '\n'
        for x in range(qtInputs):
            initialization = initialization + f"            w_ENTRADAS({x})(31 downto 16) <= (others => '1') when (i_PORT_{x} (15) = '1') else (others => '0');\n"
        
        
        for x in range(0,qtInputs):
            print(x)
            f"w_SUM_OUT_{x} <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(0)) + signed(w_ENTRADAS(1)));"

        
        return initialization