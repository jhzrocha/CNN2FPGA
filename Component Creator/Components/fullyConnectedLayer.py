from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.fullyConnectedControl import FullyConnectedControl
from Components.fullyConnectedOperator import FullyConnectedOperator
from Components.genericMultiplexer import Multiplexer
from Components.registrador import Registrador
from MemoryInitializationComponents.memoryInitializationComponent import MemoryInitializationComponent

class FullyConnectedLayer(ComponentCommonMethods):
    
    def __init__(self, dataWidth=8, numUnits=2, scaleShift=7, weightsFileDataWidth=8, biasFileName =None, biasFileDataWidth=32,qtInputs = 64, 
                 functionActivation='RELU', qtNeuronsPerLayer=[4,5,6]):
        self.dataWidth = dataWidth
        self.qtNeuronsPerLayer = qtNeuronsPerLayer

        self.weightAddressWidth = len(bin(qtInputs)[2:])
        self.biasAddressWidth = len(bin(sum(self.qtNeuronsPerLayer))[2:])
        
        self.numUnits = numUnits
        self.scaleShift = scaleShift

        self.weightsFileDataWidth = weightsFileDataWidth

        self.biasFileName = biasFileName if biasFileName != None else 'bias.mif'
        self.biasFileDataWidth = biasFileDataWidth
        
        self.qtInputs = qtInputs
        self.qtInputAddr = len(bin(qtInputs)[2:])
        
        self.functionActivation = functionActivation

        self.qtNeurons = sum(self.qtNeuronsPerLayer)
        self.qtMaxQtNeuronsOnLayer = max(self.qtNeuronsPerLayer)
        self.qtNeuronsLayers = len(self.qtNeuronsPerLayer)

        self.createComponent()
    
    
    def createComponent(self):
        self.startInstance()
        self.minimalComponentFileName = f'FullyConnectedLayer_{self.dataWidth}dw_{self.numUnits}un_{self.qtNeuronsLayers}l{self.qtNeurons}n_{self.functionActivation}_{self.weightsFileDataWidth}wfdw'
        
        self.fullyConnectedOperator = FullyConnectedOperator(nrUnits=self.numUnits, 
                                                                   biasAddressWidth=self.biasAddressWidth, 
                                                                   scaleShift=self.scaleShift, 
                                                                   dataWidth =self.dataWidth,
                                                                   functionActivationType=self.functionActivation)
        
        self.inputMultiplexer = Multiplexer(dataWidth=self.dataWidth, qtInputs=self.qtInputs)
               
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic'),
                                Port('i_PIX',self.inputMultiplexer.getPortDataType('i_A'), initialValue = "(others => (others => '0'))"),
                                ],
                            'out': [
                                Port(name='o_PIX',dataType= self.fullyConnectedOperator.getPortDataType('o_PIX'), initialValue="(others => (others => '0'))"),
                                Port(name='o_READ_ADDR',dataType=f"std_logic_vector({self.qtInputAddr-1} downto 0)"),
                                Port(name='o_READY',dataType=f"std_logic")
                                   ] 
                    }
        
        self.addInternalSignalWire(name='w_REG_PIX_ENA',      dataType=f"std_logic")
        self.addInternalSignalWire(name='w_REG_WEIGHT_ENA',   dataType=f"std_logic")
        self.addInternalSignalWire(name='w_REG_BIAS_ENA',     dataType=f"std_logic")
        self.addInternalSignalWire(name='w_ACC_ENA',          dataType=f"std_logic")
        self.addInternalSignalWire(name='w_ACC_CLR',          dataType=f"std_logic")
        self.addInternalSignalWire(name='w_REG_OUT_ENA',      dataType=f"std_logic")
        self.addInternalSignalWire(name='w_REG_OUT_ADDR',     dataType=f"std_logic_vector(5 downto 0)"                                         ,initialValue= "(others => '0')")
        self.addInternalSignalWire(name='w_WEIGHT_READ_ADDR', dataType=f"std_logic_vector({self.weightAddressWidth-1} downto 0)")
        self.addInternalSignalWire(name='w_BIAS_READ_ADDR',   dataType=f"std_logic_vector({self.biasAddressWidth-1} downto 0)")
        wweightPort = self.fullyConnectedOperator.getPort(('i_WEIGHT'))
        self.addInternalSignalWire(name='w_WEIGHT',           dataType=wweightPort.getdataType() ,initialValue= wweightPort.initialValue)
        self.addInternalSignalWire(name='w_BIAS_SCALE',       dataType=f"std_logic_vector(31 downto 0)")
        
        self.addInternalSignalWire(name='w_PIX',              dataType=self.fullyConnectedOperator.getPortDataType('i_PIX'))
        
        self.addInternalSignalWire(name='w_IN_READ_ADDR',         dataType=f"std_logic_vector({self.qtInputAddr-1} downto 0)")
        self.addInternalSignalWire(name='w_SEL_REG_INT',         dataType=f"std_logic_vector({len(bin(self.qtMaxQtNeuronsOnLayer)[2:])-1} downto 0)")
        self.addInternalSignalWire(name='w_SEL_INPUT_OR_IN_REG',      dataType=f"std_logic")

        self.addInternalSignalWire(name='w_OPERATOR_OUTPUT',dataType= self.fullyConnectedOperator.getPortDataType('o_PIX'), initialValue="(others => (others => '0'))"),
        self.addInternalSignalWire(name='w_INPUT_OR_REG',dataType= f"array (0 to 1) of std_logic_vector ({self.dataWidth-1} downto 0)", initialValue="(others => (others => '0'))"),

        self.addInternalSignalWire(name='w_FC_OPERATOR_OUTPUT',dataType=self.fullyConnectedOperator.getPortDataType('o_PIX'), initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_ROM_OUT',          dataType=f"std_logic_vector ({self.dataWidth-1} downto 0)"                           , initialValue= "(others => '0')")

        self.addInternalComponent(component=self.inputMultiplexer,
                                    componentCallName='u_INPUTS_MUX',
                                    portmap={'i_A':'i_PIX',
                                             'i_SEL': 'w_IN_READ_ADDR',
                                             'o_Q':'w_INPUT_OR_REG(0)'})

        self.internalRegistersMultiplexer = Multiplexer(dataWidth=self.dataWidth, qtInputs=self.qtMaxQtNeuronsOnLayer)
        self.addInternalComponent(component=self.internalRegistersMultiplexer,
                            componentCallName='u_REG_IN_MUX',
                            portmap={'i_A'  : 'w_OUTPUT_REG_INT',
                                     'i_SEL': 'w_SEL_REG_INT',
                                     'o_Q'  : 'w_INPUT_OR_REG(1)'})
        
        self.addInternalComponent(component=MemoryInitializationComponent(type='conv_bias',
                                                                          initFileName= self.biasFileName,
                                                                         dataWidth=self.biasFileDataWidth,
                                                                         dataDepth=self.biasAddressWidth),
                                    componentCallName='u_ROM_BIAS',
                                    portmap={'address':'w_BIAS_READ_ADDR',
                                             'clken':"'1'",
                                             'clock':"i_CLK",
                                             'q':'w_BIAS_SCALE'})

        self.addInternalComponent(component=FullyConnectedControl(qtInputs=self.qtInputs,
                                                                  qtNeuronsPerLayer = self.qtNeuronsPerLayer),
                                    componentCallName='u_CONTROLE',
                                    portmap={'i_CLK': 'i_CLK',
                                            'i_CLR' : 'i_CLR',
                                            'i_GO' : 'i_GO',
                                            'o_READY' : 'o_READY',
                                            'o_REG_PIX_ENA' : 'w_REG_PIX_ENA',
                                            'o_REG_WEIGHT_ENA' : 'w_REG_WEIGHT_ENA',
                                            'o_REG_BIAS_ENA' : 'w_REG_BIAS_ENA',
                                            'o_ACC_ENA' : 'w_ACC_ENA',
                                            'o_ACC_CLR' : 'w_ACC_CLR',
                                            'o_REG_OUT_ENA' : 'w_REG_OUT_ENA',
                                            'o_REG_OUT_ADDR' : 'w_REG_OUT_ADDR',
                                            'o_WEIGHT_READ_ADDR' : 'w_WEIGHT_READ_ADDR',
                                            'o_BIAS_READ_ADDR' : 'w_BIAS_READ_ADDR',
                                            'o_IN_READ_ADDR' : 'w_IN_READ_ADDR'})
        
        self.addInternalComponent(component=self.fullyConnectedOperator,
                                    componentCallName='u_OPERACIONAL',
                                    portmap={
                                            'i_CLK':'i_CLK',
                                            'i_CLR':'i_CLR',
                                            'i_PIX':'w_PIX',
                                            'i_WEIGHT':'w_WEIGHT',
                                            'i_REG_PIX_ENA':'w_REG_PIX_ENA',
                                            'i_REG_WEIGHT_ENA':'w_REG_WEIGHT_ENA',
                                            'i_BIAS_SCALE':'w_BIAS_SCALE',
                                            'i_REG_BIAS_ADDR':'w_BIAS_READ_ADDR',
                                            'i_REG_BIAS_ENA':'w_REG_BIAS_ENA',
                                            'i_REG_OUT_CLR' : "'0'",
                                            'i_ACC_ENA':'w_ACC_ENA',
                                            'i_ACC_CLR':'w_ACC_CLR',
                                            'i_REG_OUT_ENA':'w_REG_OUT_ENA',
                                            'i_REG_OUT_ADDR':'w_REG_OUT_ADDR',
                                            'o_PIX':'w_FC_OPERATOR_OUTPUT'        
                                    })
        self.addInternalSignalWire(name=f'w_ENA_REG_INT', dataType=f"std_logic_vector ({self.qtMaxQtNeuronsOnLayer-1} downto 0)")
        self.addInternalSignalWire(name=f'w_OUTPUT_REG_INT', dataType=self.internalRegistersMultiplexer.getPortDataType('i_A'))

        self.createWeightROMComponents()
        self.createInternalRegisters()
       
        self.internalOperations = f"""
        o_READ_ADDR <= w_IN_READ_ADDR;
        w_WEIGHT{f"(0)" if self.numUnits>1 else ""}<= w_ROM_OUT;

        w_PIX <= w_INPUT_OR_REG(1) when (w_SEL_INPUT_OR_IN_REG = '1') else w_INPUT_OR_REG(0);
        w_OPERATOR_OUTPUT <= w_FC_OPERATOR_OUTPUT;

        o_PIX <= w_FC_OPERATOR_OUTPUT;
           """
        self.OutputEntityAndArchitectureFile()

    def createInternalRegisters(self):
        for i in range(0, self.qtMaxQtNeuronsOnLayer-1):
            self.addInternalComponent(component=Registrador(dataWidth=self.dataWidth),
                            componentCallName=f'u_REG_INT_{i}',
                            portmap={ 'i_CLK' : 'i_CLK',
                                    'i_CLR' : 'i_CLR',
                                    'i_ENA' : f'w_ENA_REG_INT({i})',
                                    'i_A'   : f'w_OPERATOR_OUTPUT({i})',
                                    'o_Q'   : f'w_OUTPUT_REG_INT({i})'})

    def createWeightROMComponents(self):
        for i in range(0, self.qtNeuronsLayers):
            dataDepth=0
            if i == 0:
                dataDepth = len(bin(self.qtInputs)[2:])
            else:
                dataDepth = len(bin(self.qtNeuronsPerLayer[i-1])[2:])
            
            self.addInternalComponent(component=MemoryInitializationComponent(type='conv_weights',
                                                                            initFileName= f'fc_weights_{i}.mif',
                                                                            dataWidth=self.weightsFileDataWidth,
                                                                            dataDepth=dataDepth),
                                        componentCallName= f'u_ROM_WEIGHTS_{i}',
                                        portmap={'address':'w_WEIGHT_READ_ADDR',
                                                'clock':'i_CLK',
                                                'rden':"'1'",
                                                'q':f'w_WEIGHT_ROM_MEMORY_OUT({i})'})
            
        self.weightMultiplexer = Multiplexer(dataWidth=self.dataWidth, 
                                                            qtInputs=self.qtNeuronsLayers)
        self.addInternalComponent(component=self.weightMultiplexer,
                                  componentCallName='u_WEIGHTS_MUX',
                                    portmap={'i_A'  : 'w_WEIGHT_ROM_MEMORY_OUT',
                                     'i_SEL': 'w_WEIGHT_LAYER_SEL',
                                     'o_Q'  : 'w_ROM_OUT'})
        self.addInternalSignalWire(name='w_WEIGHT_ROM_MEMORY_OUT',          
                                   dataType=self.weightMultiplexer.getPortDataType('i_A'), 
                                   initialValue= "(others => (others => '0'))")
        self.addInternalSignalWire(name='w_WEIGHT_LAYER_SEL',dataType=f"std_logic_vector({len(bin(self.qtNeuronsLayers)[2:])-1} downto 0)", initialValue="(others => '0')")

