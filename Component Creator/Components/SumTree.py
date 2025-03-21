from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class SumTree(ComponentCommonMethods):

    def __init__(self, qtInputs=9, inputDataWidth=16, outputDataWidth=32):
        self.startInstance()
        self.minimalComponentFileName = f"SumTree_{qtInputs}_{inputDataWidth}_{outputDataWidth}"
        self.portMap =   { 'in': [],
                            'out': [Port('o_DATA',f'STD_LOGIC_VECTOR ({outputDataWidth-1} downto 0)')]
                    }
        self.addMultipleGeneratedInputPorts(qtInputs,f'STD_LOGIC_VECTOR ({inputDataWidth-1} downto 0)')
        self.addMultipleInternalSignalWires(qtInputs-1,{'name': 'w_SUM_OUT',
                                                        'dataType': f'STD_LOGIC_VECTOR({outputDataWidth-1} downto 0)',
                                                        'initialValue':''})
        self.addArrayTypeOnArchitecture('t_MAT',f'STD_LOGIC_VECTOR({outputDataWidth-1} downto 0)',qtInputs)
        self.addInternalSignalWire('w_ENTRADAS','t_MAT',"(others =>  ( others => '0'))")
        
        self.internalOperations = f"""
{self.getSignalInitialization(qtInputs,inputDataWidth,outputDataWidth)}
        """
        self.OutputEntityAndArchitectureFile()

    def getSignalInitialization(self,qtInputs,inputDataWidth,outputDataWidth):
        initialization = ''
        wSumWithoutConnection = []
        wEntradasWithoutConnection = []
        qtUsedwSum = 0

        for x in range(qtInputs):
            initialization = initialization + f"            w_ENTRADAS({x})({inputDataWidth-1} downto 0) <= i_PORT_{x};\n"
            wEntradasWithoutConnection.insert(0,x)
        initialization = initialization + '\n'
        
        for x in range(qtInputs):
            initialization = initialization + f"            w_ENTRADAS({x})({outputDataWidth-1} downto {inputDataWidth}) <= (others => '1') when (i_PORT_{x} ({inputDataWidth-1}) = '1') else (others => '0');\n"

        initialization = initialization + f"\n"
        for x in range(0,qtInputs,2):
            if x+1 > qtInputs-1:
                break
            else: 
                initialization = initialization + f"            w_SUM_OUT_{qtUsedwSum} <= STD_LOGIC_VECTOR(signed(w_ENTRADAS({x})) + signed(w_ENTRADAS({x+1})));\n"
                wEntradasWithoutConnection.remove(x)
                wEntradasWithoutConnection.remove(x+1)
                wSumWithoutConnection.insert(0,qtUsedwSum)
            qtUsedwSum = qtUsedwSum + 1
        initialization = initialization + f"\n"

        while qtUsedwSum+1 < qtInputs-1:
            initialization = initialization + f"            w_SUM_OUT_{qtUsedwSum} <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{wSumWithoutConnection.pop()}) + signed(w_SUM_OUT_{wSumWithoutConnection.pop()}));\n"
            wSumWithoutConnection.insert(0,qtUsedwSum)            
            qtUsedwSum = qtUsedwSum + 1
        
        initialization = initialization + f"\n"
        if qtUsedwSum > 1:
            if (len(wEntradasWithoutConnection) == 1 and len(wSumWithoutConnection) == 1):
                initialization = initialization + f"            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{wSumWithoutConnection.pop()}) + signed(w_ENTRADAS({wEntradasWithoutConnection.pop()})));\n"
            else:
                initialization = initialization + f"            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_{wSumWithoutConnection.pop()}) + signed(w_SUM_OUT_{wSumWithoutConnection.pop()}));\n"
        else:
            initialization = initialization + f"            o_DATA <= signed(w_SUM_OUT_{qtUsedwSum-1});\n"


        return initialization
    
