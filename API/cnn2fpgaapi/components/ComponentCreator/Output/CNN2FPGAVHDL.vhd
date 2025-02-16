library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_IN_DATA : in t_i_IN_DATA_poolingOperator_6_8_10:= (others => (others => '0'));
              i_IN_WRITE_ENA : in std_logic;
              i_IN_WRITE_ADDR : in std_logic_vector (9 downto 0):= (others => '0');
              i_IN_SEL_LINE : in std_logic_vector (1 downto 0);
              i_OUT_READ_ADDR_0 : in std_logic_vector (9 downto 0):= (others => '0');
              o_READY : out std_logic;
              o_BUFFER_OUT : out t_i_IN_DATA_poolingOperator_6_8_10
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        PoolingLayer_6_2_8_10_0110000000 : entity work.PoolingLayer_6_2_8_10_0110000000
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            i_IN_DATA  => i_IN_DATA,
            i_IN_WRITE_ENA  => i_IN_WRITE_ENA,
            i_IN_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_IN_SEL_LINE  => i_IN_SEL_LINE,
            i_OUT_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            o_READY  => o_READY,
            o_BUFFER_OUT  => o_BUFFER_OUT
        );

    end arc;