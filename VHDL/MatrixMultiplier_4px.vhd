library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity MatrixMultiplier_4px is
        generic (p_QT_BITS : natural := 8);
        port (
      i_DATA : in signed(0 to p_QT_BITS*4-1);
      i_KERNEL : in signed(0 to p_QT_BITS*4-1);
      i_ENA : in std_logic;
      o_VALUE : out integer
        );
    end MatrixMultiplier_4px;
                 
    architecture arc of MatrixMultiplier_4px is
      signal w_MULT_0 : integer := 0;
      signal w_MULT_1 : integer := 0;
      signal w_MULT_2 : integer := 0;
      signal w_MULT_3 : integer := 0;

        begin    
        
         Multi_0 : entity work.multiplicator  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => i_DATA(0*p_QT_BITS to p_QT_BITS*1-1),
        i_KERNEL  => i_KERNEL(0*p_QT_BITS to p_QT_BITS*1-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_0
    );
 Multi_1 : entity work.multiplicator  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => i_DATA(1*p_QT_BITS to p_QT_BITS*2-1),
        i_KERNEL  => i_KERNEL(1*p_QT_BITS to p_QT_BITS*2-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_1
    );
 Multi_2 : entity work.multiplicator  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => i_DATA(2*p_QT_BITS to p_QT_BITS*3-1),
        i_KERNEL  => i_KERNEL(2*p_QT_BITS to p_QT_BITS*3-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_2
    );
 Multi_3 : entity work.multiplicator  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => i_DATA(3*p_QT_BITS to p_QT_BITS*4-1),
        i_KERNEL  => i_KERNEL(3*p_QT_BITS to p_QT_BITS*4-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_3
    );
 adder : entity work.Adder_4in  
    
    port map (
        i_PORT_0  => w_MULT_0,
        i_PORT_1  => w_MULT_1,
        i_PORT_2  => w_MULT_2,
        i_PORT_3  => w_MULT_3,
        o_VALUE  => o_VALUE
    );

    end arc;