library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity One_Hot_Encoder_6x1 is
        
        port (i_DATA : in std_logic_vector(5 downto 0);
              o_DATA : out std_logic
        );
    end One_Hot_Encoder_6x1;
                 
    architecture arc of One_Hot_Encoder_6x1 is


        begin
            process (i_DATA)
            begin
                for i in 0 to 0 loop
                    if (i = to_integer(unsigned(i_DATA))) then 
                        o_DATA <= '1';
                    else
                        o_DATA <= '0'; 
                    end if;
                end loop;
            end process;
        
    end arc;