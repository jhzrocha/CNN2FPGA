from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from FileHandler.fileHandler import FileHandler
from ComponentBases.generic import Generic
import Config.config

class MemoryInitializationComponent(ComponentCommonMethods):
    
    def __init__(self, type, initFileName, dataWidth, dataDepth):
        self.type = type
        self.fpgaType = Config.config.FPGADevice
        self.initFileName = initFileName
        self.dataWidth = dataWidth
        self.dataDepth = dataDepth
        self.createComponent()
    
    def createComponent(self):
        self.startInstance()
        self.minimalComponentFileName = self.type
        self.portMap = self.getPortmap()
        self.generics = [Generic(name=f'init_file_name', 
                                 dataType='string',
                                 initialValue=f'"{self.initFileName}"'),
                         Generic(name=f'DATA_WIDTH',
                                 dataType='integer', 
                                 initialValue=self.dataWidth,),
                         Generic(name=f'DATA_DEPTH',
                                dataType='integer',
                                 initialValue=self.dataDepth)]

        self.internalOperations = """

        """
        self.OutputEntityAndArchitectureFile()
   
    def OutputEntityAndArchitectureFile(self):
        FileHandler('Output').addMemoryInitializationComponents(self.type, self.fpgaType)

    def getPortmap(self):
        if self.type == 'conv_weights':
            return  { 'in': [
                            Port('address','std_logic_vector (DATA_DEPTH - 1 downto 0)'),
                            Port('clock','std_logic', initialValue='1'),
                             Port('rden','std_logic', initialValue='1')
                            ],
                        'out': [Port('q','std_logic_vector (DATA_WIDTH - 1 downto 0)')] 
                    }

        if self.type == 'conv_bias':
            return  { 'in': [
                            Port('address','std_logic_vector (DATA_DEPTH - 1 downto 0)'),
                            Port('clken','std_logic', initialValue='1'),
                             Port('clock','std_logic', initialValue='1')
                            ],
                        'out': [Port('q','std_logic_vector (DATA_WIDTH - 1 downto 0)')] 
                    }
