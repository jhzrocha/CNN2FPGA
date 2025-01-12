library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity demux1x3_8b is
        
        port (i_A : in std_logic_vector(7 DOWNTO 0);
              i_SEL : in std_logic_vector (1 DOWNTO 0);
              o_PORT_0 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_1 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_2 : out std_logic_vector(7 DOWNTO 0)
        );
    end demux1x3_8b;
                 
    architecture arc of demux1x3_8b is


        begin
        o_PORT_0 <= i_A when (i_SEL ="00") else (others =>  '0');
        o_PORT_1 <= i_A when (i_SEL ="01") else (others =>  '0');
        o_PORT_2 <= i_A when (i_SEL ="10") else (others =>  '0');

        
    end arc;