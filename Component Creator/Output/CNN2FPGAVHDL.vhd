library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_PIX_0 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_1 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_2 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_3 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_4 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PIX_5 : in STD_LOGIC_VECTOR (7 downto 0);
              o_PIX : out STD_LOGIC_VECTOR (7 downto 0)
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        averageTree_6 : entity work.averageTree_6
        port map (
            i_PIX_0  => i_PIX_0,
            i_PIX_1  => i_PIX_1,
            i_PIX_2  => i_PIX_2,
            i_PIX_3  => i_PIX_3,
            i_PIX_4  => i_PIX_4,
            i_PIX_5  => i_PIX_5,
            o_PIX  => o_PIX
        );

    end arc;