from ComponentCommonMethods import ComponentCommonMethods

class adderComponent(ComponentCommonMethods):
  
  internalOperations = """
    add:
      process({})
      begin
      o_VALUE <= {};           
    end process add;
  """

  def __init__(self, minimalComponentFileName, qtInputPorts):
    self.addOutputPortByParameters('o_VALUE', 'integer')
    self.addMultipleGeneratedInputPorts(qtInputPorts, 'integer')
    super().__init__(minimalComponentFileName)
  

  def addMultipleGeneratedInputPorts(self, qtPorts, dataType):
    super().addMultipleGeneratedInputPorts(qtPorts, dataType)
    self.setOperations()

  def setOperations(self):
    processParameters = ''
    operations = ''
    
    for i in self.inputs:
        operations =  operations + f"{i.name} +"
        processParameters =  processParameters + f"{i.name} ,"
    
    if operations.endswith('+'): 
       operations = operations[:-1]

    if processParameters.endswith(','): 
       processParameters = processParameters[:-1]
    
    self.setProcessment(self.internalOperations.format(processParameters,operations))

