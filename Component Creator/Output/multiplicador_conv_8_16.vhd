library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity multiplicador_conv_8_16 is
        
        port (i_DATA_1 : in STD_LOGIC_VECTOR (7 downto 0);
              i_DATA_2 : in STD_LOGIC_VECTOR (7 downto 0);
              o_DATA : out STD_LOGIC_VECTOR (15 downto 0)
        );
    end multiplicador_conv_8_16;
                 
    architecture arc of multiplicador_conv_8_16 is
        signal w_A : STD_LOGIC_VECTOR (8 downto 0) := (others => '0');
        signal w_B : STD_LOGIC_VECTOR (8 downto 0) := (others => '0');
        signal w_DATA : STD_LOGIC_VECTOR (17 downto 0);


        begin
            w_A(7 downto 0) <= i_DATA_1;

            w_B(7 downto 0) <= i_DATA_2;
            w_B(8) <= i_DATA_2(7); -- estende bit de sinal do peso

            -- multiplicacao
            w_DATA <= STD_LOGIC_VECTOR(signed(w_A) * signed(w_B));

            o_DATA <= w_DATA(15 downto 0);
        
    end arc;