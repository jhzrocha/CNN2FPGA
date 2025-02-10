from ComponentBases.port import Port
from ComponentBases.generic import Generic
from ComponentBases.wire import Wire
from ComponentBases.type import Type
from ComponentBases.constant import Constant
from copy import deepcopy
import re
from FileHandler.fileHandler import FileHandler
import Config.config

class ComponentCommonMethods:
    
    minimalComponentFileName = ''
    
    generics = []
    portMap = {}
    
    internalComponents = {}
    internalSignalWires = []
    internalVariables = []
    internalTypes = []
    internalConstants = []

    importHeader = """library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;"""

    entityDeclaration = """
    entity {} is
        {}
        port ({}
        );
    end {};"""
    internalOperations = ''
    architectureDeclaration = """
    architecture arc of {} is
{}{}{}
{}
        begin{}
    end arc;"""

    processment = ''

    genericCall = """
        generic map (
            {}
        )"""    

    call =  """ 
        {} : entity work.{}{}
        port map (
    {}
        );\n"""

    signalWiresDeclarations = ''
    variableWiresDeclarations = ''

    genericsDeclaration = 'generic ({});'
    typesToTypesPackage = []

       
    def addGenericByParameters(self, name, dataType, initialValue=''):
        newGeneric = Generic(name, dataType, initialValue)
        self.generics.append(newGeneric)
    
    def addInputPortByParameters(self, name, dataType, connection = '', initialValue =''):
        newInputPort = Port(name,dataType,connection,initialValue)
        self.portMap['in'].append(newInputPort)
    
    def addOutputPortByParameters(self, name, dataType, connection = '', initialValue=''):
        newOutputPort = Port(name,dataType,connection,initialValue)
        self.portMap['out'].append(newOutputPort)

    def addMultipleGeneratedInputPorts(self, qtPorts, dataType, name = '',initialValue=''):
        for i in range(0, qtPorts):
            portName = name
            if name == '':
                portName = f"i_PORT_{i}"
            else:
                portName = f"{name}_{i}"
            self.addInputPortByParameters(name=portName,
                                          dataType=dataType,
                                          initialValue=initialValue)
                
    def addMultipleGeneratedOutputPorts(self, qtPorts, dataType,name = '', initialValue = ''):
        for i in range(0, qtPorts):
            portName = name
            if name == '':
                portName = f"o_PORT_{i}"
            else:
                portName = f"{name}_{i}"
            self.addOutputPortByParameters(name=portName,
                                           dataType=dataType,
                                           initialValue=initialValue)

    def getObjectCall(self, objectName):
        genericCall = ''
        if self.getGenericObjectCall() != '':
            genericCall = self.genericCall.format(self.getGenericObjectCall())
        callPortMap = ''
        isFirst = True
        for i in self.portMap['in']:
            if(isFirst):
                callPortMap = callPortMap + f"        {i.name}  => {i.connection},\n"
                isFirst = False
            else:
                callPortMap = callPortMap + f"            {i.name}  => {i.connection},\n"
        for i in self.portMap['out']:
               if (i.connection != ''):
                callPortMap = callPortMap + f"            {i.name}  => {i.connection},\n"
        if callPortMap.endswith(',\n'):
            callPortMap = callPortMap[:-2]
        return self.call.format(objectName,self.minimalComponentFileName,genericCall,callPortMap)
    
    def getGenericObjectCall(self):
        genericCall = ''
        isFirst = True
        for generic in self.generics:
            if(isFirst):
                genericCall = genericCall + f"{generic.name} => {generic.value},\n"
                isFirst = False
            else:
                genericCall = genericCall + f"            {generic.name} => {generic.value},\n"
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
        first = True
        initialValue = ''
        for i in self.portMap['in']:
            self.verifyDataType(i)
            if(i.initialValue != ''):
                initialValue = f":= {i.initialValue}"

            if (first):
                callPortMap = callPortMap + f'{i.name} : in {i.dataType}{initialValue};\n'
                first = False
            else:
                callPortMap = callPortMap + f'              {i.name} : in {i.dataType}{initialValue};\n'
            initialValue = ''
        for j in self.portMap['out']:
            self.verifyDataType(j)
            initialValue = ''
            if(j.initialValue != ''):
                initialValue = f":= {j.initialValue}"
            callPortMap = callPortMap + f'              {j.name} : out {j.dataType}{initialValue};\n'
                
        if callPortMap.endswith(';\n'):
            callPortMap = callPortMap[:-2]
        
        return self.entityDeclaration.format(self.minimalComponentFileName,
                                             self.getGenericDeclaration(),
                                             callPortMap,
                                             self.minimalComponentFileName)
    
    def getGenericDeclaration(self):
        generics = ''
        first = True
        if(len(self.generics) > 0):
            for generic in self.generics:
                if first:
                    generics = generics + generic.getDeclaration()
                    first = False
                else:
                    generics = generics + '                 ' + generic.getDeclaration()
            if generics.endswith(';\n'):
                generics = generics[:-2]            
            generics = self.genericsDeclaration.format(generics)
        return generics


    def getArchitectureDeclaration(self):
        processment = self.getInternalComponentDeclarations() + self.processment
        self.generateWireDeclarations()
        return self.architectureDeclaration.format(self.minimalComponentFileName, self.getTypesDeclarations(),self.signalWiresDeclarations, self.variableWiresDeclarations,self.getConstantsDeclarations(), processment)
    
    def getConstantsDeclarations(self):
        constantsDeclarations = ''
        for constant in self.internalConstants:
            constantsDeclarations = constantsDeclarations + constant.getConstantDeclaration()
        return constantsDeclarations

    def addInternalConstant(self, name, dataType, value):
        self.internalConstants.append(Constant(name=name,dataType=dataType,value=value))
    
    def setProcessment(self, internalOperations):
        self.processment = internalOperations

    def getEntityAndArchitectureFile(self):
        file = f"""{self.importHeader}
                 {self.getEntityDeclaration()}
                 {self.getArchitectureDeclaration()}"""   
        
        return file
    
            
    def addInternalComponent(self, component, componentCallName, portmap=None, generics=None):
        internalComponent = deepcopy(component)
        setattr(self, componentCallName, internalComponent)
        if(generics):
            for genericKey in generics.keys():
                for gen in internalComponent.generics:
                    if gen.name == genericKey:
                        gen.value = generics[genericKey]
        if (not self.verifyIfInternalComponentAlreadyExists(componentCallName)):
            self.internalComponents[componentCallName] = internalComponent
        if(portmap):
            self.setInternalComponentPortMap(componentCallName,portmap)
        


    
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
    

    def setInternalComponentGenerics(self, internalComponentName, genericName, value): 
        internalComponent = self.internalComponents[internalComponentName]
        for generic in internalComponent.generics:
            if(generic.name == genericName):
                generic.value = value

    def OutputEntityAndArchitectureFile(self):
        if (len(self.internalOperations) > 0):
            self.setProcessment(self.internalOperations)
        fileHandler = FileHandler("Output")
        fileHandler.addFile(f"{self.minimalComponentFileName}.vhd",self.getEntityAndArchitectureFile())
        fileHandler.addTypesToPackageFile(self.typesToTypesPackage)
        del fileHandler
    
    def generateWireDeclarations(self):
        for signal in self.internalSignalWires:
            self.verifyDataType(signal)
            if signal.initialValue != '':
                self.signalWiresDeclarations = self.signalWiresDeclarations + f"        signal {signal.name} : {signal.dataType} := {signal.initialValue};\n"
            else:
                self.signalWiresDeclarations = self.signalWiresDeclarations + f"        signal {signal.name} : {signal.dataType};\n"
        for variable in self.internalVariables:
            if variable.initialValue != '':
                self.variableWiresDeclarations = self.variableWiresDeclarations + f"        variable {variable.name} : {variable.dataType} := {variable.initialValue};\n"
            else:
                self.variableWiresDeclarations = self.variableWiresDeclarations + f"        variable {variable.name} : {variable.dataType};\n"

    def addInternalSignalWire(self,name, dataType, initialValue=''):
        newWire = Wire(name,dataType, initialValue)
        if not self.verifyIfWireAlreadyExists(newWire.name, self.internalSignalWires):
            self.internalSignalWires.append(newWire)
    
    def addInternalVariable(self,name, dataType, initialValue =''):
        newWire = Wire(name,dataType, initialValue)
        if not self.verifyIfWireAlreadyExists(newWire.name, self.internalVariables):
            self.internalVariables.append(newWire)
        

    def addMultipleInternalSignalWires(self,quantity,parameters):
        for i in range(quantity):
            if (parameters['initialValue']):
                self.addInternalSignalWire(f"{parameters['name']}_{i}",parameters['dataType'],parameters['initialValue'])
            else:
                self.addInternalSignalWire(f"{parameters['name']}_{i}",parameters['dataType'])
    
    def addMultipleInternalVariables(self,quantity,parameters):
        for i in range(quantity):
            self.addInternalVariable(f"{parameters['name']}_{i}",parameters['dataType'],parameters['initialValue'])
        
    def createDesignFile(self):
        designComponent = ComponentCommonMethods()
        designComponent.minimalComponentFileName = 'CNN2FPGAVHDL'
        designComponent.internalComponents = {}
        designComponent.internalSignalWires = {}
        designComponent.internalVariables = {}
        designComponent.internalTypes = []
        designComponent.portMap = self.portMap
        designComponent.generics = self.generics
        designComponent.addInternalComponent(deepcopy(self),self.minimalComponentFileName)
        
        portMapParameter = {}

        for i in designComponent.portMap['in']:
            portMapParameter[i.name] = i.name
        for i in designComponent.portMap['out']:
            portMapParameter[i.name] = i.name
        
        designComponent.setInternalComponentPortMap(self.minimalComponentFileName,portMapParameter)
        designComponent.OutputEntityAndArchitectureFile()
        del designComponent


    def verifyIfWireAlreadyExists(self, elementName, array):
        for x in array:
            if elementName == x.name:
                return True
        return False

    def verifyIfInternalComponentAlreadyExists(self, componentCallName):
        if componentCallName in self.internalComponents:
            return True
        return False
  
    def startInstance(self):
        self.internalComponents = {}
        self.internalSignalWires = []
        self.internalVariables = []
        self.generics = []
        self.internalTypes = []
        self.internalConstants = []


    def addArrayTypeOnArchitecture(self, name, datatype, size):
        self.internalTypes.append(Type(name=name,dataType=datatype,size=size))

    def addStateTypeOnArchitecture(self, name, states):
        self.internalTypes.append(Type(name=name,states=states,type='state'))

    def getTypesDeclarations(self):
        typesDeclarations = ''
        for type in self.internalTypes:
            typesDeclarations = typesDeclarations + type.getDeclaration()
        return typesDeclarations
    
    def addInternalOperationLine(self, operationLine):
        self.internalOperations = self.internalOperations + '\n' + operationLine

    def defineTypeOnTypePackage(self, type):
        self.typesToTypesPackage.append(type)
    
    def getPortDataType(self,nmPort):
        for port in self.portMap['in']:
            if(port.getName() == nmPort):
                self.verifyDataType(port)
                return port.getdataType()
        
        for port in self.portMap['out']:
            if(port.getName() == nmPort):
                self.verifyDataType(port)
                return port.getdataType()
        return None

    def verifyDataType(self, subcomponent):
        if (self.isArrayInDataType(subcomponent.getdataType())):
            if(not self.verifyIfArrayWithOneElement(subcomponent)):
                self.defineTypeOnTypePackage(Type(f'{subcomponent.getName()}_{self.minimalComponentFileName}',
                                                declaration=subcomponent.getdataType()))
                subcomponent.setdataType(f'{subcomponent.getName()}_{self.minimalComponentFileName}')
            else:
                subcomponent.setdataType(subcomponent.getdataType().split('of')[-1].strip())
                self.verifyInitialValue(subcomponent)
    
    def verifyInitialValue(self, subcomponent):
        if subcomponent.initialValue != '':
            if subcomponent.initialValue.count('=>') > 1:
                subcomponent.initialValue = re.sub(r"\(others\s*=>\s*\(others\s*=>\s*'0'\)\)", "(others => '0')", subcomponent.initialValue)

    def isArrayInDataType(self, dataType):
        if 'array' in dataType:
            return True
        return False
        
    def verifyIfArrayWithOneElement(self, signal):
        if ('0 to 0' in signal.getdataType() or
            '0 downto 0' in signal.getdataType()):
            return True
        return False
   
