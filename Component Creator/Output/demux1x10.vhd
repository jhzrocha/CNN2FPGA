library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity demux1x10 is
        
        port (i_A  : in std_logic_vector(7 DOWNTO 0);
              i_SEL : in std_logic_vector (3 DOWNTO 0);
              o_PORT_0 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_1 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_2 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_3 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_4 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_5 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_6 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_7 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_8 : out std_logic_vector(7 DOWNTO 0);
              o_PORT_9 : out std_logic_vector(7 DOWNTO 0)
        );
    end demux1x10;
                 
    architecture arc of demux1x10 is


        begin
        o_PORT_0 <= i_A when (i_SEL ="0000") else (others =>  '0');
        o_PORT_1 <= i_A when (i_SEL ="0001") else (others =>  '0');
        o_PORT_2 <= i_A when (i_SEL ="0010") else (others =>  '0');
        o_PORT_3 <= i_A when (i_SEL ="0011") else (others =>  '0');
        o_PORT_4 <= i_A when (i_SEL ="0100") else (others =>  '0');
        o_PORT_5 <= i_A when (i_SEL ="0101") else (others =>  '0');
        o_PORT_6 <= i_A when (i_SEL ="0110") else (others =>  '0');
        o_PORT_7 <= i_A when (i_SEL ="0111") else (others =>  '0');
        o_PORT_8 <= i_A when (i_SEL ="1000") else (others =>  '0');
        o_PORT_9 <= i_A when (i_SEL ="1001") else (others =>  '0');

        
    end arc;