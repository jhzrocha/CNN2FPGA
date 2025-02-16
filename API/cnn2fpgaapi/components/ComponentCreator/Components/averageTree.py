from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.SumTree import SumTree

#Compilado
class AverageTree(ComponentCommonMethods):
   
    def __init__(self, qtInputs, inputDataWidth):
        self.qtInputs = qtInputs
        self.inputDataWidth = inputDataWidth
        self.createComponent()
        
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = f'AverageTree{self.qtInputs}_{self.inputDataWidth}dw'
        self.portMap =   { 'in': [],
                           'out': [
                                   Port('o_PIX',f'STD_LOGIC_VECTOR ({self.inputDataWidth-1} downto 0)')] 
                         }      
        
        
        self.addMultipleGeneratedInputPorts(self.qtInputs,f'STD_LOGIC_VECTOR ({self.inputDataWidth-1} downto 0)','i_PIX')
        self.addInternalSignalWire('w_SUM_RESULT',f'STD_LOGIC_VECTOR ({self.inputDataWidth*2-1} downto 0)')
        self.addInternalSignalWire('w_TEMP_AVG',f'unsigned ({self.inputDataWidth*2-1} downto 0)')

        self.internalOperations = """ """
        self.addSumTree()
        self.OutputEntityAndArchitectureFile()



    def addSumTree(self):
        sumTreePortmap = {'o_DATA':'w_SUM_RESULT'}
        for x in range(self.qtInputs):
            sumTreePortmap[f'i_PORT_{x}'] = f'i_PIX_{x}'
        
        self.addInternalComponent(component=SumTree(qtInputs=self.qtInputs,
                                                           inputDataWidth=self.inputDataWidth,
                                                           outputDataWidth=self.inputDataWidth*2),
                                 componentCallName='SumTree',
                                 portmap=sumTreePortmap)
        
        self.addInternalOperationLine(f'        w_TEMP_AVG <= unsigned(w_SUM_RESULT) / {self.qtInputs};')
        self.addInternalOperationLine(f'        o_PIX <= std_logic_vector(w_TEMP_AVG({self.inputDataWidth-1} downto 0));')
        