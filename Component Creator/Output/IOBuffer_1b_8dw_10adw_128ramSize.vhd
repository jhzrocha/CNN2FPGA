library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity IOBuffer_1b_8dw_10adw_128ramSize is
        
        port (i_CLK : in std_logic;
              i_DATA : in std_logic_vector (7 downto 0);
              i_WRITE_ENA : in std_logic;
              i_SEL_LINE : in std_logic_vector (0 downto 0);
              i_WRITE_ADDR : in std_logic_vector (9 downto 0):= (others => '0');
              i_READ_ADDR_0 : in std_logic_vector (9 downto 0):= (others => '0');
              o_DATA_ROW_0 : out std_logic_vector (7 downto 0)
        );
    end IOBuffer_1b_8dw_10adw_128ramSize;
                 
    architecture arc of IOBuffer_1b_8dw_10adw_128ramSize is
        type t_BLOCKS_ADDR is array(2 downto 0) of STD_LOGIC_VECTOR(9 downto 0);
        signal w_ADDRs : t_BLOCKS_ADDR := (others => (others => '0'));
        signal w_WRITE_ENA : STD_LOGIC_VECTOR(0 downto 0) := (others => '0');


        begin 
        ram0 : entity work.RAM_10_8b_128
        port map (
            i_CLK  => i_CLK,
            i_ADDR  => w_ADDRs(0),
            i_DATA  => i_DATA,
            i_WRITE  => w_WRITE_ENA(0),
            o_DATA  => o_DATA_ROW_0
        );

            w_ADDRs(0) <= i_WRITE_ADDR when (i_WRITE_ENA = '1') else i_READ_ADDR_0;
            w_WRITE_ENA(0) <= '1' when (i_SEL_LINE = "0") and (i_WRITE_ENA = '1') else '0';
    end arc;