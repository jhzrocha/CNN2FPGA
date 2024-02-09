library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        generic (p_QT_BITS : natural := 8);
        port (
      i_DATA : in signed(0 to p_QT_BITS*9-1);
      i_KERNEL : in signed(0 to p_QT_BITS*9-1);
      i_ENA : in std_logic;
      o_VALUE : out integer
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is

        begin    
        
         MatrixMultiplier : entity work.MatrixMultiplier  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => i_DATA,
        i_KERNEL  => i_KERNEL,
        i_ENA  => i_ENA,
        o_VALUE  => o_VALUE
    );

    end arc;