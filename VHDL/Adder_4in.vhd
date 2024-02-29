library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity Adder_4in is
        
        port (
      i_PORT_0 : in integer;
      i_PORT_1 : in integer;
      i_PORT_2 : in integer;
      i_PORT_3 : in integer;
      o_VALUE : out integer
        );
    end Adder_4in;
                 
    architecture arc of Adder_4in is

        begin    
        
        
    add:
      process(i_PORT_0 ,i_PORT_1 ,i_PORT_2 ,i_PORT_3 )
      begin
      o_VALUE <= i_PORT_0 +i_PORT_1 +i_PORT_2 +i_PORT_3 ;           
    end process add;
    
    end arc;