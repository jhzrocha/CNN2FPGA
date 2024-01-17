from port import port
from generic import Generic

class ComponentCommonMethods:
    
    minimalComponentFileName = ''
    generics = []
    inputs = []
    outputs = []

    importHeader = """library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;"""

    entityDeclaration = """
    entity {} is
        {}
        port (
{}
        );
    end {};"""

    architectureDeclaration = """
    architecture arc of {} is
        begin    
        {}
    end arc;"""

    processment = ''

    call = """    {} : entity work.{}  
    port map (
{}
    );"""

    genericsDeclaration = 'generic ({});'

    def __init__(self, minimalComponentFileName):
        self.minimalComponentFileName = minimalComponentFileName
    
    def addInputPort(self, port):
        self.inputs.append(port)
     
    def addOutputPort(self, port):
        self.outputs.append(port)

    def addGenericByParameters(self, name, dataType, initialValue):
        newGeneric = Generic(name, dataType, initialValue)
        self.generics.append(newGeneric)
    
    def addInputPortByParameters(self, name, dataType, connection = ''):
        inputPort = port(name,dataType,connection)
        self.inputs.append(inputPort)
    
    def addOutputPortByParameters(self, name, dataType, connection = ''):
        outputPort = port(name,dataType,connection)
        self.outputs.append(outputPort)

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
                                             self.getGenericDeclaration(),
                                             callPortMap,
                                             self.minimalComponentFileName)
    
    def getGenericDeclaration(self):
        generics = ''
        if(len(self.generics) > 0):
            for i in self.generics:
                generics = generics + f"{i.name} : {i.dataType} := {i.initialValue};\n"
            if generics.endswith(';\n'):
                generics = generics[:-2]            
            generics = self.genericsDeclaration.format(generics)
        return generics


    def getArchitectureDeclaration(self):
        return self.architectureDeclaration.format(self.minimalComponentFileName,self.processment)
    
    def setProcessment(self, internalOperation):
        self.processment = internalOperation

    def getEntityAndArchitectureFile(self):
        file = f"""{self.importHeader}
                 {self.getEntityDeclaration()}
                 {self.getArchitectureDeclaration()}"""   
        
        return file
    