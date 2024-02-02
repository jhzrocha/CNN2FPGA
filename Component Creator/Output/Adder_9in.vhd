library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity Adder_9in is
        
        port (
      i_PORT_0 : in integer;
      i_PORT_1 : in integer;
      i_PORT_2 : in integer;
      i_PORT_3 : in integer;
      i_PORT_4 : in integer;
      i_PORT_5 : in integer;
      i_PORT_6 : in integer;
      i_PORT_7 : in integer;
      i_PORT_8 : in integer;
      o_VALUE : out integer
        );
    end Adder_9in;
                 
    architecture arc of Adder_9in is
        begin    
        
    add:
      process(i_PORT_0 ,i_PORT_1 ,i_PORT_2 ,i_PORT_3 ,i_PORT_4 ,i_PORT_5 ,i_PORT_6 ,i_PORT_7 ,i_PORT_8 )
      begin
      o_VALUE <= i_PORT_0 +i_PORT_1 +i_PORT_2 +i_PORT_3 +i_PORT_4 +i_PORT_5 +i_PORT_6 +i_PORT_7 +i_PORT_8 ;           
    end process add;
    
    end arc;