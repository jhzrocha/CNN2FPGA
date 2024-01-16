from port import port


class ComponentCommonMethods:
    
    minimalComponentFileName = ''
    inputs = []
    outputs = []

    importHeader = """library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;"""

    entityDeclaration = """
    entity {} is
        port (
{}
        );
    end {};"""

    architectureDeclaration = """
    architecture arc of {} is
        begin    
        {}
    end arc;"""

    internalOperations = ''

    call = """    {} : entity work.{}  
    port map (
{}
    );"""

    def __init__(self, minimalComponentFileName):
        self.minimalComponentFileName = minimalComponentFileName
    
    def addInputPort(self, port):
        self.inputs.append(port)
     
    def addOutputPort(self, port):
        self.outputs.append(port)

    def addMultipleGeneratedInputPorts(self, qtPorts, dataType):
        for i in range(0, qtPorts):
            newInputPort = port('i_PORT_{}'.format(i), dataType)
            self.inputs.append(newInputPort)
    
    def addMultipleGeneratedOutputPorts(self, qtPorts, dataType):
        for i in range(0, qtPorts):
            newOutputPort = port('o_PORT_{}'.format(i), dataType)
            self.outputs.append(newOutputPort)

    def getObjectCall(self, objectName):
        callPortMap = ''
        for i in self.inputs:
            callPortMap = callPortMap + f"        {i.name}  => {i.connection},\n"
        for i in self.outputs:
            callPortMap = callPortMap + f"        {i.name}  => {i.connection},\n"

        if callPortMap.endswith(',\n'):
            callPortMap = callPortMap[:-2]
        
        return self.call.format(objectName,self.minimalComponentFileName,callPortMap)
    
    def setPortMapConnections(self, inputConnections, outputConnections):
        if len(inputConnections) == len(self.inputs) and len(outputConnections) == len(self.outputs):
            for i in range(len(inputConnections)):
                self.inputs[i].setConnection(inputConnections[i])
            for i in range(len(outputConnections)):
                self.outputs[i].setConnection(outputConnections[i])
        else:
            print("Error: Number of input or output connections does not match.")

    def getEntityDeclaration(self):
        callPortMap = ''
        for i in self.inputs:
            callPortMap = callPortMap + f'      {i.name} : in {i.dataType};\n'
        for i in self.outputs:
            callPortMap = callPortMap + f'      {i.name} : out {i.dataType};\n'

        if callPortMap.endswith(';\n'):
            callPortMap = callPortMap[:-2]
        
        return self.entityDeclaration.format(self.minimalComponentFileName,
                                             callPortMap,
                                             self.minimalComponentFileName)
    
    def getArchitectureDeclaration(self):
        return self.architectureDeclaration.format(self.minimalComponentFileName,self.internalOperations)
    
    def setInternalOperations(self, internalOperation):
        self.internalOperations = internalOperation

    def getEntityAndArchitectureFile(self):
        file = f"""{self.importHeader}
                 {self.getEntityDeclaration()}
                 {self.getArchitectureDeclaration()}"""   
        
        return file