from port import Port
from generic import Generic
from copy import deepcopy

class ComponentCommonMethods:
    
    minimalComponentFileName = ''
    
    generics = []
    portMap = {}
    internalComponents = {}

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
    internalOperations = ''
    architectureDeclaration = """
    architecture arc of {} is
        begin    
        {}
    end arc;"""

    processment = ''

    genericCall = """generic map (
      {}
    )"""
    

    call =  """ {} : entity work.{}  
    {}
    port map (
{}
    );\n"""

    genericsDeclaration = 'generic ({});'

    def __init__(self):
        self.resetParameters()
        if (len(self.internalOperations) > 0):
            self.setProcessment(self.internalOperations)
    
        
    def addGenericByParameters(self, name, dataType, initialValue):
        newGeneric = Generic(name, dataType, initialValue)
        self.generics.append(newGeneric)
    
    def addInputPortByParameters(self, name, dataType, connection = ''):
        newInputPort = Port(name,dataType,connection)
        self.portMap['in'].append(newInputPort)
    
    def addOutputPortByParameters(self, name, dataType, connection = ''):
        newOutputPort = Port(name,dataType,connection)
        self.portMap['out'].append(newOutputPort)

    def addMultipleGeneratedInputPorts(self, qtPorts, dataType):
        for i in range(0, qtPorts):
            self.addInputPortByParameters('i_PORT_{}'.format(i),dataType)
                
    def addMultipleGeneratedOutputPorts(self, qtPorts, dataType):
        for i in range(0, qtPorts):
            self.addOutputPortByParameters('o_PORT_{}'.format(i), dataType)

    def getObjectCall(self, objectName):
        genericCall = ''
        if self.getGenericObjectCall() != '':
            genericCall = self.genericCall.format(self.getGenericObjectCall())
        
        callPortMap = ''
        for i in self.portMap['in']:
            callPortMap = callPortMap + f"        {i.name}  => {i.connection},\n"
        for i in self.portMap['out']:
            callPortMap = callPortMap + f"        {i.name}  => {i.connection},\n"

        if callPortMap.endswith(',\n'):
            callPortMap = callPortMap[:-2]
        
        return self.call.format(objectName,self.minimalComponentFileName,genericCall,callPortMap)
    
    def getGenericObjectCall(self):
        genericCall = ''
        for generic in self.generics:
            genericCall = genericCall + f"{generic.name} => {generic.value},\n"
        if genericCall.endswith(',\n'):
            genericCall = genericCall[:-2]
        return genericCall

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
        for i in self.portMap['in']:
            callPortMap = callPortMap + f'      {i.name} : in {i.dataType};\n'
        for i in self.portMap['out']:
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
        processment = self.getInternalComponentDeclarations() + self.processment
        return self.architectureDeclaration.format(self.minimalComponentFileName, processment)
    
    def setProcessment(self, internalOperations):
        self.processment = internalOperations

    def getEntityAndArchitectureFile(self):
        file = f"""{self.importHeader}
                 {self.getEntityDeclaration()}
                 {self.getArchitectureDeclaration()}"""   
        
        return file
    
            
    def addInternalComponent(self, component, componentCallName):
        self.internalComponents[componentCallName] = deepcopy(component)
    
    def addMultipleInternalComponentDeclarations(self,component, quantity):
        for i in range(quantity):
            self.addInternalComponent(component, f"{component.minimalComponentFileName}_{i}")
    
    
    def getInternalComponentDeclarations(self):
        internalComponentDeclarations = ''
        for i in self.internalComponents.keys():
            internalComponentDeclarations = internalComponentDeclarations + self.internalComponents[i].getObjectCall(i)
        return internalComponentDeclarations

    def setInternalComponentPortMap(self,componentName, portMapParameters):
        internalComponent = self.internalComponents[componentName]

        for portMapParameter in portMapParameters.keys():
            for port in internalComponent.portMap['in']:
                if port.name == portMapParameter:
                    port.connection = portMapParameters[portMapParameter]
            for port in internalComponent.portMap['out']:
                if port.name == portMapParameter:
                    port.connection = portMapParameters[portMapParameter]
    
    def resetParameters(self):
        self.internalComponents = {}
                
