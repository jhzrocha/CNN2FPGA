
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
type o_PIX_FullyConnectedOperator is array (0 to 34) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_64_8b is array (0 to 63) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_36_8b is array (0 to 35) of std_logic_vector(7 downto 0);
type i_A_Multiplexer_2_8b is array (0 to 1) of std_logic_vector(7 downto 0);
type w_INPUT_OR_REG_FullyConnectedLayer is array (0 to 1) of std_logic_vector (7 downto 0);

    END PACKAGE types_pkg;