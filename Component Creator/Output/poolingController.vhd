library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity poolingController is
        
        port (i_CLK : in STD_LOGIC;
              i_CLR : in STD_LOGIC;
              i_GO : in STD_LOGIC;
              o_READY : out STD_LOGIC;
              o_PIX_SHIFT_ENA : out STD_LOGIC;
              o_OUT_WRITE_ENA : out std_logic;
              o_OUT_WRITE_ADDR : out std_logic_vector (9 downto 0):= (others => '0');
              o_IN_READ_ADDR_0 : out std_logic_vector (9 downto 0):= (others => '0');
              o_IN_READ_ADDR_1 : out std_logic_vector (9 downto 0):= (others => '0')
        );
    end poolingController;
                 
    architecture arc of poolingController is

        type t_STATE is (
          s_IDLE,
          s_LOAD_PIX1,
          s_REG_PIX1,
          s_LOAD_PIX2,
          s_REG_PIX2,
          s_WRITE_OUT,
          s_LAST_ROW,
          s_END
        );
        signal r_STATE : t_STATE;
        signal w_NEXT : t_STATE;
        signal w_IN_READ_ADDR : std_logic_vector (9 downto 0);
        signal w_INC_IN_ADDR : std_logic;
        signal w_RST_IN_ADDR : std_logic;
        signal w_END_ROW : std_logic;
        signal w_INC_OUT_ADDR : std_logic;


        begin 
        u_INPUT_ADDR : entity work.Counter
        generic map (
            DATA_WIDTH => 10,
            STEP => 1
        )
        port map (
            i_CLK  => i_CLK,
            i_RESET  => w_RST_IN_ADDR,
            i_INC  => w_INC_IN_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => w_IN_READ_ADDR
        );
 
        u_OUTPUT_ADDR : entity work.Counter
        generic map (
            DATA_WIDTH => 10,
            STEP => 1
        )
        port map (
            i_CLK  => i_CLK,
            i_RESET  => i_CLR,
            i_INC  => w_INC_OUT_ADDR,
            i_RESET_VAL  => (others => '0'),
            o_Q  => o_OUT_WRITE_ADDR
        );

        p_STATE : process (i_CLK, i_CLR)
        begin
            if (i_CLR = '1') then
            r_STATE <= s_IDLE;      --initial state
            elsif (rising_edge(i_CLK)) then
            r_STATE <= w_NEXT;  --next state
            end if;
        end process;
            

        p_NEXT : process (r_STATE, i_GO, w_END_ROW)
        begin
            case (r_STATE) is
            when s_IDLE => -- aguarda sinal go
                if (i_GO = '1') then
                w_NEXT <= s_LOAD_PIX1;
                else
                w_NEXT <= s_IDLE;
                end if;
            
            when s_LOAD_PIX1 => -- habilita leitura pixel de entrada
                w_NEXT <= s_REG_PIX1;
                
            when s_REG_PIX1 => -- habilita leitura pixel de entrada
                w_NEXT <= s_LOAD_PIX2;         
            
            when s_LOAD_PIX2 => -- habilita leitura pixel de entrada
                w_NEXT <= s_REG_PIX2;
                
            when s_REG_PIX2 => -- habilita leitura pixel de entrada
                w_NEXT <= s_WRITE_OUT;         

            
            when s_WRITE_OUT => -- salva no bloco de saida
                w_NEXT <= s_LAST_ROW;             
                
            when s_LAST_ROW =>  -- verifica fim linhas
                if (w_END_ROW = '1') then 
                w_NEXT <= s_END;        
                else
                w_NEXT <= s_LOAD_PIX1;
                end if;
            
            when s_END =>  -- fim
                w_NEXT <= s_IDLE;      

            when others =>
                w_NEXT <= s_IDLE;
                    
            end case;
        end process;
        
        w_INC_IN_ADDR <= '1' when (r_STATE = s_LOAD_PIX1 or r_STATE = s_LOAD_PIX2) else '0';
        w_RST_IN_ADDR <= '1' when (i_CLR = '1') else '0';     
        
        o_IN_READ_ADDR_0 <= w_IN_READ_ADDR;
        o_IN_READ_ADDR_1 <= w_IN_READ_ADDR;
        
        
        w_END_ROW <= '1' when (w_IN_READ_ADDR = "0110000000") else '0';
        
        o_PIX_SHIFT_ENA <= '1' when (r_STATE = s_REG_PIX1 or r_STATE = s_REG_PIX2) else '0';

        w_INC_OUT_ADDR <= '1' when (r_STATE = s_WRITE_OUT) else '0';
        o_OUT_WRITE_ENA <= w_INC_OUT_ADDR;

        o_READY <= '1' when (r_STATE = s_END) else '0';
 
    end arc;