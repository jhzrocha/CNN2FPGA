from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.fullyConnectedLayer import FullyConnectedLayer

class FullyConnected(ComponentCommonMethods):
    def __init__(self, indexOnTopLevel = 0, qtChannels = 1, dataWidth=8, numUnits=2, scaleShift=7, weightsFileDataWidth=8, biasFileName =None, biasFileDataWidth=32,qtInputs = 64, 
                 functionActivation='RELU', qtNeuronsPerLayer=[4,5,6]):
        self.indexOnTopLevel = indexOnTopLevel
        
        self.qtChannels = qtChannels
        self.dataWidth = dataWidth
        self.numUnits = numUnits
        self.scaleShift = scaleShift

        self.weightsFileDataWidth = weightsFileDataWidth
        self.biasFileName = biasFileName
        self.biasFileDataWidth = biasFileDataWidth
        
        self.qtInputs = qtInputs        
        self.functionActivation = functionActivation
        self.qtNeuronsPerLayer = qtNeuronsPerLayer
        
        self.qtInputAddr = len(bin(qtInputs)[2:])
        self.createComponent()
    
    
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = f'FullyConnected{self.indexOnTopLevel}idx_{self.qtChannels}chs'
        
        
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic')
                                ],
                            'out': [
                                Port(name='o_READY',dataType=f"std_logic")
                                   ]
                    }
        
        self.createChannels()
        self.internalOperations = f"""
            o_READY <= {self.generateReadyOutput()};
        """
        self.OutputEntityAndArchitectureFile()


    def generateReadyOutput(self):
        condition = ''
        for i in range(0, self.qtChannels-1):
            condition = condition + f' w_CHANNEL_{i}_READY AND' 
        condition = condition + f' w_CHANNEL_{self.qtChannels-1}_READY'

        return condition

    def createChannels(self):
        self.FCLayer = FullyConnectedLayer(dataWidth=self.dataWidth,
                                           numUnits=self.numUnits,
                                           scaleShift=self.scaleShift,
                                           weightsFileDataWidth=self.weightsFileDataWidth,
                                           biasFileName=self.biasFileName,
                                           biasFileDataWidth=self.biasFileDataWidth,
                                           qtInputs=self.qtInputs,
                                           functionActivation=self.functionActivation,
                                           qtNeuronsPerLayer=self.qtNeuronsPerLayer)

        for i in range(0, self.qtChannels):
            
            self.addInputPortByParameters(name = f'i_PIX_{i}',
                                            dataType=self.FCLayer.getPortDataType('i_PIX'),
                                            initialValue = "(others => (others => '0'))")
            self.addOutputPortByParameters(name = f'o_PIX_{i}',
                                            dataType=self.FCLayer.getPortDataType('o_PIX'),
                                            initialValue = "(others => (others => '0'))")
            self.addOutputPortByParameters(name = f'o_READ_ADDR_{i}',
                                dataType=f"std_logic_vector({self.qtInputAddr-1} downto 0)",
                                initialValue = "(others => '0')")
            
            self.addInternalSignalWire(name=f'w_CHANNEL_{i}_READY',
                                       dataType='std_logic')

            self.addInternalComponent(component = self.FCLayer,
                                      componentCallName=f'fcLayerChannel_{i}',
                                      portmap={'i_CLK':'i_CLK',
                                               'i_CLR':'i_CLR',
                                               'i_GO':'i_GO',
                                                'i_PIX':f'i_PIX_{i}',
                                                'o_PIX':f'o_PIX_{i}',
                                                'o_READ_ADDR': f'o_READ_ADDR_{i}', 
                                                'o_READY': f'w_CHANNEL_{i}_READY'})    

