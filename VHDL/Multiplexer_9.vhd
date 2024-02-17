library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity Multiplexer_9 is
        generic (p_QT_BITS : natural := 8);
        port (
      i_OPTION : in unsigned(0 to 4-1);
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
    end Multiplexer_9;
                 
    architecture arc of Multiplexer_9 is
      signal w_VALUE_0 : integer := 0;
      signal w_VALUE_1 : integer := 0;
      signal w_VALUE_2 : integer := 0;
      signal w_VALUE_3 : integer := 0;
      signal w_VALUE_4 : integer := 0;
      signal w_VALUE_5 : integer := 0;
      signal w_VALUE_6 : integer := 0;
      signal w_VALUE_7 : integer := 0;
      signal w_VALUE_8 : integer := 0;

        begin    
        
        
             process (i_OPTION, i_ENA, i_VALUE)
             begin
                if (i_ENA = '1') then
                    case i_OPTION is
                  when "0001" =>
                    w_VALUE_1 <= i_VALUE;
                  when "0010" =>
                    w_VALUE_2 <= i_VALUE;
                  when "0011" =>
                    w_VALUE_3 <= i_VALUE;
                  when "0100" =>
                    w_VALUE_4 <= i_VALUE;
                  when "0101" =>
                    w_VALUE_5 <= i_VALUE;
                  when "0110" =>
                    w_VALUE_6 <= i_VALUE;
                  when "0111" =>
                    w_VALUE_7 <= i_VALUE;
                  when "1000" =>
                    w_VALUE_8 <= i_VALUE;
                  when others => 
                      null;
                end case;
                end if;
            end process;
            o_PORT_0 <= w_VALUE_0; 
            o_PORT_1 <= w_VALUE_1; 
            o_PORT_2 <= w_VALUE_2; 
            o_PORT_3 <= w_VALUE_3; 
            o_PORT_4 <= w_VALUE_4; 
            o_PORT_5 <= w_VALUE_5; 
            o_PORT_6 <= w_VALUE_6; 
            o_PORT_7 <= w_VALUE_7; 
            o_PORT_8 <= w_VALUE_8; 

        
    end arc;