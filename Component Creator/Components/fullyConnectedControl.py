from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.counter import Counter

#COMPILADO
class FullyConnectedControl(ComponentCommonMethods):
    
    #WEIGHT_ADDRESS_WIDTH - weightAddressWidth
    #BIAS_ADDRESS_WIDTH biasAddressWidth
    #ADDR_WIDTH - addWidth
    #LAST_FEATURE - lastFeature
    def __init__(self, qtInputs = 128, qtNeuronsPerLayer = [1,2,3,4]):
        self.weightAddressWidth = len(bin(qtInputs)[2:])
        self.qtNeurons = sum(qtNeuronsPerLayer)
        self.qtMaxNeuronsPerLayer = max(qtNeuronsPerLayer)
        self.biasAddressWidth = len(bin(self.qtNeurons)[2:])
        self.lastFeature = bin(qtInputs)[2:]
        self.WidthAddrInput = len(bin(qtInputs)[2:])
        self.qtNeuronLayers = len(qtNeuronsPerLayer)

        self.qtNeuronsPerLayer = qtNeuronsPerLayer
        self.createComponent()
        
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'fullyConnectedControl_{self.weightAddressWidth}_{self.biasAddressWidth}'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic')
                                ],
                            'out': [
                                Port('o_READY','std_logic'),
                                Port('o_REG_PIX_ENA','std_logic'),
                                Port('o_REG_WEIGHT_ENA','std_logic'),
                                Port('o_REG_BIAS_ENA','std_logic'),
                                Port('o_ACC_ENA','std_logic'),
                                Port('o_ACC_CLR','std_logic'),
                                Port('o_REG_OUT_ENA','std_logic'),
                                Port('o_REG_OUT_ADDR','std_logic_vector(5 downto 0)', initialValue="(others => '0')"),
                                Port('o_WEIGHT_READ_ADDR',f'std_logic_vector({self.weightAddressWidth-1} downto 0)'),
                                Port('o_BIAS_READ_ADDR',f'std_logic_vector({self.biasAddressWidth-1} downto 0)'),
                                Port('o_ACT_FUNCT_ENA','std_logic'),
                                Port('o_IN_READ_ADDR',f'std_logic_vector ({self.WidthAddrInput-1} downto 0)')
                                   ] 
                    }
        
        self.addStateTypeOnArchitecture(name='t_STATE',
                                        states=['s_IDLE',
                                                's_LOAD_INPUT',
                                                's_LOAD_WEIGHT',
                                                's_ENABLE_NEURON_ACC',
                                                's_INC_WEIGHT_AND_INPUT',
                                                's_LOAD_BIAS',
                                                's_ENABLE_BIAS_TO_SUM',
                                                's_ENABLE_FUNCTION',
                                                's_ENABLE_REG_OUT',
                                                's_BIAS_INC_ADDR',
                                                's_ADD_LAYER_COUNTER',
                                                's_ENABLE_INTERNAL_REG',
                                                's_IS_LAST_LAYER',
                                                's_END'])
        
        self.addInternalSignalWire('r_STATE','t_STATE')
        self.addInternalSignalWire('w_NEXT','t_STATE')

        self.addInternalSignalWire('w_IN_READ_ADDR',f'std_logic_vector ({self.WidthAddrInput-1} downto 0)')
        self.addInternalSignalWire('w_INC_IN_ADDR','std_logic')
        self.addInternalSignalWire('w_RST_IN_ADDR','std_logic')
        self.addInternalSignalWire('w_RST_NEURON_ON_LAYER_COUNTER','std_logic')


        self.addInternalSignalWire('r_WEIGHT_ADDR',f'std_logic_vector({self.weightAddressWidth-1} downto 0)')
        self.addInternalSignalWire('r_LAYER_COUNTER',f'std_logic_vector({len(bin(self.qtNeuronLayers)[2:])-1} downto 0)')
        self.addInternalSignalWire('r_NEURON_COUNTER',f'std_logic_vector({len(bin(self.qtMaxNeuronsPerLayer)[2:])-1} downto 0)')


        self.addInternalSignalWire('w_RST_WEIGHT_ADDR','std_logic')
        self.addInternalSignalWire('w_INC_WEIGHT_ADDR','std_logic')
        self.addInternalSignalWire('w_INC_LAYER_COUNTER','std_logic')
        self.addInternalSignalWire('w_INC_NEURON_COUNTER','std_logic')


        self.addInternalSignalWire('r_BIAS_ADDR',f'std_logic_vector({self.biasAddressWidth-1} downto 0)')
        self.addInternalSignalWire('w_RST_BIAS_ADDR','std_logic')
        self.addInternalSignalWire('w_INC_BIAS_ADDR','std_logic')

        self.addInternalSignalWire('w_LAST_WEIGHT','std_logic', initialValue="'0'")
        self.addInternalSignalWire('w_LAST_LAYER','std_logic', initialValue="'0'")

        self.addInternalSignalWire('w_LAST_NEURON','std_logic', initialValue="'0'")

        self.addInternalSignalWire('r_REG_OUT_ADDR','std_logic_vector(5 downto 0)', initialValue="(others => '0')")
        self.addInternalSignalWire('w_INC_BUFF_OUT','std_logic', initialValue="'0'")
        self.addInternalSignalWire('w_RST_BUFF_OUT','std_logic', initialValue="'0'")

        self.addInternalComponent(component=Counter(dataWidth=self.biasAddressWidth,
                                                    bitStep=1),
                                                    componentCallName='u_BIAS_ADDR',
                                                    portmap={ 'i_CLK'       : 'i_CLK',
                                                              'i_RESET'     : 'w_RST_BIAS_ADDR',
                                                              'i_INC'       : 'w_INC_BIAS_ADDR',
                                                              'i_RESET_VAL' : "(others => '0')",
                                                              'o_Q'         : 'r_BIAS_ADDR'})

        self.addInternalComponent(component=Counter(dataWidth=self.weightAddressWidth,
                                                    bitStep=1),
                                                    componentCallName='u_WEIGHT_ADDR',
                                                    portmap={ 'i_CLK'       : 'i_CLK',
                                                              'i_RESET'     : 'w_RST_WEIGHT_ADDR',
                                                              'i_INC'       : 'w_INC_WEIGHT_ADDR',
                                                              'i_RESET_VAL' : "(others => '0')",
                                                              'o_Q'         : 'r_WEIGHT_ADDR'})

        self.addInternalComponent(component=Counter(dataWidth=self.WidthAddrInput,
                                                    bitStep=1),
                                                    componentCallName='u_INPUT_ADDR',
                                                    portmap={ 'i_CLK'       : 'i_CLK',
                                                              'i_RESET'     : 'w_RST_IN_ADDR',
                                                              'i_INC'       : 'w_INC_IN_ADDR',
                                                              'i_RESET_VAL' : "(others => '0')",
                                                              'o_Q'         : 'w_IN_READ_ADDR'})
        
        self.addInternalComponent(component=Counter(dataWidth=6,
                                                    bitStep=1),
                                                    componentCallName='u_REG_OUT_ADDR',
                                                    portmap={ 'i_CLK'       : 'i_CLK',
                                                              'i_RESET'     : 'w_RST_BUFF_OUT',
                                                              'i_INC'       : 'w_INC_BUFF_OUT',
                                                              'i_RESET_VAL' : "(others => '0')",
                                                              'o_Q'         : 'r_REG_OUT_ADDR'})
        
        self.addInternalComponent(component=Counter(dataWidth=len(bin(self.qtNeuronLayers)[2:]),
                                            bitStep=1),
                                            componentCallName='u_LAYER_COUNTER',
                                            portmap={ 'i_CLK'       : 'i_CLK',
                                                      'i_RESET'     : 'i_CLR',
                                                      'i_INC'       : 'w_INC_LAYER_COUNTER',
                                                      'i_RESET_VAL' : "(others => '0')",
                                                      'o_Q'         : 'r_LAYER_COUNTER'})
        
        self.addInternalComponent(component=Counter(dataWidth=len(bin(self.qtMaxNeuronsPerLayer)[2:]),
                                    bitStep=1),
                                    componentCallName='u_NEURON_ON_LAYER',
                                    portmap={ 'i_CLK'       : 'i_CLK',
                                              'i_RESET'     : 'w_RST_NEURON_ON_LAYER_COUNTER',
                                              'i_INC'       : 'w_INC_NEURON_COUNTER',
                                              'i_RESET_VAL' : "(others => '0')",
                                              'o_Q'         : 'r_NEURON_COUNTER'})
        self.createQtNeuronsPerLayerOnConstant()
        self.internalOperations = f"""
  p_STATE : process (i_CLK, i_CLR)
  begin
    if (i_CLR = '1') then
      r_STATE <= s_IDLE; --initial state
    elsif (rising_edge(i_CLK)) then
      r_STATE <= w_NEXT; --next state
    end if;
  end process;

  p_NEXT : process (r_STATE, i_GO, r_BIAS_ADDR, w_LAST_NEURON, w_LAST_WEIGHT)
    variable lastNeuronOnLayer : std_logic_vector ({len(bin(max(self.qtNeuronsPerLayer))[2:])-1} downto 0);
    variable layerIndex : integer range 0 to {len(self.qtNeuronsPerLayer)-1};
    variable lastLayer : std_logic_vector ({len(bin(self.qtNeuronLayers)[2:])-1} downto 0);

  begin
    layerIndex := to_integer(unsigned(r_LAYER_COUNTER));
    lastNeuronOnLayer := std_logic_vector(qtNeuronsPerLayer_lut(layerIndex));
    lastLayer := "{bin(self.qtNeuronLayers)[2:].zfill(len(bin(self.qtNeuronLayers)[2:]))}";
    
    case (r_STATE) is
      when s_IDLE => -- aguarda sinal go                 
        if (i_GO = '1') then
          w_NEXT <= s_LOAD_INPUT;
        else
          w_NEXT <= s_IDLE;
        end if;

      when s_LOAD_INPUT =>
	      w_NEXT <= s_LOAD_WEIGHT;

      when s_LOAD_WEIGHT =>
	      w_NEXT <= s_ENABLE_NEURON_ACC;

      when s_ENABLE_NEURON_ACC =>
        if (w_LAST_WEIGHT = '1') then
          w_NEXT <= s_LOAD_BIAS;
        else
          w_NEXT <= s_INC_WEIGHT_AND_INPUT;
        end if;
      
      when s_INC_WEIGHT_AND_INPUT =>
        w_NEXT <= s_LOAD_INPUT;

      when s_LOAD_BIAS =>
	      w_NEXT <= s_ENABLE_BIAS_TO_SUM;

      when s_ENABLE_BIAS_TO_SUM =>
	      w_NEXT <= s_ENABLE_FUNCTION;

      when s_ENABLE_FUNCTION =>
	      w_NEXT <= s_ENABLE_REG_OUT;

      when s_ENABLE_REG_OUT =>
	      if (r_NEURON_COUNTER = lastNeuronOnLayer) then
          w_NEXT <= s_IS_LAST_LAYER;
        else
          w_NEXT <= s_BIAS_INC_ADDR;
        end if;

      when s_IS_LAST_LAYER =>
        if (r_LAYER_COUNTER = lastLayer) then
            w_NEXT <= s_END;
        else
            w_NEXT <= s_ENABLE_INTERNAL_REG;
        end if;

      when s_ENABLE_INTERNAL_REG =>
       w_NEXT <= s_ADD_LAYER_COUNTER;

      when s_ADD_LAYER_COUNTER =>
      w_NEXT <= s_LOAD_INPUT;

      when s_BIAS_INC_ADDR =>
	      w_NEXT <= s_LOAD_INPUT;

      when others =>
        w_NEXT <= s_IDLE;

    end case;
  end process;

  -- CLEAR 
  w_RST_BIAS_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else '0';
  w_RST_WEIGHT_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else '0';
  w_RST_IN_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else '0';
  w_RST_BUFF_OUT <= '1' when (r_STATE = s_IDLE) else '0';
  w_RST_NEURON_ON_LAYER_COUNTER <= '1' when (r_STATE = s_IS_LAST_LAYER) else '0';
  o_ACC_CLR <= '1' when (r_STATE = s_IDLE) else '0';

  -- ADDRS
  o_WEIGHT_READ_ADDR <= r_WEIGHT_ADDR;
  o_IN_READ_ADDR <= w_IN_READ_ADDR;
  o_REG_OUT_ADDR <= r_REG_OUT_ADDR;
  o_BIAS_READ_ADDR <= r_BIAS_ADDR;

  -- INCREMENTS  
  w_INC_BIAS_ADDR <= '1' when (r_STATE = s_BIAS_INC_ADDR) else '0';
  w_INC_WEIGHT_ADDR <= '1' when (r_STATE = s_INC_WEIGHT_AND_INPUT) else '0';
  w_INC_IN_ADDR <= '1' when (r_STATE = s_INC_WEIGHT_AND_INPUT) else '0';
  w_INC_BUFF_OUT <= '1' when (r_STATE = s_BIAS_INC_ADDR) else '0';
  w_INC_NEURON_COUNTER <= '1' when (r_STATE = s_BIAS_INC_ADDR) else '0';
  w_INC_LAYER_COUNTER <= '1' when (r_STATE = s_ADD_LAYER_COUNTER) else '0';
  
  -- ENABLERS
  o_REG_BIAS_ENA <= '1' when (r_STATE = s_LOAD_BIAS) else '0';
  o_ACT_FUNCT_ENA <= '1' when (r_STATE = s_ENABLE_FUNCTION) else '0';  
  o_REG_PIX_ENA <= '1' when (r_STATE = s_LOAD_INPUT) else '0';
  o_REG_WEIGHT_ENA <= '1' when (r_STATE = s_LOAD_WEIGHT) else '0';
  o_ACC_ENA <= '1' when (r_STATE = s_ENABLE_NEURON_ACC) else '0';
  o_REG_OUT_ENA <= '1' when (r_STATE = s_ENABLE_REG_OUT) else '0';
  
  -- LAST CONTROLLERS
  w_LAST_NEURON <= '1' when (r_BIAS_ADDR = "{bin(self.qtNeurons)[2:]}") else '0';
  w_LAST_WEIGHT <= '1' when (r_WEIGHT_ADDR = "{self.lastFeature}") else '0';
  w_LAST_LAYER <= '1' when (r_LAYER_COUNTER = "{bin(self.qtNeuronLayers)[2:]}") else '0';
  
  -- END
  o_READY <= '1' when (r_STATE = s_END) else '0';
  
  """
        
        self.OutputEntityAndArchitectureFile()


    def createQtNeuronsPerLayerOnConstant(self):
      qtBitsOnConstant = len(bin(max(self.qtNeuronsPerLayer))[2:])
      value = '('
      for i in range(0, len(self.qtNeuronsPerLayer)):
        value = value + f'''{i}   => to_unsigned({self.qtNeuronsPerLayer[i]},{qtBitsOnConstant}), \n'''
      value = value[:-3] + ')'
      self.addArrayTypeOnArchitecture(name='lut_array',datatype=f'unsigned({qtBitsOnConstant-1} downto 0)',size=len(self.qtNeuronsPerLayer))
      self.addInternalConstant(name='qtNeuronsPerLayer_lut', dataType="lut_array", value= value)