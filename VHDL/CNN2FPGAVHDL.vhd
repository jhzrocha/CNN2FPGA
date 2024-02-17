library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        generic (p_QT_BITS : natural := 8);
        port (
      i_OPTION : in unsigned(3 downto 0);
      i_ENA : in std_logic;
      i_VALUE : in integer;
      o_PORT_0 : out integer;
      o_PORT_1 : out integer;
      o_PORT_2 : out integer;
      o_PORT_3 : out integer;
      o_PORT_4 : out integer;
      o_PORT_5 : out integer;
      o_PORT_6 : out integer;
      o_PORT_7 : out integer;
      o_PORT_8 : out integer
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is

        begin    
        
         Multiplexer_9 : entity work.Multiplexer_9  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_OPTION  => i_OPTION,
        i_ENA  => i_ENA,
        i_VALUE  => i_VALUE,
        o_PORT_0  => o_PORT_0,
        o_PORT_1  => o_PORT_1,
        o_PORT_2  => o_PORT_2,
        o_PORT_3  => o_PORT_3,
        o_PORT_4  => o_PORT_4,
        o_PORT_5  => o_PORT_5,
        o_PORT_6  => o_PORT_6,
        o_PORT_7  => o_PORT_7,
        o_PORT_8  => o_PORT_8
    );

    end arc;