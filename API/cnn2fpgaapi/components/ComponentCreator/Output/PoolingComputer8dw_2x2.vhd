library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity PoolingComputer8dw_2x2 is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_PIX_SHIFT_ENA : in std_logic;
              i_PIX_ROW_0 : in std_logic_vector (7 downto 0);
              i_PIX_ROW_1 : in std_logic_vector (7 downto 0);
              o_PIX : out std_logic_vector (7 downto 0)
        );
    end PoolingComputer8dw_2x2;
                 
    architecture arc of PoolingComputer8dw_2x2 is
        type t_MAT_PoolingComputer8dw_2x2 is array(1 downto 0) of std_logic_vector(7 downto 0);
        signal w_PIX_ROW_0 : t_MAT_PoolingComputer8dw_2x2 := (others => (others => '0'));
        signal w_PIX_ROW_1 : t_MAT_PoolingComputer8dw_2x2 := (others => (others => '0'));


        begin 
        u_MAX_TREE : entity work.MaxComparisonTree_4i_8dw
        port map (
            i_PIX_0  => w_PIX_ROW_0(0),
            i_PIX_1  => w_PIX_ROW_0(1),
            i_PIX_2  => w_PIX_ROW_1(0),
            i_PIX_3  => w_PIX_ROW_1(1),
            o_PIX  => o_PIX
        );

  p_DESLOCAMENTO : process (i_CLR, i_CLK)
  begin
    -- reset
    if (i_CLR = '1') then
         w_PIX_ROW_0 <= (others => (others => '0'));
         w_PIX_ROW_1 <= (others => (others => '0'));

    elsif (rising_edge(i_CLK)) then
      -- desloca registradores de pixels
      if (i_PIX_SHIFT_ENA = '1') then
         w_PIX_ROW_0(1) <= w_PIX_ROW_0(0);
         w_PIX_ROW_1(1) <= w_PIX_ROW_1(0);
         w_PIX_ROW_0(0) <= i_PIX_ROW_0;
         w_PIX_ROW_1(0) <= i_PIX_ROW_1;

      end if;
    end if;
  end process;
        
    end arc;