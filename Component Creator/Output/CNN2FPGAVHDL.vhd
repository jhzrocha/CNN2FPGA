library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX_0 : in i_A_Multiplexer_64_8b:= (others => (others => '0'));
              o_READY : out std_logic;
              o_PIX_0 : out o_PIX_FullyConnectedOperator:= (others => (others => '0'));
              o_READ_ADDR_0 : out std_logic_vector(6 downto 0):= (others => '0')
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        FullyConnected0idx_1chs : entity work.FullyConnected0idx_1chs
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            i_PIX_0  => i_PIX_0,
            o_READY  => o_READY,
            o_PIX_0  => o_PIX_0,
            o_READ_ADDR_0  => o_READ_ADDR_0
        );

    end arc;