library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity ConvolutionalLayerIm4x4K2x2 is
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
    end ConvolutionalLayerIm4x4K2x2;
                 
    architecture arc of ConvolutionalLayerIm4x4K2x2 is
      signal w_DATA : signed(0 to p_QT_BITS*{qtKernelPixels[0]*qtKernelPixels[1]}-1) := i_DATA(0*p_QT_BITS to p_QT_BITS*1-1);
      signal w_MATRIX_MULT_O : integer := 0;

        begin    
        
         MatrixMultiplier : entity work.MatrixMultiplier_4px  
    generic map (
      p_QT_BITS => 8
    )
    port map (
        i_DATA  => w_DATA,
        i_KERNEL  => i_KERNEL,
        i_ENA  => i_ENA,
        o_VALUE  => w_MATRIX_MULT_O
    );

            multi:
            process(i_ENA,i_CLK,i_RST)            
            begin
                if (i_ENA= '1') then
                    w_O_VALUE <= TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL))); 
                end if;
            end process multi;

        
    end arc;