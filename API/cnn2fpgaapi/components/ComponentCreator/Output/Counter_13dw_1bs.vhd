library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity Counter_13dw_1bs is
        
        port (i_CLK : in std_logic;
              i_RESET : in std_logic;
              i_INC : in std_logic;
              i_RESET_VAL : in std_logic_vector(12 downto 0):= (others => '0');
              o_Q : out std_logic_vector(12 downto 0)
        );
    end Counter_13dw_1bs;
                 
    architecture arc of Counter_13dw_1bs is
        signal r_CNT : std_logic_vector (12 downto 0) := (others => '0');

constant c_STEP : std_logic_vector (12 downto 0) := std_logic_vector(to_unsigned(1, 13));

        begin
            process (i_CLK, i_RESET, i_INC, i_RESET_VAL)
            begin    
                if (rising_edge(i_CLK)) then
                if (i_RESET = '1') then
                    r_CNT <= i_RESET_VAL;
                elsif (i_INC = '1') then      
                    r_CNT <= std_logic_vector(unsigned(r_CNT) + unsigned(c_STEP));

                end if;    
                end if;
            end process;   
            
            o_Q <= r_CNT;
        
    end arc;