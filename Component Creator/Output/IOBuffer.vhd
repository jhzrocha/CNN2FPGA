library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity IOBuffer is
        generic (NUM_BLOCKS : integer := 3;
                 DATA_WIDTH : integer := 8;
                 ADDR_WIDTH : integer := 10);
        port (i_CLK : in std_logic;
              i_CLR : in std_logic;
              i_DATA : in std_logic_vector (DATA_WIDTH - 1 downto 0);
              i_READ_ENA : in std_logic;
              i_WRITE_ENA : in std_logic;
              i_SEL_LINE : in std_logic_vector (1 downto 0);
              i_READ_ADDR0 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_READ_ADDR1 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_READ_ADDR2 : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              i_WRITE_ADDR : in std_logic_vector (ADDR_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_0 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_1 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0');
              o_DATA_ROW_2 : out std_logic_vector (DATA_WIDTH - 1 downto 0):= (others => '0')
        );
    end IOBuffer;
                 
    architecture arc of IOBuffer is
        type t_BLOCKS_DATA is array(2 downto 0) of STD_LOGIC_VECTOR(DATA_WIDTH - 1 downto 0);
        type t_BLOCKS_ADDR is array(2 downto 0) of STD_LOGIC_VECTOR(ADDR_WIDTH - 1 downto 0);
        signal w_ADDRs : t_BLOCKS_ADDR := (others => (others => '0'));
        signal w_BLOCK_OUT : t_BLOCKS_DATA := (others => (others => '0'));
        signal w_WRITE_ENA : STD_LOGIC_VECTOR(2 downto 0) := (others => '0');


        begin            
            -- endereco  
            w_ADDRs(0) <= i_WRITE_ADDR when (i_WRITE_ENA = '1') else i_READ_ADDR0;
            w_ADDRs(1) <= i_WRITE_ADDR when (i_WRITE_ENA = '1') else i_READ_ADDR1;
            w_ADDRs(2) <= i_WRITE_ADDR when (i_WRITE_ENA = '1') else i_READ_ADDR2;
                            
                            
            -- enable buffers
            w_WRITE_ENA(0) <= not i_SEL_LINE(1) and not i_SEL_LINE(0) and i_WRITE_ENA;
            w_WRITE_ENA(1) <= not i_SEL_LINE(1) and     i_SEL_LINE(0) and i_WRITE_ENA;
            w_WRITE_ENA(2) <=     i_SEL_LINE(1) and not i_SEL_LINE(0) and i_WRITE_ENA;
            
            
            -- blocos de memoria
            GEN_BLOCK: 
                for i in 0 to NUM_BLOCKS-1 generate
                ramx : work.generic_ram
                            generic map (DATA_WIDTH, ADDR_WIDTH)
                            port map 
                            (
                            w_ADDRs(i),
                            i_CLK,
                            i_DATA,
                            w_WRITE_ENA(i),
                            w_BLOCK_OUT(i)
                            );
            end generate GEN_BLOCK;
            
            
            -- dados de saida
            o_DATA_ROW_0 <= w_BLOCK_OUT(0);
            o_DATA_ROW_1 <= w_BLOCK_OUT(1);
            o_DATA_ROW_2 <= w_BLOCK_OUT(2);
        
    end arc;