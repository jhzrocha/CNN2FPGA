-- Code your design here
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

entity CNN2FPGAVHDL is
    generic (p_QT_BITS : natural := 8);
    port (
      i_DATA    : in signed(0 to p_QT_BITS-1);
      i_KERNEL  : in signed(0 to p_QT_BITS-1);
      i_RST     : in std_logic;
      i_ENA     : in std_logic;
		i_CLKn    : in std_logic;
      i_VALUE   : in integer := 0;
      o_VALUE   : out integer
    );
end CNN2FPGAVHDL;

architecture arch of CNN2FPGAVHDL is
begin
    u_CONV : entity work.convolutional_unit  -- Altere aqui
        generic map (p_QT_BITS)
        port map (
            i_DATA   => i_DATA,
            i_KERNEL => i_KERNEL,
            i_RST => i_RST,
            i_ENA => i_ENA,
            i_VALUE => i_VALUE,
            o_VALUE  => o_VALUE
        );
end arch;
