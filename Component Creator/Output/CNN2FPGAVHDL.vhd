library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_PIX_SHIFT_ENA : in std_logic;
              i_PIX_ROW_0 : in std_logic_vector (7 downto 0);
              i_PIX_ROW_1 : in std_logic_vector (7 downto 0);
              o_PIX : out std_logic_vector (7 downto 0)
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        MaxPooling_8dw : entity work.MaxPooling_8dw
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => i_PIX_ROW_0,
            i_PIX_ROW_1  => i_PIX_ROW_1,
            o_PIX  => o_PIX
        );

    end arc;