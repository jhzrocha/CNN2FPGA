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
        
        count = 0
        for x in range(0,qtInputs,2):
            if x+1 > qtInputs-1:
                break
            else: 
                initialization = initialization + f"            w_SUM_OUT_{count} <= STD_LOGIC_VECTOR(signed(w_ENTRADAS({x})) + signed(w_ENTRADAS({x+1})));\n"
            count = count + 1
        
        count2 = count
        for x in range(0,count,2):
            initialization = initialization + f"            w_SUM_OUT_{count2} <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{x}) + signed(w_SUM_OUT_{x+1}));\n"
            count2 = count2 + 1
        
        count3 = count2
        for x in range(count2,count3,2):
            initialization = initialization + f"            w_SUM_OUT_{count3} <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{count2-1}) + signed(w_SUM_OUT_{count2-2}));\n"
            count3 = count3 + 1
        
        if (qtInputs % 2 != 0):
            initialization = initialization + f"            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{count2}) + signed(w_ENTRADAS({qtInputs-1})));\n"
        else:
            initialization = initialization + f"            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{count2-1}) + signed(w_SUM_OUT_{count2}));\n"
        return initialization