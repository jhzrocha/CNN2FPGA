library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.types_pkg.all;
                 
    entity conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw is
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
    end conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw;
                 
    architecture arc of conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw is
        signal w_NC_PES_ADDR : std_logic_vector (17 downto 0);
        signal w_o_NC : t_ARRAY_OF_LOGIC_VECTOR_mult4 := (others => (others => '0'));
        signal w_o_MUX_NC : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_MUX_NC;
        signal w_o_ADD : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_ADD := (others => (others => '0'));
        signal w_o_BIAS_ACC : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_BIAS_ACC := (others => (others => '0'));
        signal r_OUT_ADDR : std_logic_vector(9 downto 0) := (others => '0');
        signal w_RST_OUT_ADDR : std_logic := '0';
        signal w_CONFIG0 : std_logic;
        signal w_CONFIG1 : std_logic;
        signal w_BIAS_REG_ENA : std_logic_vector(2 downto 0);
        signal w_o_BIAS_REG : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_BIAS_REG;
        signal w_BIAS_WRITE_ENA : std_logic;
        signal w_SCALE_WRITE_ENA : std_logic;
        signal w_SCALE_REG_ENA : std_logic_vector(2 downto 0);
        signal w_o_SCALE_REG : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_SCALE_REG;
        signal w_ADD_OUT : STD_LOGIC_VECTOR(31  downto 0);
        signal w_o_SCALE_DOWN : std_logic_vector(63 downto 0) := (others => '0');
        signal w_o_CAST : std_logic_vector(31 downto 0) := (others => '0');
        signal w_DEMUX_OUT : t_ARRAY_OF_LOGIC_VECTOR_GenericDemultiplexer_3_32b := (others => (others => '0'));
        signal w_OUT_ADDR_ENA : std_logic_vector(2 downto 0) := (others => '0');
        signal w_RAM_PIX_ROW_1_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_RAM_PIX_ROW_2_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_RAM_PIX_ROW_3_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_1_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_2_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_3_0 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_o_PIX_0 : STD_LOGIC_VECTOR (31 downto 0) := (others => '0');
        signal w_WEIGHT_SHIFT_ENABLE_0 : std_logic := '0';
        signal w_MUX_I_VET_0 : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_MUX_I_VET := (others => (others => '0'));
        signal w_RAM_PIX_ROW_1_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_RAM_PIX_ROW_2_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_RAM_PIX_ROW_3_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_1_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_2_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_NC_PIX_ROW_3_1 : STD_LOGIC_VECTOR (7 downto 0);
        signal w_o_PIX_1 : STD_LOGIC_VECTOR (31 downto 0) := (others => '0');
        signal w_WEIGHT_SHIFT_ENABLE_1 : std_logic := '0';
        signal w_MUX_I_VET_1 : conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_MUX_I_VET := (others => (others => '0'));
        signal w_255_CLIP_0 : std_logic_vector (7 downto 0);
        signal w_OUT_WRITE_ENA_0 : std_logic;
        signal w_GTHAN_255_0 : std_logic;
        signal w_255_CLIP_1 : std_logic_vector (7 downto 0);
        signal w_OUT_WRITE_ENA_1 : std_logic;
        signal w_GTHAN_255_1 : std_logic;


        begin 
        MUXX : entity work.Multiplexer_4_32b
        port map (
            i_A  => w_o_NC,
            i_SEL  => i_NC_O_SEL,
            o_Q  => w_o_MUX_NC(0)
        );
 
        u_DEMUX : entity work.GenericDemultiplexer_3_32b
        port map (
            i_A  => w_o_CAST,
            i_SEL  => i_OUT_SEL,
            o_Q  => w_DEMUX_OUT
        );
 
        io_buffer_0 : entity work.IOBuffer_3b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(0),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR0,
            i_READ_ADDR_1  => i_IN_READ_ADDR1,
            i_READ_ADDR_2  => i_IN_READ_ADDR2,
            o_DATA_ROW_0  => w_RAM_PIX_ROW_1_0,
            o_DATA_ROW_1  => w_RAM_PIX_ROW_2_0,
            o_DATA_ROW_2  => w_RAM_PIX_ROW_3_0
        );
 
        NCX_0 : entity work.nucleoConvolucional_3_3_3_8_16_32
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_WEIGHT_SHIFT_ENA  => w_WEIGHT_SHIFT_ENABLE_0,
            i_WEIGHT  => i_WEIGHT,
            i_PIX_ROW_0  => w_NC_PIX_ROW_1_0,
            i_PIX_ROW_1  => w_NC_PIX_ROW_2_0,
            i_PIX_ROW_2  => w_NC_PIX_ROW_3_0,
            i_WEIGHT_ROW_SEL  => i_WEIGHT_ROW_SEL,
            o_PIX  => w_o_PIX_0
        );
 
        registrador_0 : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => '1',
            i_A  => w_o_PIX_0,
            o_Q  => w_o_NC(0)
        );
 
        io_buffer_1 : entity work.IOBuffer_3b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => i_IN_DATA(1),
            i_WRITE_ENA  => i_IN_WRITE_ENA,
            i_SEL_LINE  => i_IN_SEL_LINE,
            i_WRITE_ADDR  => i_IN_WRITE_ADDR,
            i_READ_ADDR_0  => i_IN_READ_ADDR0,
            i_READ_ADDR_1  => i_IN_READ_ADDR1,
            i_READ_ADDR_2  => i_IN_READ_ADDR2,
            o_DATA_ROW_0  => w_RAM_PIX_ROW_1_1,
            o_DATA_ROW_1  => w_RAM_PIX_ROW_2_1,
            o_DATA_ROW_2  => w_RAM_PIX_ROW_3_1
        );
 
        NCX_1 : entity work.nucleoConvolucional_3_3_3_8_16_32
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_PIX_SHIFT_ENA  => i_PIX_SHIFT_ENA,
            i_WEIGHT_SHIFT_ENA  => w_WEIGHT_SHIFT_ENABLE_1,
            i_WEIGHT  => i_WEIGHT,
            i_PIX_ROW_0  => w_NC_PIX_ROW_1_1,
            i_PIX_ROW_1  => w_NC_PIX_ROW_2_1,
            i_PIX_ROW_2  => w_NC_PIX_ROW_3_1,
            i_WEIGHT_ROW_SEL  => i_WEIGHT_ROW_SEL,
            o_PIX  => w_o_PIX_1
        );
 
        registrador_1 : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => '1',
            i_A  => w_o_PIX_1,
            o_Q  => w_o_NC(1)
        );
 
        ADDX : entity work.add32
        port map (
            a  => w_o_ADD(0),
            b  => w_o_MUX_NC(0),
            cin  => '0',
            sum1  => w_ADD_OUT
        );
 
        REGX : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_ACC_RST,
            i_ENA  => i_ACC_ENA,
            i_A  => w_ADD_OUT,
            o_Q  => w_o_ADD(0)
        );
 
        BIAS_REGX : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_BIAS_WRITE_ENA,
            i_A  => i_BIAS,
            o_Q  => w_o_BIAS_REG(0)
        );
 
        SCALE_REGX : entity work.registrador_32b
        port map (
            i_CLK  => i_CLK,
            i_CLR  => i_CLR,
            i_ENA  => w_SCALE_WRITE_ENA,
            i_A  => i_BIAS,
            o_Q  => w_o_SCALE_REG(0)
        );
 
        OUT_BUFFER_0 : entity work.IOBuffer_1b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_255_CLIP_0,
            i_WRITE_ENA  => w_OUT_WRITE_ENA_0,
            i_SEL_LINE  => "0",
            i_WRITE_ADDR  => r_OUT_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR,
            o_DATA_ROW_0  => o_OUT_DATA(0)
        );
 
        OUT_BUFFER_1 : entity work.IOBuffer_1b_8dw_10adw_128ramSize
        port map (
            i_CLK  => i_CLK,
            i_DATA  => w_255_CLIP_1,
            i_WRITE_ENA  => w_OUT_WRITE_ENA_1,
            i_SEL_LINE  => "0",
            i_WRITE_ADDR  => r_OUT_ADDR,
            i_READ_ADDR_0  => i_OUT_READ_ADDR,
            o_DATA_ROW_0  => o_OUT_DATA(1)
        );
 
        u_OHE_PES : entity work.One_Hot_Encoder_5x18
        port map (
            i_DATA  => i_WEIGHT_SHIFT_ADDR,
            o_DATA  => w_NC_PES_ADDR
        );
 
        u_OHE_OUT_BUFF : entity work.One_Hot_Encoder_3x3
        port map (
            i_DATA  => i_OUT_SEL,
            o_DATA  => w_OUT_ADDR_ENA
        );
 
        u_OUT_ADDR : entity work.Counter_10dw_1bs
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_OUT_ADDR,
            i_INC  => i_OUT_INC_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => r_OUT_ADDR
        );

        w_CONFIG0 <= '1' when (i_ROW_SEL = "00") else '0';
        w_CONFIG1 <= '1' when (i_ROW_SEL = "01") else '0';        
        
     
                w_NC_PIX_ROW_1_0 <= w_RAM_PIX_ROW_1_0 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_2_0 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_3_0;
                w_NC_PIX_ROW_2_0 <= w_RAM_PIX_ROW_2_0 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_3_0 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_1_0;
                w_NC_PIX_ROW_3_0 <= w_RAM_PIX_ROW_3_0 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_1_0 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_2_0;
w_WEIGHT_SHIFT_ENABLE_0 <= w_NC_PES_ADDR(0) AND i_WEIGHT_SHIFT_ENA;
     
                w_NC_PIX_ROW_1_1 <= w_RAM_PIX_ROW_1_1 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_2_1 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_3_1;
                w_NC_PIX_ROW_2_1 <= w_RAM_PIX_ROW_2_1 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_3_1 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_1_1;
                w_NC_PIX_ROW_3_1 <= w_RAM_PIX_ROW_3_1 when (w_CONFIG0 = '1') else 
                                        w_RAM_PIX_ROW_1_1 when (w_CONFIG1 = '1') else
                                        w_RAM_PIX_ROW_2_1;
w_WEIGHT_SHIFT_ENABLE_1 <= w_NC_PES_ADDR(1) AND i_WEIGHT_SHIFT_ENA;
w_BIAS_WRITE_ENA <= i_BIAS_WRITE_ENA;
w_SCALE_WRITE_ENA <= i_SCALE_WRITE_ENA;
w_o_BIAS_ACC(0) <= std_logic_vector(unsigned(w_o_ADD(0)) + unsigned(w_o_BIAS_REG(0)));
w_o_SCALE_DOWN <= (others => '0') when (w_o_BIAS_ACC(0)(31) = '1') else std_logic_vector(unsigned(w_o_BIAS_ACC(0)) * unsigned(w_o_SCALE_REG(0)));
w_o_CAST(31 downto 0) <= w_o_SCALE_DOWN(63  downto 32 );
w_GTHAN_255_0 <= '1' when (w_o_CAST(31 downto SCALE_SHIFT(0)) > std_logic_vector(to_unsigned(255, 32))) else '0';
w_255_CLIP_0 <= "11111111" when (w_GTHAN_255_0 = '1') else w_DEMUX_OUT(0)(SCALE_SHIFT(0)+7 downto SCALE_SHIFT(0));
w_OUT_WRITE_ENA_0 <= '1' when (i_OUT_WRITE_ENA = '1' and w_OUT_ADDR_ENA(0) = '1') else '0';
w_GTHAN_255_1 <= '1' when (w_o_CAST(31 downto SCALE_SHIFT(1)) > std_logic_vector(to_unsigned(255, 32))) else '0';
w_255_CLIP_1 <= "11111111" when (w_GTHAN_255_1 = '1') else w_DEMUX_OUT(1)(SCALE_SHIFT(1)+7 downto SCALE_SHIFT(1));
w_OUT_WRITE_ENA_1 <= '1' when (i_OUT_WRITE_ENA = '1' and w_OUT_ADDR_ENA(1) = '1') else '0';
w_RST_OUT_ADDR <= '1' when (i_CLR = '1' or i_OUT_CLR_ADDR = '1') else '0';
    end arc;