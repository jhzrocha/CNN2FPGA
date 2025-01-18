from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.counter import Counter

#COMPILADO
class FullyConnectedControl(ComponentCommonMethods):
    
    #WEIGHT_ADDRESS_WIDTH - weightAddressWidth
    #BIAS_ADDRESS_WIDTH biasAddressWidth
    #ADDR_WIDTH - addWidth
    #LAST_FEATURE - lastFeature
    def __init__(self,weightAddressWidth=13, biasAddressWidth=6, addWidth=8, lastFeature='"10000000"'):
        self.weightAddressWidth = weightAddressWidth
        self.biasAddressWidth = biasAddressWidth
        self.addWidth = addWidth
        self.lastFeature = lastFeature
        self.createComponent()
        
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'fullyConnected_{self.weightAddressWidth}_{self.biasAddressWidth}_{self.addWidth}_{self.lastFeature}'
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
                                Port('o_IN_READ_ADDR','std_logic_vector (7 downto 0)')
                                   ] 
                    }
        
        self.addStateTypeOnArchitecture(name='t_STATE',
                                        states=['s_IDLE',
                                                's_BIAS_READ_ENA',
                                                's_BIAS_WRITE_ENA',
                                                's_BIAS_INC_ADDR',
                                                's_LOAD_PIX_WEIGHT',
                                                's_REG_PIX',
                                                's_REG_OUT_NFC',
                                                's_WRITE_OUT',
                                                's_LAST_UNIT',
                                                's_RST_ADDRS',
                                                's_LAST_FEATURE',
                                                's_END'])
        
        self.addInternalSignalWire('r_STATE','t_STATE')
        self.addInternalSignalWire('w_NEXT','t_STATE')

        self.addInternalSignalWire('w_IN_READ_ADDR',F'std_logic_vector ({self.addWidth-1} downto 0)')
        self.addInternalSignalWire('w_INC_IN_ADDR','std_logic')
        self.addInternalSignalWire('w_RST_IN_ADDR','std_logic')

        self.addInternalSignalWire('r_WEIGHT_ADDR',f'std_logic_vector({self.weightAddressWidth-1} downto 0)')
        self.addInternalSignalWire('w_RST_WEIGHT_ADDR','std_logic')
        self.addInternalSignalWire('w_INC_WEIGHT_ADDR','std_logic')

        self.addInternalSignalWire('r_BIAS_ADDR',f'std_logic_vector({self.biasAddressWidth-1} downto 0)')
        self.addInternalSignalWire('w_RST_BIAS_ADDR','std_logic')
        self.addInternalSignalWire('w_INC_BIAS_ADDR','std_logic')

        self.addInternalSignalWire('w_LAST_FEATURE','std_logic')

        self.addInternalSignalWire('w_LAST_UNIT','std_logic', initialValue="'0'")

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

        self.addInternalComponent(component=Counter(dataWidth=self.addWidth,
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
                                                              'i_RESET'     : 'w_INC_BUFF_OUT',# TROCADO
                                                              'i_INC'       : 'w_RST_BUFF_OUT',# TROCADO
                                                              'i_RESET_VAL' : "(others => '0')",
                                                              'o_Q'         : 'r_REG_OUT_ADDR'})
        self.internalOperations = f"""
  p_STATE : process (i_CLK, i_CLR)
  begin
    if (i_CLR = '1') then
      r_STATE <= s_IDLE; --initial state
    elsif (rising_edge(i_CLK)) then
      r_STATE <= w_NEXT; --next state
    end if;
  end process;
  p_NEXT : process (r_STATE, i_GO, r_BIAS_ADDR, w_LAST_FEATURE, w_LAST_UNIT)
  begin
    case (r_STATE) is
      when s_IDLE => -- aguarda sinal go                 
        if (i_GO = '1') then
          w_NEXT <= s_BIAS_READ_ENA;
        else
          w_NEXT <= s_IDLE;
        end if;

      when s_BIAS_READ_ENA => -- havilita leitura de BIAS
        w_NEXT <= s_BIAS_WRITE_ENA;

      when s_BIAS_WRITE_ENA => -- havilita escrita de BIAS
        w_NEXT <= s_BIAS_INC_ADDR;

      when s_BIAS_INC_ADDR => -- incrementa contgador BIAS
        w_NEXT <= s_LOAD_PIX_WEIGHT;

      when s_LOAD_PIX_WEIGHT => -- habilita leitura pixel de entrada
        w_NEXT <= s_REG_PIX;

      when s_REG_PIX => -- registra pixel de entrada        
        w_NEXT <= s_REG_OUT_NFC;

      when s_REG_OUT_NFC => -- registra saida
        w_NEXT <= s_LAST_FEATURE;

      when s_LAST_FEATURE => -- verifica fim linhas
        if (w_LAST_FEATURE = '1') then
          w_NEXT <= s_WRITE_OUT;
        else
          w_NEXT <= s_LOAD_PIX_WEIGHT;
        end if;

      when s_WRITE_OUT =>
        w_NEXT <= s_LAST_UNIT;

      when s_LAST_UNIT =>
        if (w_LAST_UNIT = '1') then
          w_NEXT <= s_END;
        else
          w_NEXT <= s_BIAS_READ_ENA;
        end if;

      when s_END => -- fim
        w_NEXT <= s_IDLE;

      when others =>
        w_NEXT <= s_IDLE;

    end case;
  end process;

  --- sinais para ROM de pesos, bias e scale/ cache de pesos, registradores de bias e scale
  -- enderecametno do bias
  w_RST_BIAS_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else
    '0';
  w_INC_BIAS_ADDR <= '1' when (r_STATE = s_BIAS_INC_ADDR) else
    '0';

      -- ENDERECO PARA ROM BIAS
  o_BIAS_READ_ADDR <= r_BIAS_ADDR;

  -- sinaliza quando contador chegar a 34
  w_LAST_UNIT <= '1' when (r_BIAS_ADDR = "100010") else
    '0'; -- 0 to 34 

  -- habilita registradores de scale e bias
  o_REG_BIAS_ENA <= '1' when (r_STATE = s_BIAS_WRITE_ENA) else
    '0';

  -- sinais durante processamento       
  -- enderecamento dos pesos
  w_RST_WEIGHT_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else
    '0';
  w_INC_WEIGHT_ADDR <= '1' when (r_STATE = s_REG_PIX) else
    '0';

      -- ENDERECO PARA ROM PESOS
  o_WEIGHT_READ_ADDR <= r_WEIGHT_ADDR;
  ---------------------------------
  -- sinais para buffers de entrada
  ---------------------------------  
  w_INC_IN_ADDR <= '1' when (r_STATE = s_REG_PIX) else
    '0';
  w_RST_IN_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else
    '0';

      o_IN_READ_ADDR <= w_IN_READ_ADDR;

  w_LAST_FEATURE <= '1' when (w_IN_READ_ADDR = {self.lastFeature}) else
    '0';

  -- sinais de inc/rst
  w_INC_BUFF_OUT <= '1' when (r_STATE = s_LAST_UNIT) else
    '0';
  w_RST_BUFF_OUT <= '1' when (r_STATE = s_IDLE) else
    '0';

      o_REG_OUT_ADDR <= r_REG_OUT_ADDR;
  ---------------------------------
  ---------------------------------
  -- habilita registradores de pixel e peso
  o_REG_PIX_ENA <= '1' when (r_STATE = s_REG_PIX) else
    '0';
  o_REG_WEIGHT_ENA <= '1' when (r_STATE = s_REG_PIX) else
    '0';
  -- habilita acumulador
  o_ACC_ENA <= '1' when (r_STATE = s_REG_OUT_NFC) else
    '0';
  o_ACC_CLR <= '1' when (r_STATE = s_IDLE) else
    '0';

  -- habilita/clear registrador de saida
  o_REG_OUT_ENA <= '1' when (r_STATE = s_WRITE_OUT) else
    '0';
  -- sinaliza fim do processamento
  o_READY <= '1' when (r_STATE = s_END) else
    '0';
        """
        
        self.OutputEntityAndArchitectureFile()



