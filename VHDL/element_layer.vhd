library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

entity convolutional_layer is
    generic (p_QT_BITS : natural := 8;
	          p_QT_PIXELS_X_IMAGEM : natural := 28;
				 p_QT_PIXELS_Y_IMAGEM : natural := 28;
				 p_QT_PIXELS_X_KERNEL : natural := 3;
				 p_QT_PIXELS_y_KERNEL : natural := 3);
    port (
      i_DATA    : in signed(0 to (p_QT_PIXELS_X_IMAGEM*p_QT_PIXELS_Y_IMAGEM*p_QT_BITS)-1);
      i_KERNEL  : in signed(0 to (p_QT_PIXELS_x_KERNEL*p_QT_PIXELS_y_KERNEL*p_QT_BITS)-1);
      i_RST     : in std_logic;
      i_ENA     : in std_logic;
	   i_CLKn    : in std_logic;
      o_VALUE   : out integer -- Alterar conforme a geração
		-- A quantidade de saídas é igual a ((X_IMAGEM - X_KERNEL) + 1) * (Y_IMAGEM - Y_KERNEL) + 1))
    );
end convolutional_layer;

architecture arch of convolutional_layer is

	signal w_internal_ena : std_logic := i_ENA;
	
	signal w_internal_index : natural := 0;
	
	signal w_internal_data : signed(0 to p_QT_BITS-1) := i_DATA(0 to w_internal_index+p_QT_BITS-1);
	signal w_kernel_data : signed(0 to p_QT_BITS-1) := i_KERNEL(0 to w_internal_index+p_QT_BITS-1);
		
	signal w_internal_value: integer := 0;
	
	signal w_result: integer := 0;

begin
    
	 u_CONV : entity work.convolutional_unit  
        generic map (p_QT_BITS)
        port map (
            i_DATA   => w_internal_data,
            i_KERNEL => w_kernel_data,
            i_RST    => i_RST,
            i_ENA    => w_internal_ena,
            i_VALUE  => w_internal_value,
            i_CLKn => i_CLKn,
            o_VALUE  => w_result
        );

	multi: process(i_CLKn)
    begin
        if (rising_edge(i_RST)) then
				w_internal_index <= 0;
            w_internal_data <= i_DATA(0 to p_QT_BITS-1);
				w_kernel_data <= i_KERNEL(0 to p_QT_BITS-1);
            w_internal_value <= 0;
		  else
			  if (i_ENA='1') then
					if (w_internal_index <= p_QT_BITS*p_QT_PIXELS-1) then
						 if (rising_edge(i_CLKn)) then
							  w_internal_ena <= '0';
							  w_internal_value <= w_result;
							  w_internal_index <= w_internal_index + p_QT_BITS;
						 elsif (falling_edge(i_CLKn)) then
							  w_internal_data <= i_DATA(w_internal_index to w_internal_index + p_QT_BITS - 1);
							  w_kernel_data <= i_KERNEL(w_internal_index to w_internal_index + p_QT_BITS - 1);
							  w_internal_ena <= '1';
						 end if;
					end if;
			  end if;
			end if;
    end process multi;

    o_VALUE <= 0 when w_internal_index <= p_QT_BITS*p_QT_PIXELS-1 else w_result; 

end arch;
