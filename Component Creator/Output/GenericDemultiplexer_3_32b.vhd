library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity GenericDemultiplexer_3_32b is
        
        port (i_A : in std_logic_vector(31  downto 0);
              i_SEL : in std_logic_vector(2  downto 0);
              o_Q : out t_ARRAY_OF_LOGIC_VECTOR_GenericDemultiplexer_3_32b:= (others => (others => '0'))
        );
    end GenericDemultiplexer_3_32b;
                 
    architecture arc of GenericDemultiplexer_3_32b is
        signal w_INDEX : integer := 0;


        begin
            process (i_A, i_SEL)
            begin
                for i in 0 to ((2 ** 3) - 1) loop
                if (i = to_integer(unsigned(i_SEL))) then
                    o_Q(i) <= i_A; -- caso valor selecionado
                else
                    o_Q(i) <= (others => '0'); -- caso valor não selecionado
                end if;
                end loop;
            end process;
        
    end arc;