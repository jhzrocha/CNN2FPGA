library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity add1 is
        
        port (a : in std_logic;
              b : in std_logic;
              cin : in std_logic;
              sum : out std_logic;
              cout : out std_logic
        );
    end add1;
                 
    architecture arc of add1 is
        signal w_A_XOR_B  : std_logic;


        begin
            w_A_XOR_B <= (a xor b);
                
            -- resultado
            sum <= w_A_XOR_B xor cin;   
            -- carry out
            cout <= (a and b) or (w_A_XOR_B and cin);
        
    end arc;