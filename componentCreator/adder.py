from ComponentCommonMethods import ComponentCommonMethods
from port import Port

class AdderComponent(ComponentCommonMethods):
  

  def __init__(self, qtInputPorts):
    self.minimalComponentFileName = 'adder'
    self.portMap = { 'in': [],
                     'out': [Port('o_VALUE','integer')] 
                   }
    self.internalOperations = """
    add:
      process({})
      begin
      o_VALUE <= {};           
    end process add;
    """
    super().__init__()

    self.addMultipleGeneratedInputPorts(qtInputPorts, 'integer')
  
  def addMultipleGeneratedInputPorts(self, qtPorts, dataType):
    super().addMultipleGeneratedInputPorts(qtPorts, dataType)
    self.setOperations()

  def setOperations(self):
    processParameters = ''
    operations = ''
    
    for i in self.portMap['in']:
        operations =  operations + f"{i.name} +"
        processParameters =  processParameters + f"{i.name} ,"
    
    if operations.endswith('+'): 
       operations = operations[:-1]

    if processParameters.endswith(','): 
       processParameters = processParameters[:-1]
    
    self.setProcessment(self.internalOperations.format(processParameters,operations))

