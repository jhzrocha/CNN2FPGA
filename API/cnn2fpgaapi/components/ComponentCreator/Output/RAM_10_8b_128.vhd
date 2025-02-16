library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity RAM_10_8b_128 is
        
        port (i_CLK : in std_logic;
              i_ADDR : in std_logic_vector(9 downto 0);
              i_DATA : in std_logic_vector(7 downto 0);
              i_WRITE : in std_logic;
              o_DATA : out std_logic_vector(7 downto 0)
        );
    end RAM_10_8b_128;
                 
    architecture arc of RAM_10_8b_128 is
        type RAM_ARRAY is array(127 downto 0) of std_logic_vector (7 downto 0);
        signal RAM : RAM_ARRAY := (others => (others => '0'));


        begin 
        process(i_CLK)
        begin
            if(rising_edge(i_CLK)) then
                if(i_WRITE='1') then
                    RAM(to_integer(unsigned(i_ADDR))) <= i_DATA;
                end if;
            end if;
        end process;

        o_DATA <= RAM(to_integer(unsigned(i_ADDR)));
        
        
    end arc;