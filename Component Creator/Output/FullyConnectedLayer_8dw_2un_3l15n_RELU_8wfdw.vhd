library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX : in i_A_Multiplexer_64_8b:= (others => (others => '0'));
              o_PIX : out o_PIX_FullyConnectedOperator:= (others => (others => '0'));
              o_READ_ADDR : out std_logic_vector(6 downto 0);
              o_READY : out std_logic
        );
    end FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw;
                 
    architecture arc of FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw is
        signal w_REG_PIX_ENA : std_logic;
        signal w_REG_WEIGHT_ENA : std_logic;
        signal w_REG_BIAS_ENA : std_logic;
        signal w_ACC_ENA : std_logic;
        signal w_ACC_CLR : std_logic;
        signal w_REG_OUT_ENA : std_logic;
        signal w_REG_OUT_ADDR : std_logic_vector(5 downto 0) := (others => '0');
        signal w_WEIGHT_READ_ADDR : std_logic_vector(6 downto 0);
        signal w_BIAS_READ_ADDR : std_logic_vector(3 downto 0);
        signal w_WEIGHT : i_WEIGHT_FullyConnectedOperator := (others => (others => '0'));
        signal w_BIAS_SCALE : std_logic_vector(31 downto 0);
        signal w_PIX : std_logic_vector(7 downto 0);
        signal w_IN_READ_ADDR : std_logic_vector(6 downto 0);
        signal w_SEL_REG_INT : std_logic_vector(2 downto 0);
        signal w_SEL_INPUT_OR_IN_REG : std_logic;
        signal w_OPERATOR_OUTPUT : o_PIX_FullyConnectedOperator := (others => (others => '0'));
        signal w_INPUT_OR_REG : w_INPUT_OR_REG_FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw := (others => (others => '0'));
        signal w_FC_OPERATOR_OUTPUT : o_PIX_FullyConnectedOperator := (others => (others => '0'));
        signal w_ROM_OUT : std_logic_vector (7 downto 0) := (others => '0');
        signal w_ENA_REG_INT : std_logic_vector (5 downto 0);
        signal w_OUTPUT_REG_INT : i_A_Multiplexer_6_8b;
        signal w_WEIGHT_ROM_MEMORY_OUT : i_A_Multiplexer_3_8b := (others => (others => '0'));
        signal w_WEIGHT_LAYER_SEL : std_logic_vector(1 downto 0) := (others => '0');


        begin 
        u_INPUTS_MUX : entity work.Multiplexer_64_8b
        port map (
            i_A  => i_PIX,
            i_SEL  => w_IN_READ_ADDR,
            o_Q  => w_INPUT_OR_REG(0)
        );
 
        u_REG_IN_MUX : entity work.Multiplexer_6_8b
        port map (
            i_A  => w_OUTPUT_REG_INT,
            i_SEL  => w_SEL_REG_INT,
            o_Q  => w_INPUT_OR_REG(1)
        );
 
        u_ROM_BIAS : entity work.conv_bias
        generic map (
            init_file_name => "bias.mif",
            DATA_WIDTH => 32,
            DATA_DEPTH => 4
        )
        port map (
            address  => w_BIAS_READ_ADDR,
            clken  => '1',
            clock  => i_CLK,
            q  => w_BIAS_SCALE
        );
 
        u_CONTROLE : entity work.fullyConnectedControl_7_4
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
            DATA_DEPTH => 3
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
            DATA_DEPTH => 3
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

        o_READ_ADDR <= w_IN_READ_ADDR;
        w_WEIGHT(0)<= w_ROM_OUT;

        w_PIX <= w_INPUT_OR_REG(1) when (w_SEL_INPUT_OR_IN_REG = '1') else w_INPUT_OR_REG(0);
        w_OPERATOR_OUTPUT <= w_FC_OPERATOR_OUTPUT;

        o_PIX <= w_FC_OPERATOR_OUTPUT;
           
    end arc;