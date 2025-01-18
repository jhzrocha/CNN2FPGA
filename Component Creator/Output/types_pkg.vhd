
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
type i_WEIGHT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(7 downto 0);
type o_PIX_FullyConnectedOperator is array (0 to 34) of std_logic_vector(7 downto 0);
type w_NFC_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_ADD_BIAS_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_A_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_SCALE_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(63 downto 0);
type w_CAST_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_SHIFT_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_OFFSET_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(31 downto 0);
type w_CLIP_OUT_FullyConnectedOperator is array (0 to 0) of std_logic_vector(7 downto 0);

    END PACKAGE types_pkg;