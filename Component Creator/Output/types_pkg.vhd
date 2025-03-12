
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
type commonUnitsTypeOn_FullyConnectedOperator is array (0 to 1) of std_logic_vector(31 downto 0);
type o_PIX_FullyConnectedOperator is array (0 to 34) of std_logic_vector(7 downto 0);
type i_WEIGHT_FullyConnectedOperator is array (0 to 1) of std_logic_vector(7 downto 0);
type w_SCALE_OUT_FullyConnectedOperator is array (0 to 1) of std_logic_vector(63 downto 0);
type w_CLIP_OUT_BIAS_FullyConnectedOperator is array (0 to 1) of std_logic_vector(7 downto 0);
type w_CLIP_OUT_FUNCTION_FullyConnectedOperator is array (0 to 1) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_64_8b is array (0 to 63) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_6_8b is array (0 to 5) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_3_8b is array (0 to 2) of std_logic_vector(7 downto 0);
type w_INPUT_OR_REG_FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw is array (0 to 1) of std_logic_vector (7 downto 0);

    END PACKAGE types_pkg;