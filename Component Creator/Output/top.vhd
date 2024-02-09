library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity top is
        generic (p_QT_BITS : natural := 8);
        port (
      i_DATA : in signed(0 to p_QT_BITS*16-1);
      i_KERNEL : in signed(0 to p_QT_BITS*4-1);
      i_ENA : in std_logic;
      i_RST : in std_logic;
      i_CLK : in std_logic;
      O_Value0_0 : out integer;
      O_Value0_1 : out integer;
      O_Value0_2 : out integer;
      O_Value1_0 : out integer;
      O_Value1_1 : out integer;
      O_Value1_2 : out integer;
      O_Value2_0 : out integer;
      O_Value2_1 : out integer;
      O_Value2_2 : out integer
        );
    end top;
                 
    architecture arc of top is

        begin    
        
         ConvolutionalLayerIm4x4K2x2 : entity work.ConvolutionalLayerIm4x4K2x2  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => i_DATA,
        i_KERNEL  => i_KERNEL,
        i_ENA  => i_ENA,
        i_RST  => i_RST,
        i_CLK  => i_CLK,
        O_Value0_0  => O_Value0_0,
        O_Value0_1  => O_Value0_1,
        O_Value0_2  => O_Value0_2,
        O_Value1_0  => O_Value1_0,
        O_Value1_1  => O_Value1_1,
        O_Value1_2  => O_Value1_2,
        O_Value2_0  => O_Value2_0,
        O_Value2_1  => O_Value2_1,
        O_Value2_2  => O_Value2_2
    );

    end arc;