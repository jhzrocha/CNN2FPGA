library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

entity multiplicator is
    generic (p_QT_BITS : natural := 8);
    port (
      i_DATA    : in signed(0 to p_QT_BITS-1);
      i_KERNEL  : in signed(0 to p_QT_BITS-1);
      i_RST     : in std_logic;
      i_ENA     : in std_logic;
      i_VALUE   : in integer;
	  i_CLKn    : in std_logic;
      o_VALUE   : out integer
    );
end multiplicator;

architecture arc of multiplicator is
begin    
    multi:
    process(i_DATA,i_KERNEL)
    begin
		if (i_RST = '1') then
				o_VALUE <= i_VALUE + TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL)));
		elsif (i_ENA= '1') then
			o_VALUE <= i_VALUE + TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL))); 
		end if;
	end process multi;

end arc;
