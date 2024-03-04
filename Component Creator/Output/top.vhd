library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity top is
        
        port (a : in std_logic_vector(31 DOWNTO 0);
              b : in std_logic_vector(31 DOWNTO 0);
              cin : in std_logic;
              sum1 : out std_logic_vector(31 DOWNTO 0);
              cout : out std_logic;
              overflow : out std_logic;
              underflow : out std_logic
        );
    end top;
                 
    architecture arc of top is


        begin 
        add32 : entity work.add32
        port map (
            a  => a,
            b  => b,
            cin  => cin,
            sum1  => sum1,
            cout  => cout,
            overflow  => overflow,
            underflow  => underflow
        );

    end arc;