library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity ConvolutionalLayerIm4x4K2x2 is
        generic (p_QT_BITS : natural := 1);
        port (
      i_DATA : in signed(0 to p_QT_BITS*16-1);
      i_KERNEL : in signed(0 to p_QT_BITS*4-1);
      i_ENA : in std_logic;
      i_RST : in std_logic;
      i_CLK : in std_logic;
      O_VALUE_0_0 : out integer;
      O_VALUE_0_1 : out integer;
      O_VALUE_0_2 : out integer;
      O_VALUE_1_0 : out integer;
      O_VALUE_1_1 : out integer;
      O_VALUE_1_2 : out integer;
      O_VALUE_2_0 : out integer;
      O_VALUE_2_1 : out integer;
      O_VALUE_2_2 : out integer
        );
    end ConvolutionalLayerIm4x4K2x2;
                 
    architecture arc of ConvolutionalLayerIm4x4K2x2 is
      signal w_OPTION : unsigned(0 to 4-1) := "0000";
      signal w_DATA : signed(0 to p_QT_BITS*4-1);
      signal w_MATRIX_MULT_O : integer := 0;

        begin    
        
         switcher : entity work.Switcher_9  
    
    port map (
        i_OPTION  => w_OPTION,
        i_ENA  => i_ENA,
        i_VALUE  => w_MATRIX_MULT_O,
        o_PORT_0  => O_VALUE_0_0,
        o_PORT_1  => O_VALUE_0_1,
        o_PORT_2  => O_VALUE_0_2,
        o_PORT_3  => O_VALUE_1_0,
        o_PORT_4  => O_VALUE_1_1,
        o_PORT_5  => O_VALUE_1_2,
        o_PORT_6  => O_VALUE_2_0,
        o_PORT_7  => O_VALUE_2_1,
        o_PORT_8  => O_VALUE_2_2
    );
 MatrixMultiplier : entity work.MatrixMultiplier_4px  
    generic map (
      p_QT_BITS => p_QT_BITS
    )
    port map (
        i_DATA  => w_DATA,
        i_KERNEL  => i_KERNEL,
        i_ENA  => i_ENA,
        o_VALUE  => w_MATRIX_MULT_O
    );

            proc:
            process(i_ENA, i_CLK)
                variable cont : integer := 0;
            begin
                if (i_ENA = '1') then
                    if(cont < 8) then
						w_OPTION <= to_unsigned(cont, 4);
                        w_DATA <= i_DATA(cont*p_QT_BITS to (p_QT_BITS*(cont+1))-1);
					    cont := cont + 1;
					end if;
                end if;
            end process proc;
        
    end arc;