library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity ComparisonTree_4i_8dw is
        
        port (i_PIX_0 : in std_logic_vector (7 downto 0);
              i_PIX_1 : in std_logic_vector (7 downto 0);
              i_PIX_2 : in std_logic_vector (7 downto 0);
              i_PIX_3 : in std_logic_vector (7 downto 0);
              o_PIX : out std_logic_vector (7 downto 0)
        );
    end ComparisonTree_4i_8dw;
                 
    architecture arc of ComparisonTree_4i_8dw is
        signal w_PIX_OUT_0 : std_logic_vector (7 downto 0);
        signal w_PIX_OUT_1 : std_logic_vector (7 downto 0);
        signal w_PIX_OUT_2 : std_logic_vector (7 downto 0);


        begin
             w_PIX_OUT_0 <=  i_PIX_0 when (i_PIX_0 > i_PIX_1) else i_PIX_1;
             w_PIX_OUT_1 <=  i_PIX_2 when (i_PIX_2 > i_PIX_3) else i_PIX_3;


             o_PIX <= w_PIX_OUT_0 when (w_PIX_OUT_0 > w_PIX_OUT_1) else w_PIX_OUT_1;

    end arc;