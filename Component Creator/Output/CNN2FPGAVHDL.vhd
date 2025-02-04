library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX : in std_logic_vector(7 downto 0):= (others => '0');
              o_PIX : out o_PIX_FullyConnectedLayer:= (others => (others => '0'));
              o_READ_ADDR : out std_logic_vector(7 downto 0);
              o_READY : out std_logic
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        FullyConnectedLayer : entity work.FullyConnectedLayer
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            i_PIX  => i_PIX,
            o_PIX  => o_PIX,
            o_READ_ADDR  => o_READ_ADDR,
            o_READY  => o_READY
        );

    end arc;