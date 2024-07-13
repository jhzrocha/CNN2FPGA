library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity arvore_soma_conv_6 is
        
        port (i_PORT_0 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PORT_1 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PORT_2 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PORT_3 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PORT_4 : in STD_LOGIC_VECTOR (7 downto 0);
              i_PORT_5 : in STD_LOGIC_VECTOR (7 downto 0);
              o_DATA : out STD_LOGIC_VECTOR (15 downto 0)
        );
    end arvore_soma_conv_6;
                 
    architecture arc of arvore_soma_conv_6 is
        type t_MAT is array(5 downto 0) of STD_LOGIC_VECTOR(15 downto 0);
        signal w_SUM_OUT_0 : STD_LOGIC_VECTOR(15 downto 0);
        signal w_SUM_OUT_1 : STD_LOGIC_VECTOR(15 downto 0);
        signal w_SUM_OUT_2 : STD_LOGIC_VECTOR(15 downto 0);
        signal w_SUM_OUT_3 : STD_LOGIC_VECTOR(15 downto 0);
        signal w_SUM_OUT_4 : STD_LOGIC_VECTOR(15 downto 0);
        signal w_ENTRADAS : t_MAT := (others =>  ( others => '0'));


        begin
            w_ENTRADAS(0)(7 downto 0) <= i_PORT_0;
            w_ENTRADAS(1)(7 downto 0) <= i_PORT_1;
            w_ENTRADAS(2)(7 downto 0) <= i_PORT_2;
            w_ENTRADAS(3)(7 downto 0) <= i_PORT_3;
            w_ENTRADAS(4)(7 downto 0) <= i_PORT_4;
            w_ENTRADAS(5)(7 downto 0) <= i_PORT_5;

            w_ENTRADAS(0)(15 downto 8) <= (others => '1') when (i_PORT_0 (7) = '1') else (others => '0');
            w_ENTRADAS(1)(15 downto 8) <= (others => '1') when (i_PORT_1 (7) = '1') else (others => '0');
            w_ENTRADAS(2)(15 downto 8) <= (others => '1') when (i_PORT_2 (7) = '1') else (others => '0');
            w_ENTRADAS(3)(15 downto 8) <= (others => '1') when (i_PORT_3 (7) = '1') else (others => '0');
            w_ENTRADAS(4)(15 downto 8) <= (others => '1') when (i_PORT_4 (7) = '1') else (others => '0');
            w_ENTRADAS(5)(15 downto 8) <= (others => '1') when (i_PORT_5 (7) = '1') else (others => '0');

            w_SUM_OUT_0 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(0)) + signed(w_ENTRADAS(1)));
            w_SUM_OUT_1 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(2)) + signed(w_ENTRADAS(3)));
            w_SUM_OUT_2 <= STD_LOGIC_VECTOR(signed(w_ENTRADAS(4)) + signed(w_ENTRADAS(5)));

            w_SUM_OUT_3 <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_0) + signed(w_SUM_OUT_1));

            o_DATA <= STD_LOGIC_VECTOR(signed(w_SUM_OUT_2) + signed(w_SUM_OUT_3));

        
    end arc;