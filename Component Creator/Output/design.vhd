library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity design is
        
        port (
      i_DATA : in signed(0 to p_QT_BITS*9-1);
      i_KERNEL : in signed(0 to p_QT_BITS*9-1);
      i_ENA : in std_logic;
      o_VALUE : out integer
        );
    end design;
                 
    architecture arc of design is

        begin    
        
         MatrixMultiplier : entity work.MatrixMultiplier  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => ,
        i_KERNEL  => ,
        i_ENA  => ,
        o_VALUE  => 
    );

    end arc;