library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity multiplicador_conv is
        generic (i_DATA_WIDTH : INTEGER := 8;
                 o_DATA_WIDTH : INTEGER := 16);
        port (i_DATA_1  : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_DATA_2 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              o_DATA    : out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)
        );
    end multiplicador_conv;
                 
    architecture arc of multiplicador_conv is
        signal w_A : STD_LOGIC_VECTOR (i_DATA_WIDTH downto 0) := (others => '0');
        signal w_B : STD_LOGIC_VECTOR (i_DATA_WIDTH downto 0) := (others => '0');
        signal w_DATA : STD_LOGIC_VECTOR (17 downto 0);


        begin
            w_A(i_DATA_WIDTH - 1 downto 0) <= i_DATA_1;

            w_B(i_DATA_WIDTH - 1 downto 0) <= i_DATA_2;
            w_B(i_DATA_WIDTH) <= i_DATA_2(i_DATA_WIDTH - 1); -- estende bit de sinal do peso

            -- multiplicacao
            w_DATA <= STD_LOGIC_VECTOR(signed(w_A) * signed(w_B));

            o_DATA <= w_DATA(o_DATA_WIDTH - 1 downto 0);
        
    end arc;