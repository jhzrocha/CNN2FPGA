-- testbench do nucleo convolucional
-- Inicialmente sao necssarios 3 ciclos de clock para que o resultado seja
-- valido. Apos esses 3 ciclos de clock, um novo resultado e gerado.

library ieee;
use ieee.std_logic_1164.all;
use ieee.STD_LOGIC_UNSIGNED.all;

entity nucleo_convolucional_tb is
end nucleo_convolucional_tb;

architecture arch of nucleo_convolucional_tb is
	-- LARGURA DOS DADOS
	constant i_DATA_WIDTH : integer := 8;
	constant w_CONV_OUT : integer := 16;
	constant o_DATA_WIDTH : integer := 32;

  constant c_CLK_PERIOD : time := 2 ns;

  -- Component
  component nucleo_convolucional is
    generic (
      i_DATA_WIDTH : integer := 8;
      w_CONV_OUT : integer := 16;
      o_DATA_WIDTH : integer := 32);
    port (
      i_CLK       : in STD_LOGIC;
    	i_CLR       : in STD_LOGIC;
    
    	-- habilita deslocamento dos registradores
    	i_PIX_SHIFT_ENA : in STD_LOGIC;
   	 	i_PES_SHIFT_ENA : in STD_LOGIC;    

    	-- linhas de pixels
    	i_PIX_ROW_1 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
    	i_PIX_ROW_2 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
    	i_PIX_ROW_3 : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);  
    
    	-- habilita escrita em uma das linhas de pesos
    	i_PES_ROW_SEL : in std_logic_vector (1 downto 0);
    
    	-- peso de entrada
    	i_PES : in STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
    
    	-- pixel de saida
    	o_PIX       : out STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)

    );
  end component;
	
	-- clock e clear
	signal w_CLK, w_CLR : STD_LOGIC;

	-- enable para os registradores de deslocamento
	signal w_PIX_SHIFT_ENA, w_PES_SHIFT_ENA : STD_LOGIC;

  -- pixels e pesos de entrada
	signal w_PIX_ROW_1, w_PIX_ROW_2, w_PIX_ROW_3 : STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);
	signal w_PES : STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0);  
  signal w_PES_ROW_SEL : std_logic_vector (1 downto 0);

	-- pixel de saida
	signal w_OUT_PIX : STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0);  

begin
  u_DUT : work.nucleo_convolucional
  generic map(i_DATA_WIDTH, w_CONV_OUT, o_DATA_WIDTH)
  port map(
    i_CLK           => w_CLK,
    i_CLR           => w_CLR,
    -- habilita deslocamento dos registradores
    i_PIX_SHIFT_ENA => w_PIX_SHIFT_ENA,
    i_PES_SHIFT_ENA => w_PES_SHIFT_ENA,
    -- linhas de pixels
    i_PIX_ROW_1     => w_PIX_ROW_1,
    i_PIX_ROW_2     => w_PIX_ROW_2,
    i_PIX_ROW_3     => w_PIX_ROW_3,
    -- linhas de pesos
    i_PES     			=> w_PES,
		i_PES_ROW_SEL   => w_PES_ROW_SEL,
    -- pixel de saida
    o_PIX           => w_OUT_PIX
  );

  ---------------------
  p_CLK : process
  begin
    w_CLK <= '1';
    wait for c_CLK_PERIOD/2;
    w_CLK <= '0';
    wait for c_CLK_PERIOD/2;
  end process p_CLK;
  ---------------------

	p_TEST : process
	begin
	  --------------------------
		w_CLR <= '1'; -- clear 
    wait for 2 * c_CLK_PERIOD;
		w_CLR <= '0'; -- clear 
		---------------------------
		
		-- habilita deslocamento
		w_PIX_SHIFT_ENA <= '1';
		w_PES_SHIFT_ENA <= '1';
		
		-- PRIMEIRA COLUNA DE VALORES
		w_PIX_ROW_1 <= "00000001";
		w_PIX_ROW_2 <= "00000001";
		w_PIX_ROW_3 <= "00000001";

		w_PES_ROW_1 <= "00000001";
		w_PES_ROW_2 <= "00000010";
		w_PES_ROW_3 <= "00000001";
		
		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;
		
		-- SEGUNDA COLUNA DE CAVALORES		
		w_PIX_ROW_1 <= "10000000";
		w_PIX_ROW_2 <= "10000000";
		w_PIX_ROW_3 <= "10000000";

		w_PES_ROW_1 <= "00000000";
		w_PES_ROW_2 <= "00000000";
		w_PES_ROW_3 <= "00000000";

		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;
		
		-- TERVEIRA COLUNA DE VALORES
		w_PIX_ROW_1 <= "00000000";
		w_PIX_ROW_2 <= "00000000";
		w_PIX_ROW_3 <= "00000000";

		w_PES_ROW_1 <= "10000000";
		w_PES_ROW_2 <= "10000000";
		w_PES_ROW_3 <= "10000000";

		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;


		-- QUARTA COLUNA DE VALORES
		w_PIX_ROW_1 <= "10000000";
		w_PIX_ROW_2 <= "10000000";
		w_PIX_ROW_3 <= "10000000";

		w_PES_ROW_1 <= "10000000";
		w_PES_ROW_2 <= "10000000";
		w_PES_ROW_3 <= "10000000";

		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;
	
		-- Quinta COLUNA DE VALORES
		w_PIX_ROW_1 <= "10000000";
		w_PIX_ROW_2 <= "10000000";
		w_PIX_ROW_3 <= "10000000";

		w_PES_ROW_1 <= "01000000";
		w_PES_ROW_2 <= "01000000";
		w_PES_ROW_3 <= "01000000";

		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;


		-- SEXTA COLUNA DE VALORES
		w_PIX_ROW_1 <= "11111111";
		w_PIX_ROW_2 <= "11111111";
		w_PIX_ROW_3 <= "11111111";

		w_PES_ROW_1 <= "00000010";
		w_PES_ROW_2 <= "11111111";
		w_PES_ROW_3 <= "11111111";

		-- espera um ciclo de clock
		wait for c_CLK_PERIOD;


		-- SETIMA COLUNA DE VALORES
		w_PIX_ROW_1 <= "00000010";
		w_PIX_ROW_2 <= "00000010";
		w_PIX_ROW_3 <= "00000010";

		w_PES_ROW_1 <= "00000010";
		w_PES_ROW_2 <= "00000010";
		w_PES_ROW_3 <= "00000010";

		-- espera um ciclo de clock
		wait for 3*c_CLK_PERIOD;
		
		assert (w_OUT_PIX = "00100100") report "valor incorreto." severity error;

    -- TEST DONE
    assert false report "Test done." severity note;
    wait;

	end process p_TEST;
	


end arch;
