library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity FullyConnectedLayer is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX : in i_A_Multiplexer_64_8b:= (others => (others => '0'));
              o_PIX : out o_PIX_FullyConnectedOperator:= (others => (others => '0'));
              o_READ_ADDR : out std_logic_vector(6 downto 0);
              o_READY : out std_logic
        );
    end FullyConnectedLayer;
                 
    architecture arc of FullyConnectedLayer is
        signal w_REG_PIX_ENA : std_logic;
        signal w_REG_WEIGHT_ENA : std_logic;
        signal w_REG_BIAS_ENA : std_logic;
        signal w_ACC_ENA : std_logic;
        signal w_ACC_CLR : std_logic;
        signal w_REG_OUT_ENA : std_logic;
        signal w_REG_OUT_ADDR : std_logic_vector(5 downto 0) := (others => '0');
        signal w_WEIGHT_READ_ADDR : std_logic_vector(6 downto 0);
        signal w_BIAS_READ_ADDR : std_logic_vector(5 downto 0);
        signal w_WEIGHT : std_logic_vector(7 downto 0) := (others => '0');
        signal w_BIAS_SCALE : std_logic_vector(31 downto 0);
        signal w_PIX : std_logic_vector(7 downto 0);
        signal w_IN_READ_ADDR : std_logic_vector(6 downto 0);
        signal w_SEL_REG_INT : std_logic_vector(5 downto 0);
        signal w_SEL_INPUT_OR_IN_REG : std_logic;
        signal w_OPERATOR_OUTPUT : o_PIX_FullyConnectedOperator := (others => (others => '0'));
        signal w_INPUT_OR_REG : w_INPUT_OR_REG_FullyConnectedLayer := (others => (others => '0'));
        signal w_FC_OPERATOR_OUTPUT : o_PIX_FullyConnectedOperator := (others => (others => '0'));
        signal w_ROM_OUT : std_logic_vector (7 downto 0) := (others => '0');
        signal w_ENA_REG_INT : std_logic_vector (35 downto 0);
        signal w_OUTPUT_REG_INT : i_A_Multiplexer_36_8b;
        signal w_WEIGHT_ROM_MEMORY_OUT : i_A_Multiplexer_3_8b := (others => (others => '0'));
        signal w_WEIGHT_LAYER_SEL : std_logic_vector(1 downto 0) := (others => '0');


        begin 
        u_INPUTS_MUX : entity work.Multiplexer_64_8b
        port map (
            i_A  => i_PIX,
            i_SEL  => w_IN_READ_ADDR,
            o_Q  => w_INPUT_OR_REG(0)
        );
 
        u_REG_IN_MUX : entity work.Multiplexer_36_8b
        port map (
            i_A  => w_OUTPUT_REG_INT,
            i_SEL  => w_SEL_REG_INT,
            o_Q  => w_INPUT_OR_REG(1)
        );
 
        u_ROM_BIAS : entity work.conv_bias
        generic map (
            init_file_name => "conv2_bias.mif",
            DATA_WIDTH => 32,
            DATA_DEPTH => 6
        )
        port map (
            address  => w_BIAS_READ_ADDR,
            clken  => '1',
            clock  => i_CLK,
            q  => w_BIAS_SCALE
        );
 
        u_CONTROLE : entity work.fullyConnectedControl_7_6
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            o_READY  => o_READY,
            o_REG_PIX_ENA  => w_REG_PIX_ENA,
            o_REG_WEIGHT_ENA  => w_REG_WEIGHT_ENA,
            o_REG_BIAS_ENA  => w_REG_BIAS_ENA,
            o_ACC_ENA  => w_ACC_ENA,
            o_ACC_CLR  => w_ACC_CLR,
            o_REG_OUT_ENA  => w_REG_OUT_ENA,
            o_REG_OUT_ADDR  => w_REG_OUT_ADDR,
            o_WEIGHT_READ_ADDR  => w_WEIGHT_READ_ADDR,
            o_BIAS_READ_ADDR  => w_BIAS_READ_ADDR,
            o_IN_READ_ADDR  => w_IN_READ_ADDR
        );
 
        u_OPERACIONAL : entity work.FullyConnectedOperator
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX  => w_PIX,
            i_WEIGHT  => w_WEIGHT,
            i_REG_PIX_ENA  => w_REG_PIX_ENA,
            i_REG_WEIGHT_ENA  => w_REG_WEIGHT_ENA,
            i_BIAS_SCALE  => w_BIAS_SCALE,
            i_REG_BIAS_ADDR  => w_BIAS_READ_ADDR,
            i_REG_BIAS_ENA  => w_REG_BIAS_ENA,
            i_ACC_ENA  => w_ACC_ENA,
            i_ACC_CLR  => w_ACC_CLR,
            i_REG_OUT_CLR  => '0',
            i_REG_OUT_ENA  => w_REG_OUT_ENA,
            i_REG_OUT_ADDR  => w_REG_OUT_ADDR,
            o_PIX  => w_FC_OPERATOR_OUTPUT
        );
 
        u_ROM_WEIGHTS_0 : entity work.conv_weights
        generic map (
            init_file_name => "fc_weights_0.mif",
            DATA_WIDTH => 8,
            DATA_DEPTH => 7
        )
        port map (
            address  => w_WEIGHT_READ_ADDR,
            clock  => i_CLK,
            rden  => '1',
            q  => w_WEIGHT_ROM_MEMORY_OUT(0)
        );
 
        u_ROM_WEIGHTS_1 : entity work.conv_weights
        generic map (
            init_file_name => "fc_weights_1.mif",
            DATA_WIDTH => 8,
            DATA_DEPTH => 7
        )
        port map (
            address  => w_WEIGHT_READ_ADDR,
            clock  => i_CLK,
            rden  => '1',
            q  => w_WEIGHT_ROM_MEMORY_OUT(1)
        );
 
        u_ROM_WEIGHTS_2 : entity work.conv_weights
        generic map (
            init_file_name => "fc_weights_2.mif",
            DATA_WIDTH => 8,
            DATA_DEPTH => 7
        )
        port map (
            address  => w_WEIGHT_READ_ADDR,
            clock  => i_CLK,
            rden  => '1',
            q  => w_WEIGHT_ROM_MEMORY_OUT(2)
        );
 
        u_WEIGHTS_MUX : entity work.Multiplexer_3_8b
        port map (
            i_A  => w_WEIGHT_ROM_MEMORY_OUT,
            i_SEL  => w_WEIGHT_LAYER_SEL,
            o_Q  => w_ROM_OUT
        );
 
        u_REG_INT_0 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(0),
            i_A  => w_OPERATOR_OUTPUT(0),
            o_Q  => w_OUTPUT_REG_INT(0)
        );
 
        u_REG_INT_1 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(1),
            i_A  => w_OPERATOR_OUTPUT(1),
            o_Q  => w_OUTPUT_REG_INT(1)
        );
 
        u_REG_INT_2 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(2),
            i_A  => w_OPERATOR_OUTPUT(2),
            o_Q  => w_OUTPUT_REG_INT(2)
        );
 
        u_REG_INT_3 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(3),
            i_A  => w_OPERATOR_OUTPUT(3),
            o_Q  => w_OUTPUT_REG_INT(3)
        );
 
        u_REG_INT_4 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(4),
            i_A  => w_OPERATOR_OUTPUT(4),
            o_Q  => w_OUTPUT_REG_INT(4)
        );
 
        u_REG_INT_5 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(5),
            i_A  => w_OPERATOR_OUTPUT(5),
            o_Q  => w_OUTPUT_REG_INT(5)
        );
 
        u_REG_INT_6 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(6),
            i_A  => w_OPERATOR_OUTPUT(6),
            o_Q  => w_OUTPUT_REG_INT(6)
        );
 
        u_REG_INT_7 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(7),
            i_A  => w_OPERATOR_OUTPUT(7),
            o_Q  => w_OUTPUT_REG_INT(7)
        );
 
        u_REG_INT_8 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(8),
            i_A  => w_OPERATOR_OUTPUT(8),
            o_Q  => w_OUTPUT_REG_INT(8)
        );
 
        u_REG_INT_9 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(9),
            i_A  => w_OPERATOR_OUTPUT(9),
            o_Q  => w_OUTPUT_REG_INT(9)
        );
 
        u_REG_INT_10 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(10),
            i_A  => w_OPERATOR_OUTPUT(10),
            o_Q  => w_OUTPUT_REG_INT(10)
        );
 
        u_REG_INT_11 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(11),
            i_A  => w_OPERATOR_OUTPUT(11),
            o_Q  => w_OUTPUT_REG_INT(11)
        );
 
        u_REG_INT_12 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(12),
            i_A  => w_OPERATOR_OUTPUT(12),
            o_Q  => w_OUTPUT_REG_INT(12)
        );
 
        u_REG_INT_13 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(13),
            i_A  => w_OPERATOR_OUTPUT(13),
            o_Q  => w_OUTPUT_REG_INT(13)
        );
 
        u_REG_INT_14 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(14),
            i_A  => w_OPERATOR_OUTPUT(14),
            o_Q  => w_OUTPUT_REG_INT(14)
        );
 
        u_REG_INT_15 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(15),
            i_A  => w_OPERATOR_OUTPUT(15),
            o_Q  => w_OUTPUT_REG_INT(15)
        );
 
        u_REG_INT_16 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(16),
            i_A  => w_OPERATOR_OUTPUT(16),
            o_Q  => w_OUTPUT_REG_INT(16)
        );
 
        u_REG_INT_17 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(17),
            i_A  => w_OPERATOR_OUTPUT(17),
            o_Q  => w_OUTPUT_REG_INT(17)
        );
 
        u_REG_INT_18 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(18),
            i_A  => w_OPERATOR_OUTPUT(18),
            o_Q  => w_OUTPUT_REG_INT(18)
        );
 
        u_REG_INT_19 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(19),
            i_A  => w_OPERATOR_OUTPUT(19),
            o_Q  => w_OUTPUT_REG_INT(19)
        );
 
        u_REG_INT_20 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(20),
            i_A  => w_OPERATOR_OUTPUT(20),
            o_Q  => w_OUTPUT_REG_INT(20)
        );
 
        u_REG_INT_21 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(21),
            i_A  => w_OPERATOR_OUTPUT(21),
            o_Q  => w_OUTPUT_REG_INT(21)
        );
 
        u_REG_INT_22 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(22),
            i_A  => w_OPERATOR_OUTPUT(22),
            o_Q  => w_OUTPUT_REG_INT(22)
        );
 
        u_REG_INT_23 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(23),
            i_A  => w_OPERATOR_OUTPUT(23),
            o_Q  => w_OUTPUT_REG_INT(23)
        );
 
        u_REG_INT_24 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(24),
            i_A  => w_OPERATOR_OUTPUT(24),
            o_Q  => w_OUTPUT_REG_INT(24)
        );
 
        u_REG_INT_25 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(25),
            i_A  => w_OPERATOR_OUTPUT(25),
            o_Q  => w_OUTPUT_REG_INT(25)
        );
 
        u_REG_INT_26 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(26),
            i_A  => w_OPERATOR_OUTPUT(26),
            o_Q  => w_OUTPUT_REG_INT(26)
        );
 
        u_REG_INT_27 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(27),
            i_A  => w_OPERATOR_OUTPUT(27),
            o_Q  => w_OUTPUT_REG_INT(27)
        );
 
        u_REG_INT_28 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(28),
            i_A  => w_OPERATOR_OUTPUT(28),
            o_Q  => w_OUTPUT_REG_INT(28)
        );
 
        u_REG_INT_29 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(29),
            i_A  => w_OPERATOR_OUTPUT(29),
            o_Q  => w_OUTPUT_REG_INT(29)
        );
 
        u_REG_INT_30 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(30),
            i_A  => w_OPERATOR_OUTPUT(30),
            o_Q  => w_OUTPUT_REG_INT(30)
        );
 
        u_REG_INT_31 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(31),
            i_A  => w_OPERATOR_OUTPUT(31),
            o_Q  => w_OUTPUT_REG_INT(31)
        );
 
        u_REG_INT_32 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(32),
            i_A  => w_OPERATOR_OUTPUT(32),
            o_Q  => w_OUTPUT_REG_INT(32)
        );
 
        u_REG_INT_33 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(33),
            i_A  => w_OPERATOR_OUTPUT(33),
            o_Q  => w_OUTPUT_REG_INT(33)
        );
 
        u_REG_INT_34 : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_ENA_REG_INT(34),
            i_A  => w_OPERATOR_OUTPUT(34),
            o_Q  => w_OUTPUT_REG_INT(34)
        );

        o_READ_ADDR <= w_IN_READ_ADDR;
        w_WEIGHT<= w_ROM_OUT;

        w_PIX <= w_INPUT_OR_REG(1) when (w_SEL_INPUT_OR_IN_REG = '1') else w_INPUT_OR_REG(0);
        w_OPERATOR_OUTPUT <= w_FC_OPERATOR_OUTPUT;

        o_PIX <= w_FC_OPERATOR_OUTPUT;
           
    end arc;