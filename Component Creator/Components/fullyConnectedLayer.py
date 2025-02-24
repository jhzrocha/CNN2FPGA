from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.fullyConnectedControl import FullyConnectedControl
from Components.fullyConnectedOperator import FullyConnectedOperator
from MemoryInitializationComponents.memoryInitializationComponent import MemoryInitializationComponent

class FullyConnectedLayer(ComponentCommonMethods):
    
    #BIAS_ADDRESS_WIDTH    : integer          := 6;               -- numero de bits para enderecar registradores de bias e scales    
    #NUM_WEIGHT_FILTER_CHA : std_logic_vector := "1000";          -- quantidade de peso por filtro por canal(R*S) (de 0 a 8)
    #LAST_WEIGHT           : std_logic_vector := "1000110000000"; -- quantidade de pesos (27) !! QUANTIDADE PESOS POR FILTRO (R*S*C) !!
    #LAST_BIAS             : std_logic_vector := "100100";        -- 35 bias + 1 scale
    #LAST_FEATURE          : std_logic_vector := "10000000";      -- 128 pixels     
    #NUM_CHANNELS          : integer          := 64;
    #NUM_UNITS             : integer          := 1;
    #SCALE_SHIFT           : integer          := 7
    def __init__(self, dataWidth=8, addWidth=8, weightAddressWidth=13, biasAddressWidth=6,numWeightFilterCha='"1000"', lastWeight='"1000110000000"', lastBias='"100100"', lastFeature='"10000000"',
                 numChannels=64, numUnits=2, scaleShift=7, weightsFileName='', weightsFileDataWidth=8, biasFileName ='', biasFileDataWidth=32):
        self.dataWidth = dataWidth
        self.addWidth = addWidth
        self.weightAddressWidth = weightAddressWidth
        self.biasAddressWidth = biasAddressWidth
        self.numWeightFilterCha = numWeightFilterCha
        self.lastWeight = lastWeight
        self.lastBias = lastBias
        self.lastFeature = lastFeature
        self.numChannels = numChannels
        self.numUnits = numUnits
        self.scaleShift = scaleShift
        self.weightsFileName = weightsFileName
        self.weightsFileDataWidth = weightsFileDataWidth
        self.biasFileName = biasFileName
        self.biasFileDataWidth = biasFileDataWidth
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'FullyConnectedLayer'
        
        self.fullyConnectedOperator = FullyConnectedOperator(nrUnits=self.numUnits, 
                                                                   biasAddressWidth=self.biasAddressWidth, 
                                                                   scaleShift=self.scaleShift, 
                                                                   dataWidth =self.dataWidth)
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic'),
                                Port('i_PIX',f'std_logic_vector({self.dataWidth-1} downto 0)', initialValue="(others => '0')")
                                ],
                            'out': [
                                Port(name='o_PIX',dataType= self.fullyConnectedOperator.getPortDataType('o_PIX'), initialValue="(others => (others => '0'))"),
                                Port(name='o_READ_ADDR',dataType=f"std_logic_vector(7 downto 0)"),
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
        self.addInternalSignalWire(name='w_IN_READ_ADDR',     dataType=f"std_logic_vector (7 downto 0)")
        wweightDataType = self.fullyConnectedOperator.getPortDataType(('i_WEIGHT'))
        self.addInternalSignalWire(name='w_WEIGHT',           dataType=wweightDataType ,initialValue= "(others => (others => '0'))" if 'array' in wweightDataType else "(others => '0')")
        self.addInternalSignalWire(name='w_ROM_OUT',          dataType=f"std_logic_vector ({self.dataWidth-1} downto 0)"                           , initialValue= "(others => '0')")
        self.addInternalSignalWire(name='w_BIAS_SCALE',       dataType=f"std_logic_vector(31 downto 0)")

        self.addInternalComponent(component=MemoryInitializationComponent(type='conv_weights',
                                                                          initFileName= self.weightsFileName,
                                                                         dataWidth=self.weightsFileDataWidth,
                                                                         dataDepth=self.weightAddressWidth),
                                    componentCallName='u_ROM_WEIGHTS',
                                    portmap={'address':'w_WEIGHT_READ_ADDR',
                                             'clock':'i_CLK',
                                             'rden':"'1'",
                                             'q':'w_ROM_OUT'})
        
        self.addInternalComponent(component=MemoryInitializationComponent(type='conv_bias',
                                                                          initFileName= self.biasFileName,
                                                                         dataWidth=self.biasFileDataWidth,
                                                                         dataDepth=self.biasAddressWidth),
                                    componentCallName='u_ROM_BIAS',
                                    portmap={'address':'w_BIAS_READ_ADDR',
                                             'clken':"'1'",
                                             'clock':"i_CLK",
                                             'q':'w_BIAS_SCALE'})
        self.addInternalComponent(component=FullyConnectedControl(weightAddressWidth=self.weightAddressWidth, 
                                                                  biasAddressWidth=self.biasAddressWidth, 
                                                                  addWidth=self.addWidth, 
                                                                  lastFeature=self.lastFeature),
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
                                            'i_PIX':'i_PIX',
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
                                            'o_PIX':'o_PIX'        
                                    })
        self.internalOperations = f"""
  o_READ_ADDR <= w_IN_READ_ADDR;
  w_WEIGHT{f"(0)" if self.numUnits>1 else ""}<= w_ROM_OUT;
        """
        self.OutputEntityAndArchitectureFile()



