library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity One_Hot_Encoder_5x18 is
        
        port (i_DATA : in std_logic_vector(4 downto 0);
              o_DATA : out std_logic_vector(17 downto 0)
        );
    end One_Hot_Encoder_5x18;
                 
    architecture arc of One_Hot_Encoder_5x18 is


        begin
            process (i_DATA)
            begin
                for i in 0 to 17 loop
                    if (i = to_integer(unsigned(i_DATA))) then 
                        o_DATA(i) <= '1';
                    else
                        o_DATA(i) <= '0'; 
                    end if;
                end loop;
            end process;
        
    end arc;