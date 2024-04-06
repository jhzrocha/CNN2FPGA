library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        generic (NUM_BLOCKS : integer := 3;
                 DATA_WIDTH : integer := 8;
                 ADDR_WIDTH : integer := 10);
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_DATA : in std_logic_vector (DATA_WIDTH - 1 downto 0);
              i_READ_ENA : in std_logic;
              i_WRITE_ENA : in std_logic;
              i_SEL_LINE : in std_logic_vector (1 downto 0);
              i_READ_ADDR0 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_READ_ADDR1 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_READ_ADDR2 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_WRITE_ADDR : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_0 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_1 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_2 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0')
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        IOBuffer : entity work.IOBuffer
        generic map (
            NUM_BLOCKS => 3,
            DATA_WIDTH => 8,
            ADDR_WIDTH => 10
        )
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_DATA  => i_DATA,
            i_READ_ENA  => i_READ_ENA,
            i_WRITE_ENA  => i_WRITE_ENA,
            i_SEL_LINE  => i_SEL_LINE,
            i_READ_ADDR0  => i_READ_ADDR0,
            i_READ_ADDR1  => i_READ_ADDR1,
            i_READ_ADDR2  => i_READ_ADDR2,
            i_WRITE_ADDR  => i_WRITE_ADDR,
            o_DATA_ROW_0  => o_DATA_ROW_0,
            o_DATA_ROW_1  => o_DATA_ROW_1,
            o_DATA_ROW_2  => o_DATA_ROW_2
        );

    end arc;