library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        generic (i_DATA_WIDTH : integer := 8;
                 w_CONV_OUT : integer := 16;
                 o_DATA_WIDTH : integer := 32;
                 i_WIDTH : integer := 8;
                 i_DATA_WIDTH : INTEGER := 8;
                 o_DATA_WIDTH : INTEGER := 16);
        port (i_CLK  : in STD_LOGIC;
              i_CLR : in STD_LOGIC;
              i_PIX_SHIFT_ENA : in STD_LOGIC;
              i_WEIGHT_SHIFT_ENA : in STD_LOGIC;
              i_WEIGHT : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              o_PIX : out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        nucleoConvolucional : entity work.nucleoConvolucional
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_CLK   => i_CLK ,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_WEIGHT_SHIFT_ENA  => i_WEIGHT_SHIFT_ENA,
            i_WEIGHT  => i_WEIGHT,
            i_PIX_ROW  => i_PIX_ROW,
            i_PIX_ROW  => i_PIX_ROW,
            i_PIX_ROW  => i_PIX_ROW,
            o_PIX  => o_PIX
        );

    end arc;