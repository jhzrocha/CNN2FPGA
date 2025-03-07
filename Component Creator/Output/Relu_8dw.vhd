library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity Relu_8dw is
        
        port (i_PIX : in STD_LOGIC_VECTOR (7 downto 0);
              o_PIX : out STD_LOGIC_VECTOR (7 downto 0)
        );
    end Relu_8dw;
                 
    architecture arc of Relu_8dw is


        begin
            o_PIX <= (others => '0') when (i_PIX(8 - 1) = '1') else i_PIX;
        
    end arc;