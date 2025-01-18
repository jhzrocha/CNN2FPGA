library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity neuron_8_32 is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_ACC_ENA : in std_logic;
              i_REG_PIX_ENA : in std_logic;
              i_REG_WEIGHT_ENA : in std_logic;
              i_ACC_CLR : in std_logic;
              i_PIX : in std_logic_vector (7 downto 0);
              i_WEIGHT : in std_logic_vector (7 downto 0);
              o_PIX : out std_logic_vector (31 downto 0)
        );
    end neuron_8_32;
                 
    architecture arc of neuron_8_32 is
        signal w_CLR_OR_ACC_CLR : std_logic;
        signal w_MULT_OUT : std_logic_vector(31 downto 0) := (others => '0');
        signal w_ADD_OUT : std_logic_vector(31 downto 0) := (others => '0');
        signal r_PIX : std_logic_vector(7 downto 0);
        signal r_WEIGHT : std_logic_vector(7 downto 0);
        signal r_ACC : std_logic_vector(31 downto 0);


        begin 
        u_REG_WEIGHT : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => i_REG_WEIGHT_ENA,
            i_A  => i_WEIGHT,
            o_Q  => r_WEIGHT
        );
 
        u_REG_PIX : entity work.registrador_8b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => i_REG_PIX_ENA,
            i_A  => i_PIX,
            o_Q  => r_PIX
        );
 
        u_REG_ACC : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => w_CLR_OR_ACC_CLR,
            i_ENA  => i_ACC_ENA,
            i_A  => w_ADD_OUT,
            o_Q  => r_ACC
        );
 
        u_MULT : entity work.multiplicador_conv_8_16
        port map (
            i_DATA_1  => r_PIX,
            i_DATA_2  => r_WEIGHT,
            o_DATA  => w_MULT_OUT(15 downto 0)
        );

         -- extende sinal
       w_CLR_OR_ACC_CLR <= i_CLR or i_ACC_CLR;
       
       w_MULT_OUT(31 downto 16) <= (others => '1') when (w_MULT_OUT(15) = '1') else
       (others                             => '0');

       -- somador
       w_ADD_OUT <= std_logic_vector(signed(r_ACC) + signed(w_MULT_OUT));

       -- saida
       o_PIX <= w_ADD_OUT;

    end arc;