library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity Multiplexer_4_32b is
        
        port (i_A : in t_ARRAY_OF_LOGIC_VECTOR_mult4:= (others => (others => '0'));
              i_SEL : in std_logic_vector(1 DOWNTO 0):= (others => '0');
              o_Q : out std_logic_vector(31 DOWNTO 0)
        );
    end Multiplexer_4_32b;
                 
    architecture arc of Multiplexer_4_32b is
        signal w_INDEX : integer := 0;


        begin
            w_INDEX <= to_integer(unsigned(i_SEL));
            o_Q <= i_A(w_INDEX);
        
    end arc;