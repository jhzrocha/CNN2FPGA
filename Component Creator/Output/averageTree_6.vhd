library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity averageTree_6 is
        
        port (i_PIX_0 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_1 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_2 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_3 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_4 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_5 : in STD_LOGIC_VECTOR (7 downto 0);
              o_PIX : out STD_LOGIC_VECTOR (7 downto 0)
        );
    end averageTree_6;
                 
    architecture arc of averageTree_6 is
        signal w_SUM_RESULT : STD_LOGIC_VECTOR (15 downto 0);
        signal w_TEMP_AVG : unsigned (15 downto 0);


        begin 
        SumTree : entity work.arvore_soma_conv_6
        port map (
            i_PORT_0  => i_PIX_0,
            i_PORT_1  => i_PIX_1,
            i_PORT_2  => i_PIX_2,
            i_PORT_3  => i_PIX_3,
            i_PORT_4  => i_PIX_4,
            i_PORT_5  => i_PIX_5,
            o_DATA  => w_SUM_RESULT
        );
 
w_TEMP_AVG <= unsigned(w_SUM_RESULT) / 6;
o_PIX <= std_logic_vector(w_TEMP_AVG(7 downto 0));
    end arc;