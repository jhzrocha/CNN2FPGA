library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity FullyConnected0idx_1chs is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX_0 : in i_A_Multiplexer_64_8b:= (others => (others => '0'));
              o_READY : out std_logic;
              o_PIX_0 : out o_PIX_FullyConnectedOperator:= (others => (others => '0'));
              o_READ_ADDR_0 : out std_logic_vector(6 downto 0):= (others => '0')
        );
    end FullyConnected0idx_1chs;
                 
    architecture arc of FullyConnected0idx_1chs is
        signal w_CHANNEL_0_READY : std_logic;


        begin 
        fcLayerChannel_0 : entity work.FullyConnectedLayer_8dw_2un_3l15n_RELU_8wfdw
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            i_PIX  => i_PIX_0,
            o_PIX  => o_PIX_0,
            o_READ_ADDR  => o_READ_ADDR_0,
            o_READY  => w_CHANNEL_0_READY
        );

            o_READY <=  w_CHANNEL_0_READY;
        
    end arc;