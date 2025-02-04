library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity FullyConnectedLayer is
        
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_GO : in std_logic;
              i_PIX : in std_logic_vector(7 downto 0):= (others => '0');
              o_PIX : out o_PIX_FullyConnectedLayer:= (others => (others => '0'));
              o_READ_ADDR : out std_logic_vector(7 downto 0);
              o_READY : out std_logic
        );
    end FullyConnectedLayer;
                 
    architecture arc of FullyConnectedLayer is
        signal w_REG_PIX_ENA : std_logic;
        signal w_REG_WEIGHT_ENA : std_logic;
        signal w_REG_BIAS_ENA : std_logic;
        signal w_ACC_ENA : std_logic;
        signal w_ACC_CLR : std_logic;
        signal w_REG_OUT_ENA : std_logic;
        signal w_REG_OUT_ADDR : std_logic_vector(5 downto 0) := (others => '0');
        signal w_WEIGHT_READ_ADDR : std_logic_vector(12 downto 0);
        signal w_BIAS_READ_ADDR : std_logic_vector(5 downto 0);
        signal w_IN_READ_ADDR : std_logic_vector (7 downto 0);
        signal w_WEIGHT : std_logic_vector(7 downto 0) := (others => '0');
        signal w_ROM_OUT : std_logic_vector (7 downto 0) := (others => '0');
        signal w_BIAS_SCALE : std_logic_vector(31 downto 0);


        begin 
        u_ROM_WEIGHTS : entity work.conv_weights
        generic map (
            init_file_name => "test1.mif",
            DATA_WIDTH => 8,
            DATA_DEPTH => 13
        )
        port map (
            address  => w_WEIGHT_READ_ADDR,
            clock  => i_CLK,
            rden  => '1',
            q  => w_ROM_OUT
        );
 
        u_ROM_BIAS : entity work.conv_bias
        generic map (
            init_file_name => "test2.mif",
            DATA_WIDTH => 32,
            DATA_DEPTH => 6
        )
        port map (
            address  => w_BIAS_READ_ADDR,
            clken  => '1',
            clock  => i_CLK,
            q  => w_BIAS_SCALE
        );
 
        u_CONTROLE : entity work.fullyConnectedControl_13_6_8
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_GO  => i_GO,
            o_READY  => o_READY,
            o_REG_PIX_ENA  => w_REG_PIX_ENA,
            o_REG_WEIGHT_ENA  => w_REG_WEIGHT_ENA,
            o_REG_BIAS_ENA  => w_REG_BIAS_ENA,
            o_ACC_ENA  => w_ACC_ENA,
            o_ACC_CLR  => w_ACC_CLR,
            o_REG_OUT_ENA  => w_REG_OUT_ENA,
            o_REG_OUT_ADDR  => w_REG_OUT_ADDR,
            o_WEIGHT_READ_ADDR  => w_WEIGHT_READ_ADDR,
            o_BIAS_READ_ADDR  => w_BIAS_READ_ADDR,
            o_IN_READ_ADDR  => w_IN_READ_ADDR
        );
 
        u_OPERACIONAL : entity work.FullyConnectedOperator
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX  => i_PIX,
            i_WEIGHT  => w_WEIGHT,
            i_REG_PIX_ENA  => w_REG_PIX_ENA,
            i_REG_WEIGHT_ENA  => w_REG_WEIGHT_ENA,
            i_BIAS_SCALE  => w_BIAS_SCALE,
            i_REG_BIAS_ADDR  => w_BIAS_READ_ADDR,
            i_REG_BIAS_ENA  => w_REG_BIAS_ENA,
            i_ACC_ENA  => w_ACC_ENA,
            i_ACC_CLR  => w_ACC_CLR,
            i_REG_OUT_CLR  => '0',
            i_REG_OUT_ENA  => w_REG_OUT_ENA,
            i_REG_OUT_ADDR  => w_REG_OUT_ADDR,
            o_PIX  => o_PIX
        );

  o_READ_ADDR <= w_IN_READ_ADDR;
  w_WEIGHT(0) <= w_ROM_OUT;
        
    end arc;