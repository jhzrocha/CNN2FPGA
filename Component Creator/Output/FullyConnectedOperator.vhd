library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity FullyConnectedOperator is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_PIX : in std_logic_vector(7 downto 0):= (others => '0');
              i_WEIGHT : in i_WEIGHT_FullyConnectedOperator:= (others => (others => '0'));
              i_REG_PIX_ENA : in std_logic;
              i_REG_WEIGHT_ENA : in std_logic;
              i_BIAS_SCALE : in std_logic_vector(31 downto 0);
              i_REG_BIAS_ADDR : in std_logic_vector(3 downto 0);
              i_REG_BIAS_ENA : in std_logic;
              i_ACC_ENA : in std_logic;
              i_ACC_CLR : in std_logic;
              i_REG_OUT_CLR : in std_logic:= '0';
              i_REG_OUT_ENA : in std_logic;
              i_REG_OUT_ADDR : in std_logic_vector(5 downto 0):= (others => '0');
              o_PIX : out o_PIX_FullyConnectedOperator:= (others => (others => '0'))
        );
    end FullyConnectedOperator;
                 
    architecture arc of FullyConnectedOperator is
        signal w_NFC_OUT : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_ADD_BIAS_OUT : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_A : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_B : std_logic_vector(31 downto 0) := (others => '0');
        signal w_SCALE_OUT : w_SCALE_OUT_FullyConnectedOperator := (others => (others => '0'));
        signal w_CAST_OUT : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_SHIFT_OUT : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_OFFSET_OUT : commonUnitsTypeOn_FullyConnectedOperator := (others => (others => '0'));
        signal w_CLIP_OUT_BIAS : w_CLIP_OUT_BIAS_FullyConnectedOperator := (others => (others => '0'));
        signal w_CLIP_OUT_FUNCTION : w_CLIP_OUT_FUNCTION_FullyConnectedOperator := (others => (others => '0'));
        signal r_REG_OUT : o_PIX_FullyConnectedOperator := (others => (others => '0'));
        signal w_BIAS_ADDR : std_logic_vector(1 downto 0) := (others => '0');
        signal w_SCALE : std_logic_vector(31 downto 0) := (others => '0');
        signal w_REG_OUT_ADDR : std_logic_vector(33 downto 0) := (others => '0');
        signal w_REG_BIAS_OUT_0 : std_logic_vector(31 downto 0) := (others => '0');
        signal w_REG_BIAS_ENA_w_BIAS_ADDR_0 : std_logic;
        signal w_REG_BIAS_OUT_1 : std_logic_vector(31 downto 0) := (others => '0');
        signal w_REG_BIAS_ENA_w_BIAS_ADDR_1 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_0 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_1 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_2 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_3 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_4 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_5 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_6 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_7 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_8 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_9 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_10 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_11 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_12 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_13 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_14 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_15 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_16 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_17 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_18 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_19 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_20 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_21 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_22 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_23 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_24 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_25 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_26 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_27 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_28 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_29 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_30 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_31 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_32 : std_logic;
        signal w_REG_OUT_ENA_W_REG_OUT_ADDR_33 : std_logic;

constant SCALE_FACTOR : std_logic_vector(31 downto 0) := "01000000000000000000000000000000";

        begin 
        u_UNIT_0 : entity work.neuron_8_32
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ACC_ENA  => i_ACC_ENA,
            i_REG_PIX_ENA  => i_REG_PIX_ENA,
            i_REG_WEIGHT_ENA  => i_REG_WEIGHT_ENA,
            i_ACC_CLR  => i_ACC_CLR,
            i_PIX  => i_PIX,
            i_WEIGHT  => i_WEIGHT(0),
            o_PIX  => w_NFC_OUT(0)
        );
 
        u_REG_BIAS_0 : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_REG_BIAS_ENA_w_BIAS_ADDR_0,
            i_A  => i_BIAS_SCALE,
            o_Q  => w_REG_BIAS_OUT_0
        );
 
        u_RELU : entity work.Relu_8dw
        port map (
            i_PIX  => w_CLIP_OUT_BIAS(0),
            o_PIX  => w_CLIP_OUT_FUNCTION(0)
        );
 
        u_UNIT_1 : entity work.neuron_8_32
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ACC_ENA  => i_ACC_ENA,
            i_REG_PIX_ENA  => i_REG_PIX_ENA,
            i_REG_WEIGHT_ENA  => i_REG_WEIGHT_ENA,
            i_ACC_CLR  => i_ACC_CLR,
            i_PIX  => i_PIX,
            i_WEIGHT  => i_WEIGHT(1),
            o_PIX  => w_NFC_OUT(1)
        );
 
        u_REG_BIAS_1 : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_REG_BIAS_ENA_w_BIAS_ADDR_1,
            i_A  => i_BIAS_SCALE,
            o_Q  => w_REG_BIAS_OUT_1
        );
 
        u_REG_OUT_0 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_0,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(0)
        );
 
        u_REG_OUT_1 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_1,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(1)
        );
 
        u_REG_OUT_2 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_2,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(2)
        );
 
        u_REG_OUT_3 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_3,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(3)
        );
 
        u_REG_OUT_4 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_4,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(4)
        );
 
        u_REG_OUT_5 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_5,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(5)
        );
 
        u_REG_OUT_6 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_6,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(6)
        );
 
        u_REG_OUT_7 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_7,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(7)
        );
 
        u_REG_OUT_8 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_8,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(8)
        );
 
        u_REG_OUT_9 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_9,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(9)
        );
 
        u_REG_OUT_10 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_10,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(10)
        );
 
        u_REG_OUT_11 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_11,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(11)
        );
 
        u_REG_OUT_12 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_12,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(12)
        );
 
        u_REG_OUT_13 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_13,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(13)
        );
 
        u_REG_OUT_14 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_14,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(14)
        );
 
        u_REG_OUT_15 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_15,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(15)
        );
 
        u_REG_OUT_16 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_16,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(16)
        );
 
        u_REG_OUT_17 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_17,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(17)
        );
 
        u_REG_OUT_18 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_18,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(18)
        );
 
        u_REG_OUT_19 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_19,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(19)
        );
 
        u_REG_OUT_20 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_20,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(20)
        );
 
        u_REG_OUT_21 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_21,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(21)
        );
 
        u_REG_OUT_22 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_22,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(22)
        );
 
        u_REG_OUT_23 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_23,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(23)
        );
 
        u_REG_OUT_24 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_24,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(24)
        );
 
        u_REG_OUT_25 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_25,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(25)
        );
 
        u_REG_OUT_26 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_26,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(26)
        );
 
        u_REG_OUT_27 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_27,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(27)
        );
 
        u_REG_OUT_28 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_28,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(28)
        );
 
        u_REG_OUT_29 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_29,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(29)
        );
 
        u_REG_OUT_30 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_30,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(30)
        );
 
        u_REG_OUT_31 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_31,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(31)
        );
 
        u_REG_OUT_32 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_32,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(32)
        );
 
        u_REG_OUT_33 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_REG_OUT_CLR,
            i_ENA  => w_REG_OUT_ENA_W_REG_OUT_ADDR_33,
            i_A  => w_CLIP_OUT_FUNCTION(0),
            o_Q  => r_REG_OUT(33)
        );
 
        u_OHE_BIAS : entity work.One_Hot_Encoder_4x2
        port map (
            i_DATA  => i_REG_BIAS_ADDR,
            o_DATA  => w_BIAS_ADDR
        );
 
        u_OHE_OUT : entity work.One_Hot_Encoder_6x34
        port map (
            i_DATA  => i_REG_OUT_ADDR,
            o_DATA  => W_REG_OUT_ADDR
        );

     w_REG_BIAS_ENA_w_BIAS_ADDR_0   <= i_REG_BIAS_ENA and w_BIAS_ADDR(0);
     w_ADD_BIAS_OUT(0)   <= std_logic_vector(signed(w_NFC_OUT(0)) + signed(w_REG_BIAS_OUT_0));
     w_A(0)(31 downto 0) <= w_ADD_BIAS_OUT(0);
     w_SCALE_OUT(0) <= std_logic_vector(signed(w_A(0)) * signed(SCALE_FACTOR));
     w_CAST_OUT(0) <= w_SCALE_OUT(0)(62 downto 31);
     w_SHIFT_OUT(0)(24 downto 0)  <= w_CAST_OUT(0)(31 downto 7);
     w_SHIFT_OUT(0)(31 downto 24) <= (others => '1') when (w_CAST_OUT(0)(31) = '1') else (others => '0');
     w_OFFSET_OUT(0) <= std_logic_vector(unsigned(w_SHIFT_OUT(0)) + to_unsigned(82, 32));
     w_CLIP_OUT_BIAS(0) <= w_OFFSET_OUT(0)(7 downto 0);
     w_REG_BIAS_ENA_w_BIAS_ADDR_1   <= i_REG_BIAS_ENA and w_BIAS_ADDR(1);
     w_ADD_BIAS_OUT(1)   <= std_logic_vector(signed(w_NFC_OUT(1)) + signed(w_REG_BIAS_OUT_1));
     w_A(1)(31 downto 0) <= w_ADD_BIAS_OUT(1);
     w_SCALE_OUT(1) <= std_logic_vector(signed(w_A(1)) * signed(SCALE_FACTOR));
     w_CAST_OUT(1) <= w_SCALE_OUT(1)(62 downto 31);
     w_SHIFT_OUT(1)(24 downto 0)  <= w_CAST_OUT(1)(31 downto 7);
     w_SHIFT_OUT(1)(31 downto 24) <= (others => '1') when (w_CAST_OUT(1)(31) = '1') else (others => '0');
     w_OFFSET_OUT(1) <= std_logic_vector(unsigned(w_SHIFT_OUT(1)) + to_unsigned(82, 32));
     w_CLIP_OUT_BIAS(1) <= w_OFFSET_OUT(1)(7 downto 0);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_0   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(0);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_1   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(1);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_2   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(2);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_3   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(3);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_4   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(4);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_5   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(5);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_6   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(6);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_7   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(7);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_8   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(8);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_9   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(9);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_10   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(10);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_11   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(11);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_12   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(12);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_13   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(13);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_14   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(14);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_15   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(15);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_16   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(16);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_17   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(17);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_18   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(18);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_19   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(19);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_20   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(20);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_21   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(21);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_22   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(22);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_23   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(23);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_24   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(24);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_25   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(25);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_26   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(26);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_27   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(27);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_28   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(28);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_29   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(29);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_30   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(30);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_31   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(31);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_32   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(32);
     w_REG_OUT_ENA_W_REG_OUT_ADDR_33   <= i_REG_OUT_ENA and W_REG_OUT_ADDR(33);
       o_PIX <= r_REG_OUT;
    end arc;