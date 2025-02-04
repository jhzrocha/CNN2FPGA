
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
type o_PIX_FullyConnectedOperator is array (0 to 34) of std_logic_vector(7 downto 0);
type o_PIX_FullyConnectedLayer is array (0 to 34) of std_logic_vector(7 downto 0);

    END PACKAGE types_pkg;