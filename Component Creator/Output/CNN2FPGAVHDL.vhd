library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_PIX : in std_logic_vector(7 downto 0);
              i_WEIGHT : in i_WEIGHT_FullyConnectedOperator;
              i_REG_PIX_ENA : in std_logic;
              i_REG_WEIGHT_ENA : in std_logic;
              i_BIAS_SCALE : in std_logic_vector(31 downto 0);
              i_REG_BIAS_ADDR : in std_logic_vector(5 downto 0);
              i_REG_BIAS_ENA : in std_logic;
              i_ACC_ENA : in std_logic;
              i_ACC_CLR : in std_logic;
              i_REG_OUT_CLR : in std_logic:= '0';
              i_REG_OUT_ENA : in std_logic;
              i_REG_OUT_ADDR : in std_logic_vector(5 downto 0):= (others => '0');
              o_PIX : out o_PIX_FullyConnectedOperator:= (others => (others => '0'))
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        FullyConnectedOperator : entity work.FullyConnectedOperator
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX  => i_PIX,
            i_WEIGHT  => i_WEIGHT,
            i_REG_PIX_ENA  => i_REG_PIX_ENA,
            i_REG_WEIGHT_ENA  => i_REG_WEIGHT_ENA,
            i_BIAS_SCALE  => i_BIAS_SCALE,
            i_REG_BIAS_ADDR  => i_REG_BIAS_ADDR,
            i_REG_BIAS_ENA  => i_REG_BIAS_ENA,
            i_ACC_ENA  => i_ACC_ENA,
            i_ACC_CLR  => i_ACC_CLR,
            i_REG_OUT_CLR  => i_REG_OUT_CLR,
            i_REG_OUT_ENA  => i_REG_OUT_ENA,
            i_REG_OUT_ADDR  => i_REG_OUT_ADDR,
            o_PIX  => o_PIX
        );

    end arc;