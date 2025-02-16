from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port


#Compilado
class MaxComparisonTree(ComponentCommonMethods):
    def __init__(self, qtInputs=4, dataWidth=8):
        self.qtInputs = qtInputs
        self.dataWidth = dataWidth

        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'MaxComparisonTree_{self.qtInputs}i_{self.dataWidth}dw'
        self.portMap =   { 'in': [

                                ],
                            'out': [
                                    Port(name='o_PIX',dataType=f"std_logic_vector ({self.dataWidth-1} downto 0)"),
                                   ] 
                         }
        
        self.addMultipleGeneratedInputPorts(qtPorts=self.qtInputs,
                                            dataType=f"std_logic_vector ({self.dataWidth-1} downto 0)",
                                            name='i_PIX')
        
        self.addMultipleInternalSignalWires(quantity=self.qtInputs-1,
                                            parameters= {'name':'w_PIX_OUT',
                                                        'dataType': f"std_logic_vector ({self.dataWidth-1} downto 0)",
                                                        'initialValue': ""})
        self.internalOperations = """

        """                                                
        self.createinternalOperations()

        self.OutputEntityAndArchitectureFile()

    def createinternalOperations(self):
        initialization = ''
        wSumWithoutConnection = []
        wEntradasWithoutConnection = []
        qtUsedwSum = 0
        
        for x in range(self.qtInputs):
            wEntradasWithoutConnection.insert(0,x)
        initialization = initialization + '\n'
        for x in range(0,self.qtInputs,2):
            if x+1 > self.qtInputs-1:
                break
            else: 
                initialization = initialization + f"             w_PIX_OUT_{qtUsedwSum} <=  i_PIX_{x} when (i_PIX_{x} > i_PIX_{x+1}) else i_PIX_{x+1};\n"
                wEntradasWithoutConnection.remove(x)
                wEntradasWithoutConnection.remove(x+1)
                wSumWithoutConnection.insert(0,qtUsedwSum)
            qtUsedwSum = qtUsedwSum + 1
        initialization = initialization + f"\n"

        while qtUsedwSum+1 < self.qtInputs-1:
            wire = wSumWithoutConnection.pop()
            wire2 = wSumWithoutConnection.pop()

            initialization = initialization + f"             w_PIX_OUT_{qtUsedwSum} <= w_PIX_OUT_{wire} when (w_PIX_OUT_{wire} > w_PIX_OUT_{wire2}) else w_PIX_OUT_{wire2};\n"
            wSumWithoutConnection.insert(0,qtUsedwSum)            
            qtUsedwSum = qtUsedwSum + 1

        initialization = initialization + f"\n"

        if qtUsedwSum > 1:
            if (len(wEntradasWithoutConnection) == 1 and len(wSumWithoutConnection) == 1):
                wire = wSumWithoutConnection.pop()
                wire2 = wEntradasWithoutConnection.pop()
                initialization = initialization + f"            o_PIX <= w_PIX_OUT_{wire} when (w_PIX_OUT_{wire} > i_PIX_{wire2}) else i_PIX_{wire2};\n"
            else:
                wire = wSumWithoutConnection.pop()
                wire2 = wSumWithoutConnection.pop()
                initialization = initialization + f"             o_PIX <= w_PIX_OUT_{wire} when (w_PIX_OUT_{wire} > w_PIX_OUT_{wire2}) else w_PIX_OUT_{wire2};\n"
        else:
            initialization = initialization + f"            o_PIX <= w_PIX_OUT_{qtUsedwSum-1};\n"
        self.internalOperations = initialization



