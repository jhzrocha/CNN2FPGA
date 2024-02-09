library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity multiplicator is
        generic (p_QT_BITS : natural := 8);
        port (
      i_DATA : in signed(0 to p_QT_BITS-1);
      i_KERNEL : in signed(0 to p_QT_BITS-1);
      i_ENA : in std_logic;
      o_VALUE : out integer
        );
    end multiplicator;
                 
    architecture arc of multiplicator is
      signal w_O_VALUE : integer := 0;

        begin    
        
        
            multi:
            process(i_DATA,i_KERNEL,i_ENA)
            
            begin
                if (i_ENA= '1') then
                    w_O_VALUE <= TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL))); 
                end if;
            end process multi;
            o_VALUE <= w_O_VALUE;
        
    end arc;