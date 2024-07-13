from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.arvore_soma_conv import ArvoreSomaConv

class AverageTree(ComponentCommonMethods):
   
    def __init__(self, qtInputs, inputDataWidth):
        self.startInstance()
        self.minimalComponentFileName = f'averageTree_{qtInputs}'
        self.portMap =   { 'in': [],
                           'out': [
                                   Port('o_PIX',f'STD_LOGIC_VECTOR ({inputDataWidth-1} downto 0)')] 
                         }
        
        
        
        self.addMultipleGeneratedInputPorts(qtInputs,f'STD_LOGIC_VECTOR ({inputDataWidth-1} downto 0)','i_PIX')
        self.addInternalSignalWire('w_SUM_RESULT',f'STD_LOGIC_VECTOR ({inputDataWidth*2-1} downto 0)')
        self.addInternalSignalWire('w_TEMP_AVG',f'unsigned ({inputDataWidth*2-1} downto 0)')

        self.internalOperations = """ """
        self.addSumTree(qtInputs,inputDataWidth)
        self.OutputEntityAndArchitectureFile()



    def addSumTree(self,qtInputs,inputDataWidth):
        sumTreePortmap = {'o_DATA':'w_SUM_RESULT'}
        for x in range(qtInputs):
            sumTreePortmap[f'i_PORT_{x}'] = f'i_PIX_{x}'
        
        self.addInternalComponent(component=ArvoreSomaConv(qtInputs=qtInputs,
                                                           inputDataWidth=inputDataWidth,
                                                           outputDataWidth=inputDataWidth*2),
                                 componentCallName='SumTree',
                                 portmap=sumTreePortmap)
        
        self.addInternalOperationLine(f'w_TEMP_AVG <= unsigned(w_SUM_RESULT) / 6;')
        self.addInternalOperationLine(f'o_PIX <= std_logic_vector(w_TEMP_AVG({inputDataWidth-1} downto 0));')
        