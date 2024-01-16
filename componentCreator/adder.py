from ComponentCommonMethods import ComponentCommonMethods

class adderComponent(ComponentCommonMethods):
  
  internalOperations = """
    add:
      process({})
      begin
      o_VALUE <={};           
    end process add;
  """

  def __init__(self):
    self.setOperations(qtInputs)
    super.__init__

  def setOperations(self, qtInputs):
    processParameters = ''
    operations = ''
    
    for i in range(0, qtInputs-1):
        operations =  operations + 'i_VALUE_{} +'.format(i)
        processParameters =  processParameters + 'i_VALUE_{},'.format(i)
    
    processParameters =  processParameters + 'i_VALUE_{}'.format(qtInputs-1)
    operations =  operations + 'i_VALUE_{}'.format(qtInputs-1)
    self.internalOperations.format(processParameters,operations)

