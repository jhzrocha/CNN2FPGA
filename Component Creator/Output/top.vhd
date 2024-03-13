library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity top is
        generic (i_DATA_WIDTH : INTEGER := 16;
                 o_DATA_WIDTH : INTEGER := 32);
        port (i_PORT_0 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_1 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_2 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_3 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_4 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_5 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_6 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_7 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PORT_8 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              o_DATA : out out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)
        );
    end top;
                 
    architecture arc of top is
        type t_MAT is array(8 downto 0) of STD_LOGIC_VECTOR(o_DATA_WIDTH - 1 downto 0);


        begin 
        arvore_soma_conv_9 : entity work.arvore_soma_conv_9
        generic map (
            i_DATA_WIDTH => 16,
o_DATA_WIDTH => 32
        )
        port map (
            i_PORT_0  => i_PORT_0,
            i_PORT_1  => i_PORT_1,
            i_PORT_2  => i_PORT_2,
            i_PORT_3  => i_PORT_3,
            i_PORT_4  => i_PORT_4,
            i_PORT_5  => i_PORT_5,
            i_PORT_6  => i_PORT_6,
            i_PORT_7  => i_PORT_7,
            i_PORT_8  => i_PORT_8,
            o_DATA  => o_DATA
        );

    end arc;