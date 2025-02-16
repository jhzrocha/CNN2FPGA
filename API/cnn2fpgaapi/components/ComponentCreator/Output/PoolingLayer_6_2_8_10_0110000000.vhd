library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity PoolingLayer_6_2_8_10_0110000000 is
        
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
    end PoolingLayer_6_2_8_10_0110000000;
                 
    architecture arc of PoolingLayer_6_2_8_10_0110000000 is
        signal w_IN_READ_ADDR_0 : std_logic_vector (9 downto 0);
        signal w_IN_READ_ADDR_1 : std_logic_vector (9 downto 0);
        signal w_PIX_SHIFT_ENA : std_logic;
        signal w_OUT_WRITE_ENA : std_logic;
        signal w_OUT_WRITE_ADDR : std_logic_vector (9 downto 0) := (others => '0');


        begin 
        u_CONTROLE : entity work.poolingController_2_8_10_0110000000
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            o_READY  => o_READY,
            o_PIX_SHIFT_ENA  => w_PIX_SHIFT_ENA,
            o_OUT_WRITE_ENA  => w_OUT_WRITE_ENA,
            o_OUT_WRITE_ADDR  => w_OUT_WRITE_ADDR,
            o_IN_READ_ADDR_0  => w_IN_READ_ADDR_0,
            o_IN_READ_ADDR_1  => w_IN_READ_ADDR_1
        );
 
        u_OPERACIONAL : entity work.poolingOperator_6_8_10
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => w_PIX_SHIFT_ENA,
            i_IN_DATA  => i_IN_DATA,
            i_IN_WRITE_ENA  => i_IN_WRITE_ENA,
            i_IN_SEL_LINE  => i_IN_SEL_LINE,
            i_IN_READ_ADDR_0  => w_IN_READ_ADDR_0,
            i_IN_READ_ADDR_1  => w_IN_READ_ADDR_1,
            i_IN_READ_ADDR_2  => (others => '0'),
            i_IN_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_OUT_WRITE_ENA  => w_OUT_WRITE_ENA,
            i_OUT_SEL_LINE  => "00",
            i_OUT_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_OUT_WRITE_ADDR  => w_OUT_WRITE_ADDR,
            o_BUFFER_OUT  => o_BUFFER_OUT
        );
 
    end arc;