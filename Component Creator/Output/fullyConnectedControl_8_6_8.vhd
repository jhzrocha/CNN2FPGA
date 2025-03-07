library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity fullyConnectedControl_8_6_8 is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              o_READY : out std_logic;
              o_REG_PIX_ENA : out std_logic;
              o_REG_WEIGHT_ENA : out std_logic;
              o_REG_BIAS_ENA : out std_logic;
              o_ACC_ENA : out std_logic;
              o_ACC_CLR : out std_logic;
              o_REG_OUT_ENA : out std_logic;
              o_REG_OUT_ADDR : out std_logic_vector(5 downto 0):= (others => '0');
              o_WEIGHT_READ_ADDR : out std_logic_vector(7 downto 0);
              o_BIAS_READ_ADDR : out std_logic_vector(5 downto 0);
              o_ACT_FUNCT_ENA : out std_logic;
              o_IN_READ_ADDR : out std_logic_vector (7 downto 0)
        );
    end fullyConnectedControl_8_6_8;
                 
    architecture arc of fullyConnectedControl_8_6_8 is

            type t_STATE is (
              s_IDLE,
          s_LOAD_INPUT,
          s_LOAD_WEIGHT,
          s_ENABLE_NEURON_ACC,
          s_INC_WEIGHT_AND_INPUT,
          s_LOAD_BIAS,
          s_ENABLE_BIAS_TO_SUM,
          s_ENABLE_FUNCTION,
          s_ENABLE_REG_OUT,
          s_BIAS_INC_ADDR,
          s_END
            );
        signal r_STATE : t_STATE;
        signal w_NEXT : t_STATE;
        signal w_IN_READ_ADDR : std_logic_vector (7 downto 0);
        signal w_INC_IN_ADDR : std_logic;
        signal w_RST_IN_ADDR : std_logic;
        signal r_WEIGHT_ADDR : std_logic_vector(7 downto 0);
        signal w_RST_WEIGHT_ADDR : std_logic;
        signal w_INC_WEIGHT_ADDR : std_logic;
        signal r_BIAS_ADDR : std_logic_vector(5 downto 0);
        signal w_RST_BIAS_ADDR : std_logic;
        signal w_INC_BIAS_ADDR : std_logic;
        signal w_LAST_WEIGHT : std_logic := '0';
        signal w_LAST_NEURON : std_logic := '0';
        signal r_REG_OUT_ADDR : std_logic_vector(5 downto 0) := (others => '0');
        signal w_INC_BUFF_OUT : std_logic := '0';
        signal w_RST_BUFF_OUT : std_logic := '0';


        begin 
        u_BIAS_ADDR : entity work.Counter_6dw_1bs
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_BIAS_ADDR,
            i_INC  => w_INC_BIAS_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => r_BIAS_ADDR
        );
 
        u_WEIGHT_ADDR : entity work.Counter_8dw_1bs
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_WEIGHT_ADDR,
            i_INC  => w_INC_WEIGHT_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => r_WEIGHT_ADDR
        );
 
        u_INPUT_ADDR : entity work.Counter_8dw_1bs
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_IN_ADDR,
            i_INC  => w_INC_IN_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => w_IN_READ_ADDR
        );
 
        u_REG_OUT_ADDR : entity work.Counter_6dw_1bs
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_BUFF_OUT,
            i_INC  => w_INC_BUFF_OUT,
            i_RESET_VAL  => (others => '0'),
            o_Q  => r_REG_OUT_ADDR
        );

  p_STATE : process (i_CLK, i_CLR)
  begin
    if (i_CLR = '1') then
      r_STATE <= s_IDLE; --initial state
    elsif (rising_edge(i_CLK)) then
      r_STATE <= w_NEXT; --next state
    end if;
  end process;
  p_NEXT : process (r_STATE, i_GO, r_BIAS_ADDR, w_LAST_NEURON, w_LAST_WEIGHT)
  begin
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
	      if (w_LAST_NEURON = '1') then
          w_NEXT <= s_END;
        else
          w_NEXT <= s_BIAS_INC_ADDR;
        end if;

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
  
  -- ENABLERS
  o_REG_BIAS_ENA <= '1' when (r_STATE = s_LOAD_BIAS) else '0';
  o_ACT_FUNCT_ENA <= '1' when (r_STATE = s_ENABLE_FUNCTION) else '0';  
  o_REG_PIX_ENA <= '1' when (r_STATE = s_LOAD_INPUT) else '0';
  o_REG_WEIGHT_ENA <= '1' when (r_STATE = s_LOAD_WEIGHT) else '0';
  o_ACC_ENA <= '1' when (r_STATE = s_ENABLE_NEURON_ACC) else '0';
  o_REG_OUT_ENA <= '1' when (r_STATE = s_ENABLE_REG_OUT) else '0';
  
  -- LAST CONTROLLERS
  w_LAST_NEURON <= '1' when (r_BIAS_ADDR = "100010") else '0';
  w_LAST_WEIGHT <= '1' when (r_WEIGHT_ADDR = "10000000") else '0';
  
  -- END
  o_READY <= '1' when (r_STATE = s_END) else '0';
  
  
    end arc;