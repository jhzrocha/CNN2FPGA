from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class GreaterComparissonTree(ComponentCommonMethods):
   
    def __init__(self, qtInputs, dataWidth):
        self.startInstance()
        self.minimalComponentFileName = f'greaterComparissonTree_{qtInputs}_{dataWidth}b'
        self.portMap =   { 'in': [],
                           'out': [
                                   Port('o_PIX',f'STD_LOGIC_VECTOR ({dataWidth-1} downto 0)')] 
                         }
        
        
        
        self.addMultipleGeneratedInputPorts(qtInputs,f'STD_LOGIC_VECTOR ({dataWidth-1} downto 0)','i_PIX')
        self.addMultipleInternalSignalWires(quantity= qtInputs-1,
                                            parameters={'name' : 'w_PIX_OUT',
                                                        'dataType' : f'STD_LOGIC_VECTOR ({dataWidth-1} downto 0)',
                                                        'initialValue': None})
        self.internalOperations = """ """
        self.setInternalBehavior(qtInputs)
        self.OutputEntityAndArchitectureFile()


    def setInternalBehavior(self,qtInputs):
        count = 0
        for i in range(0,qtInputs-1,2):
            self.addInternalOperationLine(f'w_PIX_OUT_{count} <= i_PIX_{i} when (i_PIX_{i} > i_PIX_{i+1}) else i_PIX_{i+1};')
            count = count + 1
        
        for i in range(0,count,2):
            self.addInternalOperationLine(f'w_PIX_OUT_{count} <= w_PIX_OUT_{i} when (w_PIX_OUT_{i} > w_PIX_OUT_{i+1}) else w_PIX_OUT_{i+1};')
            count = count + 1

        self.addInternalOperationLine(f'o_PIX <= w_PIX_OUT_{count-1} ;')

