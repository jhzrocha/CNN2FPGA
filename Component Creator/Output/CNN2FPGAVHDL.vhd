library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in STD_LOGIC;
              i_CLR : in STD_LOGIC;
              i_GO : in STD_LOGIC;
              o_READY : out STD_LOGIC;
              o_PIX_SHIFT_ENA : out STD_LOGIC;
              o_OUT_WRITE_ENA : out std_logic;
              o_OUT_WRITE_ADDR : out std_logic_vector (9 downto 0):= (others => '0');
              o_IN_READ_ADDR_0 : out std_logic_vector (9 downto 0):= (others => '0');
              o_IN_READ_ADDR_1 : out std_logic_vector (9 downto 0):= (others => '0')
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        poolingController : entity work.poolingController
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            o_READY  => o_READY,
            o_PIX_SHIFT_ENA  => o_PIX_SHIFT_ENA,
            o_OUT_WRITE_ENA  => o_OUT_WRITE_ENA,
            o_OUT_WRITE_ADDR  => o_OUT_WRITE_ADDR,
            o_IN_READ_ADDR_0  => o_IN_READ_ADDR_0,
            o_IN_READ_ADDR_1  => o_IN_READ_ADDR_1
        );

    end arc;