library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        generic (NC_SEL_WIDTH : integer := 1;
                 DATA_WIDTH : integer := 32);
        port (i_A : in t_ARRAY_OF_LOGIC_VECTOR(0 to (2**NC_SEL_WIDTH)-1)(DATA_WIDTH-1 downto 0):= (others => (others => '0');
              i_SEL : in std_logic_vector(NC_SEL_WIDTH - 1 DOWNTO 0):= (others => (others => '0');
              o_Q : out std_logic_vector(DATA_WIDTH-1 DOWNTO 0):= (others => (others => '0')
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        Multiplexer_2 : entity work.Multiplexer_2
        generic map (
            NC_SEL_WIDTH => 1,
            DATA_WIDTH => 32
        )
        port map (
            i_A  => i_A,
            i_SEL  => i_SEL,
            o_Q  => o_Q
        );

    end arc;