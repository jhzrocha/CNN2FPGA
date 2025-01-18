library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity registrador_8b is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_ENA : in std_logic;
              i_A : in std_logic_vector(7 DOWNTO 0);
              o_Q : out std_logic_vector(7 DOWNTO 0)
        );
    end registrador_8b;
                 
    architecture arc of registrador_8b is
        signal r_A : std_logic_vector(7 DOWNTO 0);


        begin
            process (i_CLK, i_CLR, i_ENA, i_A)
            begin 
                -- reset
                if (i_CLR = '1') then
                    r_A <= (others => '0');    
                -- subida clock
                elsif (rising_edge(i_CLK)) then 
                -- enable ativo
                    if (i_ENA = '1') then
                        r_A <= i_A;      
                    end if;
                end if;
            end process;  
            o_Q <= r_A;
        
    end arc;