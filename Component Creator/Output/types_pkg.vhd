
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
        type t_ARRAY_OF_LOGIC_VECTOR_mult4 is array(3 downto 0) of std_logic_vector(31 downto 0);

type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_inData is array(0 to 2) of std_logic_vector(7 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_outData is array(0 to 2) of std_logic_vector(7 downto 0);
type t_ARRAY_OF_LOGIC_VECTOR_GenericDemultiplexer_3_32b is array (0 to (2 ** 3) - 1) of std_logic_vector(32 downto 0);
type t_ARRAY_OF_INTEGER is array (integer range <>) of integer;
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_NC is array(0 to 3) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_MUX_NC is array(0 to 2) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_ADD is array(0 to 2) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_BIAS_ACC is array(0 to 2) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_BIAS_REG is array(0 to 2) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_o_SCALE_REG is array(0 to 2) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_DEMUX_OUT is array(0 to 7) of std_logic_vector(31 downto 0);
type conv1_op_3b_3r_3c_3ppr_3c_3f_5wsa_18ohe_8dw_32dwn_10adw_3odwsb_5baw_w_MUX_I_VET is array(0 to 3) of std_logic_vector(31 downto 0);

    END PACKAGE types_pkg;