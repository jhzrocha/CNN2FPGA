library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity MatrixMultiplier is
        generic (p_QT_BITS : natural := 8);
        port (
      i_DATA : in signed(0 to p_QT_BITS*9-1);
      i_KERNEL : in signed(0 to p_QT_BITS*9-1);
      i_ENA : in std_logic;
      o_VALUE : out integer
        );
    end MatrixMultiplier;
                 
    architecture arc of MatrixMultiplier is
      signal w_MULT_0 : integer := 0;
      signal w_MULT_1 : integer := 0;
      signal w_MULT_2 : integer := 0;
      signal w_MULT_3 : integer := 0;
      signal w_MULT_4 : integer := 0;
      signal w_MULT_5 : integer := 0;
      signal w_MULT_6 : integer := 0;
      signal w_MULT_7 : integer := 0;
      signal w_MULT_8 : integer := 0;

        begin    
        
         Multi_0 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(0*p_QT_BITS to p_QT_BITS*1-1),
        i_KERNEL  => i_KERNEL(0*p_QT_BITS to p_QT_BITS*1-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_0
    );
 Multi_1 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(1*p_QT_BITS to p_QT_BITS*2-1),
        i_KERNEL  => i_KERNEL(1*p_QT_BITS to p_QT_BITS*2-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_1
    );
 Multi_2 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(2*p_QT_BITS to p_QT_BITS*3-1),
        i_KERNEL  => i_KERNEL(2*p_QT_BITS to p_QT_BITS*3-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_2
    );
 Multi_3 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(3*p_QT_BITS to p_QT_BITS*4-1),
        i_KERNEL  => i_KERNEL(3*p_QT_BITS to p_QT_BITS*4-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_3
    );
 Multi_4 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(4*p_QT_BITS to p_QT_BITS*5-1),
        i_KERNEL  => i_KERNEL(4*p_QT_BITS to p_QT_BITS*5-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_4
    );
 Multi_5 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(5*p_QT_BITS to p_QT_BITS*6-1),
        i_KERNEL  => i_KERNEL(5*p_QT_BITS to p_QT_BITS*6-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_5
    );
 Multi_6 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(6*p_QT_BITS to p_QT_BITS*7-1),
        i_KERNEL  => i_KERNEL(6*p_QT_BITS to p_QT_BITS*7-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_6
    );
 Multi_7 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(7*p_QT_BITS to p_QT_BITS*8-1),
        i_KERNEL  => i_KERNEL(7*p_QT_BITS to p_QT_BITS*8-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_7
    );
 Multi_8 : entity work.multiplicator  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA(8*p_QT_BITS to p_QT_BITS*9-1),
        i_KERNEL  => i_KERNEL(8*p_QT_BITS to p_QT_BITS*9-1),
        i_ENA  => i_ENA,
        o_VALUE  => w_MULT_8
    );
 adder : entity work.Adder_9in  
    
    port map (
        i_PORT_0  => w_MULT_0,
        i_PORT_1  => w_MULT_1,
        i_PORT_2  => w_MULT_2,
        i_PORT_3  => w_MULT_3,
        i_PORT_4  => w_MULT_4,
        i_PORT_5  => w_MULT_5,
        i_PORT_6  => w_MULT_6,
        i_PORT_7  => w_MULT_7,
        i_PORT_8  => w_MULT_8,
        o_VALUE  => o_VALUE
    );

    end arc;