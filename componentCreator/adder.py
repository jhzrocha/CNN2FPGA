import os
class adderComponent:
  
  inputs = []
  portMap = ''
  process = ''
  operations = ''

  call = """    {} : entity work.adder  
        port map (
            {}
            o_VALUE  => {}}
        );"""
  
  file = """
    library IEEE;
    use IEEE.std_logic_1164.all;
    use ieee.numeric_std.all;

    entity adder is
        port (
      {}
      o_VALUE      : out integer
    );
end adder;

architecture arc of adder is
begin    
    add:
    process({})
    begin
		o_VALUE <={}; 
        
	end process add;

end arc;"""



  def __init__(self, qtInputs):

    self.generateFile(qtInputs)
    print(self.file)


  
  def generateFile(self, qtInputs):
    self.setPortMap(qtInputs)
    self.setProcessParameters(qtInputs)
    self.setOperations(qtInputs)
    self.file = self.file.format(self.getInputs(),
                           self.getProcessParameters(),
                           self.getOperations())
     
  def getPortMap(self):
    return self.portMap
  
  def setPortMap(self, qtInputs):
    for i in range(0, qtInputs):
        self.portMap =  self.portMap + 'i_VALUE_{} : in integer;\n'.format(i)
        self.inputs.append('i_VALUE_{}'.format(i))

  
  def getProcessParameters(self):
    return self.process

  def setProcessParameters(self,qtInputs):
    for i in range(0, qtInputs-1):
        self.process =  self.process + 'i_VALUE_{},'.format(i)
    self.process =  self.process + 'i_VALUE_{}'.format(qtInputs-1)
   
  
  def getOperations(self):
    return self.operations
  
  def setOperations(self, qtInputs):
    for i in range(0, qtInputs-1):
        self.operations =  self.operations + 'i_VALUE_{} +'.format(i)
    self.operations =  self.operations + 'i_VALUE_{}'.format(qtInputs-1)
  
  def getObjectCall(self):
    return self.call 
  
  def setObjectCall(self, objectName, connectionParameters):
    self.call = self.call.format(objectName,)  

  def getPortMapConnections(self):
    print('a')
    #    criar a entrada do parametro e criar o
