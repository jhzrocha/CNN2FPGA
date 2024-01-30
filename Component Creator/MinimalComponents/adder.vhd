library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

entity adder is
    port (
      i_VALUE_1    : in integer;
      i_VALUE_2    : in integer;
      o_VALUE      : out integer
    );
end adder;

architecture arc of adder is
begin    
    add:
    process(i_VALUE_1,i_VALUE_2)
    begin
		o_VALUE <= i_VALUE_1 + i_VALUE_2; 
        
	end process add;

end arc;
