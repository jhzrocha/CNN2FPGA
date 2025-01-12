library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity CNN2FPGAVHDL is
        generic (SCALE_SHIFT : t_ARRAY_OF_INTEGER);
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_IN_READ_ENA : in std_logic;
              i_IN_DATA : in conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_inData;
              i_IN_WRITE_ENA : in std_logic;
              i_IN_SEL_LINE : in std_logic_vector (1 downto 0);
              i_IN_READ_ADDR0 : in std_logic_vector (9  downto 0);
              i_IN_READ_ADDR1 : in std_logic_vector (9 downto 0);
              i_IN_READ_ADDR2 : in std_logic_vector (9 downto 0);
              i_IN_WRITE_ADDR : in std_logic_vector (9 downto 0);
              i_WEIGHT : in std_logic_vector(7 downto 0);
              i_BIAS : in std_logic_vector (31 downto 0);
              i_BIAS_WRITE_ENA : in std_logic;
              i_SCALE_WRITE_ENA : in std_logic;
              i_PIX_SHIFT_ENA : in std_logic;
              i_WEIGHT_SHIFT_ENA : in std_logic;
              i_WEIGHT_SHIFT_ADDR : in std_logic_vector(4 downto 0);
              i_WEIGHT_ROW_SEL : in std_logic_vector(1 downto 0);
              i_NC_O_SEL : in std_logic_vector(1 DOWNTO 0);
              i_ACC_ENA : in std_logic;
              i_ACC_RST : in std_logic;
              i_ROW_SEL : in std_logic_vector(1 downto 0);
              i_OUT_SEL : in std_logic_vector(2 downto 0):= (others => '0');
              i_OUT_WRITE_ENA : in std_logic;
              i_OUT_READ_ENA : in std_logic;
              i_OUT_READ_ADDR : in std_logic_vector (9 downto 0):= (others => '0');
              i_OUT_INC_ADDR : in std_logic;
              i_OUT_CLR_ADDR : in std_logic;
              o_OUT_DATA : out conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_outData
        );
    end CNN2FPGAVHDL;
                 
    architecture arc of CNN2FPGAVHDL is


        begin 
        conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw : entity work.conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw
        generic map (
            SCALE_SHIFT => 
        )
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_IN_READ_ENA  => i_IN_READ_ENA,
            i_IN_DATA  => i_IN_DATA,
            i_IN_WRITE_ENA  => i_IN_WRITE_ENA,
            i_IN_SEL_LINE  => i_IN_SEL_LINE,
            i_IN_READ_ADDR0  => i_IN_READ_ADDR0,
            i_IN_READ_ADDR1  => i_IN_READ_ADDR1,
            i_IN_READ_ADDR2  => i_IN_READ_ADDR2,
            i_IN_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_WEIGHT  => i_WEIGHT,
            i_BIAS  => i_BIAS,
            i_BIAS_WRITE_ENA  => i_BIAS_WRITE_ENA,
            i_SCALE_WRITE_ENA  => i_SCALE_WRITE_ENA,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_WEIGHT_SHIFT_ENA  => i_WEIGHT_SHIFT_ENA,
            i_WEIGHT_SHIFT_ADDR  => i_WEIGHT_SHIFT_ADDR,
            i_WEIGHT_ROW_SEL  => i_WEIGHT_ROW_SEL,
            i_NC_O_SEL  => i_NC_O_SEL,
            i_ACC_ENA  => i_ACC_ENA,
            i_ACC_RST  => i_ACC_RST,
            i_ROW_SEL  => i_ROW_SEL,
            i_OUT_SEL  => i_OUT_SEL,
            i_OUT_WRITE_ENA  => i_OUT_WRITE_ENA,
            i_OUT_READ_ENA  => i_OUT_READ_ENA,
            i_OUT_READ_ADDR  => i_OUT_READ_ADDR,
            i_OUT_INC_ADDR  => i_OUT_INC_ADDR,
            i_OUT_CLR_ADDR  => i_OUT_CLR_ADDR,
            o_OUT_DATA  => o_OUT_DATA
        );

    end arc;