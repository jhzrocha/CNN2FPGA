library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity poolingOperator_6_8_10 is
        
        port (i_CLK : in STD_LOGIC;
              i_CLR : in STD_LOGIC;
              i_PIX_SHIFT_ENA : in STD_LOGIC;
              i_IN_DATA : in t_i_IN_DATA_poolingOperator_6_8_10;
              i_IN_WRITE_ENA : in STD_LOGIC;
              i_IN_SEL_LINE : in std_logic_vector (1 downto 0);
              i_IN_READ_ADDR_0 : in std_logic_vector (9 downto 0):= (others => '0');
              i_IN_READ_ADDR_1 : in std_logic_vector (9 downto 0):= (others => '0');
              i_IN_READ_ADDR_2 : in std_logic_vector (9 downto 0):= (others => '0');
              i_IN_WRITE_ADDR : in std_logic_vector (9 downto 0):= (others => '0');
              i_OUT_WRITE_ENA : in STD_LOGIC;
              i_OUT_SEL_LINE : in std_logic_vector (1 downto 0);
              i_OUT_READ_ADDR_0 : in std_logic_vector (9 downto 0):= (others => '0');
              i_OUT_WRITE_ADDR : in std_logic_vector (9 downto 0):= (others => '0');
              o_BUFFER_OUT : out t_i_IN_DATA_poolingOperator_6_8_10
        );
    end poolingOperator_6_8_10;
                 
    architecture arc of poolingOperator_6_8_10 is
        signal w_PIX_ROW_0 : t_i_IN_DATA_poolingOperator_6_8_10 := (others => (others => '0'));
        signal w_PIX_ROW_1 : t_i_IN_DATA_poolingOperator_6_8_10 := (others => (others => '0'));
        signal w_o_PIX : t_i_IN_DATA_poolingOperator_6_8_10 := (others => (others => '0'));


        begin 
        u_BUFFER_IN_0 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(0),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR_0,
            i_READ_ADDR_1  => i_IN_READ_ADDR_1,
            o_DATA_ROW_0  => w_PIX_ROW_0(0),
            o_DATA_ROW_1  => w_PIX_ROW_1(0)
        );
 
        u_MAX_POOL_0 : entity work.PoolingComputer8dw_2x2
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => w_PIX_ROW_0(0),
            i_PIX_ROW_1  => w_PIX_ROW_1(0),
            o_PIX  => w_o_PIX(0)
        );
 
        u_BUFFER_OUT_0 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_o_PIX(0),
            i_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_SEL_LINE  => i_OUT_SEL_LINE,
            i_WRITE_ADDR  => i_OUT_WRITE_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_READ_ADDR_1  => (others => '0'),
            o_DATA_ROW_0  => o_BUFFER_OUT(0)
        );
 
        u_BUFFER_IN_1 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(1),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR_0,
            i_READ_ADDR_1  => i_IN_READ_ADDR_1,
            o_DATA_ROW_0  => w_PIX_ROW_0(1),
            o_DATA_ROW_1  => w_PIX_ROW_1(1)
        );
 
        u_MAX_POOL_1 : entity work.PoolingComputer8dw_2x2
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => w_PIX_ROW_0(1),
            i_PIX_ROW_1  => w_PIX_ROW_1(1),
            o_PIX  => w_o_PIX(1)
        );
 
        u_BUFFER_OUT_1 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_o_PIX(1),
            i_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_SEL_LINE  => i_OUT_SEL_LINE,
            i_WRITE_ADDR  => i_OUT_WRITE_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_READ_ADDR_1  => (others => '0'),
            o_DATA_ROW_0  => o_BUFFER_OUT(1)
        );
 
        u_BUFFER_IN_2 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(2),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR_0,
            i_READ_ADDR_1  => i_IN_READ_ADDR_1,
            o_DATA_ROW_0  => w_PIX_ROW_0(2),
            o_DATA_ROW_1  => w_PIX_ROW_1(2)
        );
 
        u_MAX_POOL_2 : entity work.PoolingComputer8dw_2x2
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => w_PIX_ROW_0(2),
            i_PIX_ROW_1  => w_PIX_ROW_1(2),
            o_PIX  => w_o_PIX(2)
        );
 
        u_BUFFER_OUT_2 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_o_PIX(2),
            i_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_SEL_LINE  => i_OUT_SEL_LINE,
            i_WRITE_ADDR  => i_OUT_WRITE_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_READ_ADDR_1  => (others => '0'),
            o_DATA_ROW_0  => o_BUFFER_OUT(2)
        );
 
        u_BUFFER_IN_3 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(3),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR_0,
            i_READ_ADDR_1  => i_IN_READ_ADDR_1,
            o_DATA_ROW_0  => w_PIX_ROW_0(3),
            o_DATA_ROW_1  => w_PIX_ROW_1(3)
        );
 
        u_MAX_POOL_3 : entity work.PoolingComputer8dw_2x2
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => w_PIX_ROW_0(3),
            i_PIX_ROW_1  => w_PIX_ROW_1(3),
            o_PIX  => w_o_PIX(3)
        );
 
        u_BUFFER_OUT_3 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_o_PIX(3),
            i_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_SEL_LINE  => i_OUT_SEL_LINE,
            i_WRITE_ADDR  => i_OUT_WRITE_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_READ_ADDR_1  => (others => '0'),
            o_DATA_ROW_0  => o_BUFFER_OUT(3)
        );
 
        u_BUFFER_IN_4 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(4),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR_0,
            i_READ_ADDR_1  => i_IN_READ_ADDR_1,
            o_DATA_ROW_0  => w_PIX_ROW_0(4),
            o_DATA_ROW_1  => w_PIX_ROW_1(4)
        );
 
        u_MAX_POOL_4 : entity work.PoolingComputer8dw_2x2
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_PIX_ROW_0  => w_PIX_ROW_0(4),
            i_PIX_ROW_1  => w_PIX_ROW_1(4),
            o_PIX  => w_o_PIX(4)
        );
 
        u_BUFFER_OUT_4 : entity work.IOBuffer_2b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_o_PIX(4),
            i_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_SEL_LINE  => i_OUT_SEL_LINE,
            i_WRITE_ADDR  => i_OUT_WRITE_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR_0,
            i_READ_ADDR_1  => (others => '0'),
            o_DATA_ROW_0  => o_BUFFER_OUT(4)
        );
 
    end arc;