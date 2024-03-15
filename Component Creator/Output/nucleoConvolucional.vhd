library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity nucleoConvolucional is
        generic (i_DATA_WIDTH : integer := 8;
                 w_CONV_OUT : integer := 16;
                 o_DATA_WIDTH : integer := 32;
                 i_WIDTH : integer := 8;
                 i_DATA_WIDTH : INTEGER := 8;
                 o_DATA_WIDTH : INTEGER := 16);
        port (i_CLK  : in STD_LOGIC;
              i_CLR : in STD_LOGIC;
              i_PIX_SHIFT_ENA : in STD_LOGIC;
              i_WEIGHT_SHIFT_ENA : in STD_LOGIC;
              i_WEIGHT : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              i_PIX_ROW : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
              o_PIX : out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)
        );
    end nucleoConvolucional;
                 
    architecture arc of nucleoConvolucional is
        type t_MAT is array(1 downto 0) of STD_LOGIC_VECTOR(i_DATA_WIDTH - 1 downto 0);
        type t_MULT_OUT_MAT is array(7 downto 0) of STD_LOGIC_VECTOR(w_CONV_OUT - 1 downto 0);
        signal w_PIX_ROW_0 : t_MAT  := (others =>  ( others => '0'));
        signal w_PIX_ROW_1 : t_MAT  := (others =>  ( others => '0'));
        signal w_PIX_ROW_2 : t_MAT  := (others =>  ( others => '0'));
        signal w_WEIGHT_ROW_0 : t_MAT  := (others =>  ( others => '0'));
        signal w_WEIGHT_ROW_1 : t_MAT  := (others =>  ( others => '0'));
        signal w_WEIGHT_ROW_2 : t_MAT  := (others =>  ( others => '0'));
        signal w_i_WEIGHT_ROW_0 : STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
        signal w_i_WEIGHT_ROW_1 : STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
        signal w_i_WEIGHT_ROW_2 : STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
        signal w_MULT_OUT : t_MULT_OUT_MAT := (others =>  ( others => '0'));


        begin 
        u_DEMUX_PEX : entity work.demux1x3
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_A   => ,
            i_SEL  => ,
            o_PORT_0  => ,
            o_PORT_1  => ,
            o_PORT_2  => 
        );
 
        multiplicador_conv_0 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_1 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_2 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_3 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_4 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_5 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_6 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_7 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );
 
        multiplicador_conv_8 : entity work.multiplicador_conv
        generic map (
            i_DATA_WIDTH => 8,
            w_CONV_OUT => 16,
            o_DATA_WIDTH => 32,
            i_WIDTH => 8,
            i_DATA_WIDTH => 8,
            o_DATA_WIDTH => 16
        )
        port map (
            i_DATA_1   => ,
            i_DATA_2  => ,
            o_DATA     => 
        );

        p_DESLOCAMENTO : process (i_CLR, i_CLK)
            begin
            -- reset
            if (i_CLR = '1') then
                w_PIX_ROW_0 <= (others =>  ( others => '0'));
                w_PIX_ROW_1 <= (others =>  ( others => '0'));
                w_PIX_ROW_2 <= (others =>  ( others => '0'));

                w_WEIGHT_ROW_0 <= (others =>  ( others => '0'));
                w_WEIGHT_ROW_1 <= (others =>  ( others => '0'));
                w_WEIGHT_ROW_2 <= (others =>  ( others => '0'));

            elsif (rising_edge(i_CLK)) then
                if (i_PIX_SHIFT_ENA = '1') then
                  w_PIX_ROW_0(2) <= w_PIX_ROW_0(1);
                  w_PIX_ROW_1(2) <= w_PIX_ROW_1(1);
                  w_PIX_ROW_2(2) <= w_PIX_ROW_2(1);

                  w_PIX_ROW_0(1) <= w_PIX_ROW_0(0);
                  w_PIX_ROW_1(1) <= w_PIX_ROW_1(0);
                  w_PIX_ROW_2(1) <= w_PIX_ROW_2(0);

                  w_PIX_ROW_0(0) <= i_PIX_ROW_0;
                  w_PIX_ROW_1(0) <= i_PIX_ROW_1;
                  w_PIX_ROW_2(0) <= i_PIX_ROW_2;

                end if;
            if (i_WEIGHT_SHIFT_ENA = '1' and i_WEIGHT_ROW_SEL = "00") then
               w_WEIGHT_ROW_0(2) <= w_WEIGHT_ROW_0(1);
               w_WEIGHT_ROW_0(1) <= w_WEIGHT_ROW_0(0);
               w_WEIGHT_ROW_0(0) <= w_i_WEIGHT_ROW_0;
            end if;
            if (i_WEIGHT_SHIFT_ENA = '1' and i_WEIGHT_ROW_SEL = "01") then
               w_WEIGHT_ROW_1(2) <= w_WEIGHT_ROW_1(1);
               w_WEIGHT_ROW_1(1) <= w_WEIGHT_ROW_1(0);
               w_WEIGHT_ROW_1(0) <= w_i_WEIGHT_ROW_1;
            end if;
            if (i_WEIGHT_SHIFT_ENA = '1' and i_WEIGHT_ROW_SEL = "10") then
               w_WEIGHT_ROW_2(2) <= w_WEIGHT_ROW_2(1);
               w_WEIGHT_ROW_2(1) <= w_WEIGHT_ROW_2(0);
               w_WEIGHT_ROW_2(0) <= w_i_WEIGHT_ROW_2;
            end if;

            end if;        
        end process;

    end arc;