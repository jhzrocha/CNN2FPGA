library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity arvore_soma_conv_9_16_32 is
        
        port (i_PORT_0 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_1 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_2 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_3 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_4 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_5 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_6 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_7 : in STD_LOGIC_VECTOR (15 downto 0);
              i_PORT_8 : in STD_LOGIC_VECTOR (15 downto 0);
              o_DATA : out STD_LOGIC_VECTOR (31 downto 0)
        );
    end arvore_soma_conv_9_16_32;
                 
    architecture arc of arvore_soma_conv_9_16_32 is
        type t_MAT is array(8 downto 0) of STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_0 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_1 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_2 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_3 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_4 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_5 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_6 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_SUM_OUT_7 : STD_LOGIC_VECTOR(31 downto 0);
        signal w_ENTRADAS : t_MAT := (others =>  ( others => '0'));


        begin
            w_ENTRADAS(0)(15 downto 0) <= i_PORT_0;
            w_ENTRADAS(1)(15 downto 0) <= i_PORT_1;
            w_ENTRADAS(2)(15 downto 0) <= i_PORT_2;
            w_ENTRADAS(3)(15 downto 0) <= i_PORT_3;
            w_ENTRADAS(4)(15 downto 0) <= i_PORT_4;
            w_ENTRADAS(5)(15 downto 0) <= i_PORT_5;
            w_ENTRADAS(6)(15 downto 0) <= i_PORT_6;
            w_ENTRADAS(7)(15 downto 0) <= i_PORT_7;
            w_ENTRADAS(8)(15 downto 0) <= i_PORT_8;

            w_ENTRADAS(0)(31 downto 16) <= (others => '1') when (i_PORT_0 (15) = '1') else (others => '0');
            w_ENTRADAS(1)(31 downto 16) <= (others => '1') when (i_PORT_1 (15) = '1') else (others => '0');
            w_ENTRADAS(2)(31 downto 16) <= (others => '1') when (i_PORT_2 (15) = '1') else (others => '0');
            w_ENTRADAS(3)(31 downto 16) <= (others => '1') when (i_PORT_3 (15) = '1') else (others => '0');
            w_ENTRADAS(4)(31 downto 16) <= (others => '1') when (i_PORT_4 (15) = '1') else (others => '0');
            w_ENTRADAS(5)(31 downto 16) <= (others => '1') when (i_PORT_5 (15) = '1') else (others => '0');
            w_ENTRADAS(6)(31 downto 16) <= (others => '1') when (i_PORT_6 (15) = '1') else (others => '0');
            w_ENTRADAS(7)(31 downto 16) <= (others => '1') when (i_PORT_7 (15) = '1') else (others => '0');
            w_ENTRADAS(8)(31 downto 16) <= (others => '1') when (i_PORT_8 (15) = '1') else (others => '0');

            w_SUM_OUT_0 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(0)) + signed(w_ENTRADAS(1)));
            w_SUM_OUT_1 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(2)) + signed(w_ENTRADAS(3)));
            w_SUM_OUT_2 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(4)) + signed(w_ENTRADAS(5)));
            w_SUM_OUT_3 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(6)) + signed(w_ENTRADAS(7)));

            w_SUM_OUT_4 <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_0) + signed(w_SUM_OUT_1));
            w_SUM_OUT_5 <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_2) + signed(w_SUM_OUT_3));
            w_SUM_OUT_6 <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_4) + signed(w_SUM_OUT_5));

            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_6) + signed(w_ENTRADAS(8)));

        
    end arc;