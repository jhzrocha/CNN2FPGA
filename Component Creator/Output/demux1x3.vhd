library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity demux1x3 is
        generic (i_DATA_WIDTH : integer := 8;
                 w_CONV_OUT : integer := 16;
                 o_DATA_WIDTH : integer := 32;
                 i_WIDTH : integer := 8);
        port (i_A  : in std_logic_vector(i_WIDTH DOWNTO 0);
              i_SEL : in std_logic_vector (i_WIDTH-1 DOWNTO 0);
              o_PORT_0 : out std_logic_vector('i_WIDTH'-1 DOWNTO 0);
              o_PORT_1 : out std_logic_vector('i_WIDTH'-1 DOWNTO 0);
              o_PORT_2 : out std_logic_vector('i_WIDTH'-1 DOWNTO 0)
        );
    end demux1x3;
                 
    architecture arc of demux1x3 is
        type t_MAT is array(1 downto 0) of STD_LOGIC_VECTOR(i_DATA_WIDTH - 1 downto 0);
        type t_MULT_OUT_MAT is array(7 downto 0) of STD_LOGIC_VECTOR(w_CONV_OUT - 1 downto 0);


        begin
        o_PORT_0 <= i_A when (i_SEL ="00") else (others =>  '0');
        o_PORT_1 <= i_A when (i_SEL ="01") else (others =>  '0');
        o_PORT_2 <= i_A when (i_SEL ="10") else (others =>  '0');

        
    end arc;