from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.counter import Counter

#Compilado

class ConvCrt(ComponentCommonMethods):

    # ADDR_WIDTH - addWidth
    # NC_ADDRESS_WIDTH - ncAddrWidth
    # NC_SEL_WIDTH -   ncSelWidth
    # OUT_SEL_WIDTH - outSelWidthBuffers
    # W - ifMapWidth
    #WEIGHT_ADDRESS_WIDTH - lengthWeightAddress
    #BIAS_ADDRESS_WIDTH - lengthBiasAddress
    #OUT_SEL_WIDTH - outSelWidthBuffers
    #NUM_WEIGHT_FILTER_CHA - qtFiltersPerChannel R*S filter Height * filter Width

    #LAST_WEIGHT - qtWeights
    #LAST_BIAS - qtBias
    #LAST_ROW - qtRows
    #LAST_COL - qtCols

    #C - qtChannels
    #M - qtFilters

    def __init__(self,addWidth=10,ncAddrWidth=2,ncSelWidth=2, ifMapWidth=26, lengthWeightAddress=8, lengthBiasAddress=5, outSelWidthBuffers=3, qtFiltersPerChannel='"1000"', qtWeights='"11011"', qtBias='"10"', qtRows='"100010"', qtCols='"11010"', qtChannels=3, qtFilters=6):
        self.addWidth=addWidth
        self.ncAddrWidth=ncAddrWidth
        self.ncSelWidth=ncSelWidth
        self.ifMapWidth = ifMapWidth
        self.lengthWeightAddress = lengthWeightAddress
        self.lengthBiasAddress = lengthBiasAddress
        self.outSelWidthBuffers = outSelWidthBuffers
        self.qtFiltersPerChannel = qtFiltersPerChannel
        self.qtWeights = qtWeights
        self.qtBias = qtBias
        self.qtRows = qtRows
        self.qtCols = qtCols
        self.qtChannels = qtChannels
        self.qtFilters = qtFilters
        
        self.createComponent()



    def createComponent(self):
        self.startInstance()
        self.minimalComponentFileName = f'conv1_crt_{self.addWidth}dw_{self.ncAddrWidth}ncaw_{self.ncSelWidth}ncsw_{self.ifMapWidth}ifmw_{self.lengthWeightAddress}lwaw_{self.lengthBiasAddress}lbaw_{self.outSelWidthBuffers}oswb_{self.qtFiltersPerChannel}qfpc_{self.qtWeights}qw_{self.qtBias}qb_{self.qtRows}qr_{self.qtCols}qc_{self.qtChannels}qc_{self.qtFilters}qf'.replace('"','')
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic')
                                ],
                'out': [
                                    Port(name='o_READY',dataType=f"std_logic"),
                                    Port(name='o_IN_READ_ENA',dataType=f"std_logic",initialValue="'0'"),
                                    Port(name='o_IN_READ_ADDR_0',dataType=f"std_logic_vector ({self.addWidth-1} downto 0)"),
                                    Port(name='o_IN_READ_ADDR_1',dataType=f"std_logic_vector ({self.addWidth-1} downto 0)"),
                                    Port(name='o_IN_READ_ADDR_2',dataType=f"std_logic_vector ({self.addWidth-1} downto 0)"),
                                    Port(name='o_WEIGHT_READ_ENA',dataType=f"std_logic"),
                                    Port(name='o_WEIGHT_READ_ADDR',dataType=f"std_logic_vector({self.lengthWeightAddress-1} downto 0)"),
                                    Port(name='o_BIAS_READ_ENA',dataType=f"std_logic"),
                                    Port(name='o_BIAS_READ_ADDR',dataType=f"std_logic_vector({self.lengthBiasAddress-1} downto 0)"),
                                    Port(name='o_BIAS_WRITE_ENA',dataType=f"std_logic"),
                                    Port(name='o_SCALE_WRITE_ENA',dataType=f"std_logic"),
                                    Port(name='o_PIX_SHIFT_ENA',dataType=f"std_logic"),
                                    Port(name='o_WEIGHT_SHIFT_ENA',dataType=f"std_logic"),
                                    Port(name='o_NC_ADDR',dataType=f"std_logic_vector({self.ncAddrWidth-1} downto 0)"),
                                    Port(name='o_WEIGHT_ROW_SEL',dataType=f"std_logic_vector(1 downto 0)"),
                                    Port(name='o_NC_O_SEL',dataType=f"std_logic_vector({self.ncSelWidth-1} downto 0)"),
                                    Port(name='o_ACC_ENA',dataType=f"std_logic"),
                                    Port(name='o_ACC_RST',dataType=f"std_logic"),
                                    Port(name='o_ROW_SEL',dataType=f"std_logic_vector(1 downto 0)"),
                                    Port(name='o_OUT_SEL',dataType=f"std_logic_vector({self.outSelWidthBuffers-1} downto 0)", initialValue="(others => '0')"),
                                    Port(name='o_OUT_WRITE_ENA',dataType=f"std_logic"),
                                    Port(name='o_OUT_INC_ADDR',dataType=f"std_logic"),
                                    Port(name='o_OUT_CLR_ADDR',dataType=f"std_logic")
                                   ] 
                        }
        self.addStateTypeOnArchitecture('t_STATE',['s_IDLE',
                                        's_WEIGHT_VERIFY_ADDR',
                                        's_WEIGHT_READ_ENA',
                                        's_WEIGHT_WRITE_ENA',
                                        's_WEIGHT_INC_ADDR',
                                        's_BIAS_VERIFY_ADDR',
                                        's_BIAS_READ_ENA',
                                        's_BIAS_WRITE_ENA',
                                        's_BIAS_INC_ADDR',
                                        's_LOAD_PIX',
                                        's_REG_PIX',
                                        's_REG_OUT_NC',  
                                        's_ACC_FIL_CH',  
                                        's_WRITE_OUT',   
                                        's_RIGHT_SHIFT',
                                        's_LAST_COL',    
                                        's_DOWN_SHIFT',  
                                        's_LAST_ROW',
                                        's_INC_SEL_OUT', 
                                        's_LAST_OBUFF',  
                                        's_END' ])
        self.addInternalSignalWire(name='r_STATE',dataType='t_STATE')
        self.addInternalSignalWire(name='w_NEXT',dataType='t_STATE')

        self.internalOperations = f"""
        
        p_STATE : process (i_CLK, i_CLR)
        begin
            if (i_CLR = '1') then
            r_STATE <= s_IDLE; --initial state
            elsif (rising_edge(i_CLK)) then
            r_STATE <= w_NEXT; --next state
            end if;
        end process;
        p_NEXT : process (r_STATE, i_GO, r_WEIGHT_CNTR, r_BIAS_CNTR, r_OUT_SEL, r_CNT_REG_PIX, r_NC_O_SEL, w_END_COL, w_END_ROW)
        begin
            case (r_STATE) is
            when s_IDLE => -- aguarda sinal go                 
                if (i_GO = '1') then
                w_NEXT <= s_WEIGHT_READ_ENA;
                else
                w_NEXT <= s_IDLE;
                end if;

            when s_WEIGHT_READ_ENA => -- habilita leitura de pesos
                w_NEXT <= s_WEIGHT_WRITE_ENA;

            when s_WEIGHT_WRITE_ENA => -- habilita escrita de pesos
                w_NEXT <= s_WEIGHT_INC_ADDR;

            when s_WEIGHT_INC_ADDR => -- incrementa contador pesos
                w_NEXT <= s_WEIGHT_VERIFY_ADDR;

            when s_WEIGHT_VERIFY_ADDR => -- verifica endereco de pesos
                if (r_WEIGHT_CNTR < {self.qtWeights}) then
                w_NEXT <= s_WEIGHT_READ_ENA;
                else
                w_NEXT <= s_BIAS_READ_ENA;
                end if;

            when s_BIAS_READ_ENA => -- havilita leitura de BIAS
                w_NEXT <= s_BIAS_WRITE_ENA;

            when s_BIAS_WRITE_ENA => -- havilita escrita de BIAS
                w_NEXT <= s_BIAS_INC_ADDR;

            when s_BIAS_INC_ADDR => -- incrementa contgador BIAS
                w_NEXT <= s_BIAS_VERIFY_ADDR;

            when s_BIAS_VERIFY_ADDR => -- verifica endereco de BIAS
                if (r_BIAS_CNTR < {self.qtBias}) then
                w_NEXT <= s_BIAS_READ_ENA;
                else
                w_NEXT <= s_LOAD_PIX;
                end if;
            when s_LOAD_PIX => -- habilita leitura pixel de entrada
                w_NEXT <= s_REG_PIX;

            when s_REG_PIX => -- registra pixel de entrada
                if (r_CNT_REG_PIX = "11") then
                w_NEXT <= s_REG_OUT_NC;
                else
                w_NEXT <= s_LOAD_PIX;
                end if;

            when s_REG_OUT_NC => -- registra saida
                w_NEXT <= s_ACC_FIL_CH;

            when s_ACC_FIL_CH =>            -- acumula canais de um filtro
                if (r_NC_O_SEL = std_logic_vector(to_unsigned({self.qtChannels}, {self.ncSelWidth-1}))) then -- enquanto < C
                w_NEXT <= s_WRITE_OUT;
                else
                w_NEXT <= s_ACC_FIL_CH;
                end if;

            when s_WRITE_OUT => -- salva no bloco de saida
                w_NEXT <= s_RIGHT_SHIFT;

            when s_RIGHT_SHIFT => -- deslocamento à direita
                w_NEXT <= s_LAST_COL;

            when s_LAST_COL => -- verifica fim colunas
                if (w_END_COL = '1') then
                w_NEXT <= s_DOWN_SHIFT;
                else
                w_NEXT <= s_REG_OUT_NC;
                end if;

            when s_DOWN_SHIFT => -- deslocamento à baixo
                w_NEXT <= s_LAST_ROW;

            when s_LAST_ROW => -- verifica fim linhas
                if (w_END_ROW = '1') then
                w_NEXT <= s_INC_SEL_OUT;
                else
                w_NEXT <= s_LOAD_PIX;
                end if;

            when s_INC_SEL_OUT => -- incrementa selecionador de buffer
                w_NEXT <= s_LAST_OBUFF;

            when s_LAST_OBUFF => -- verificar se selecionador atingiu valor max
                if (r_OUT_SEL = std_logic_vector(to_unsigned({self.qtFilters}, {self.outSelWidthBuffers}))) then
                w_NEXT <= s_END;
                else
                w_NEXT <= s_WEIGHT_VERIFY_ADDR;
                end if;

            when s_END => -- fim
                w_NEXT <= s_IDLE;

            when others =>
                w_NEXT <= s_IDLE;

            end case;
        end process;

        -----------------------------------------------------------------------
        -- sinais para buffers de entrada
        ---------------------------------  
        w_INC_IN_ADDR <= '1' when (r_STATE = s_LOAD_PIX or r_STATE = s_RIGHT_SHIFT) else '0';
        w_RST_IN_ADDR <= '1' when (i_CLR = '1' or w_END_COL = '1') else '0';
        
        w_INC_IN_ADDR_0 <= '1' when (r_ROW_SEL = "00" and r_STATE = s_DOWN_SHIFT) else '0';
        w_INC_IN_ADDR_1 <= '1' when (r_ROW_SEL = "01" and r_STATE = s_DOWN_SHIFT) else '0';
        w_INC_IN_ADDR_2 <= '1' when (r_ROW_SEL = "10" and r_STATE = s_DOWN_SHIFT) else '0';

        w_RST_IN_ADDR_0 <= '1' when (r_STATE = s_INC_SEL_OUT or i_CLR = '1') else '0';
        w_RST_IN_ADDR_1 <= w_RST_IN_ADDR_0;
        w_RST_IN_ADDR_2 <= w_RST_IN_ADDR_0;

          o_IN_READ_ENA <= '1' when (r_STATE = s_LOAD_PIX or r_STATE = s_RIGHT_SHIFT) else '0';
        o_IN_READ_ADDR_0 <= w_IN_READ_ADDR and r_ADDR_0_OFF;
        o_IN_READ_ADDR_1 <= w_IN_READ_ADDR and r_ADDR_1_OFF;
        o_IN_READ_ADDR_2 <= w_IN_READ_ADDR and r_ADDR_2_OFF;
        -----------------------------------------------------------------------    
        ---------------------------------
        -- sinais para nucleos convolucionais
        ---------------------------------    
        -- seleciona configuração de conexao entre buffer e registradores de deslocamento
        W_ROW_SEL_RST <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_ROW_SEL = "11" or r_STATE = s_INC_SEL_OUT) else '0';
        W_ROW_SEL_INC <= '1' when (r_STATE = s_DOWN_SHIFT) else '0';

        o_ROW_SEL <= r_ROW_SEL;

        -- habilita sinal para incrementar contador de deslocamento dos 3 pixels iniciais
        w_INC_CNT_REG_PIX <= '1' when (r_STATE = s_LOAD_PIX) else '0';
        W_CNT_REG_PIX_RST <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_STATE = s_REG_OUT_NC) else '0';

        o_PIX_SHIFT_ENA <= '1' when (r_STATE = s_REG_PIX or r_STATE = s_RIGHT_SHIFT) else '0';
        ---------------------------------

        -- seleciona saida de NCs  
        w_NC_O_SEL_INC <= '1' when (r_STATE = s_ACC_FIL_CH) else '0';
        w_NC_O_SEL_RST <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_STATE = s_RIGHT_SHIFT) else '0';

        o_NC_O_SEL <= r_NC_O_SEL;

        -- habilita acumulador de pixels de saida dos NCs
        o_ACC_ENA <= w_NC_O_SEL_INC;
        -- reseta acumulador de pixels de saida dos NCs
        o_ACC_RST <= w_NC_O_SEL_RST;
        ---------------------------------

        ---------------------------------
        -- sinais para buffers de saida
        ---------------------------------    
        -- habilita escrita buffer de saida
        o_OUT_WRITE_ENA <= '1' when (r_STATE = s_WRITE_OUT) else '0';
        -- incrementa endereco de saida
        o_OUT_INC_ADDR <= '1' when (r_STATE = s_WRITE_OUT) else '0';
        -- reset endreco de saida
        o_OUT_CLR_ADDR <= '1' when (r_STATE = s_IDLE or r_STATE = s_INC_SEL_OUT) else '0';
        ---------------------------------
        ---------------------------------
        -- Sinais para deslocamento a direita
        ---------------------------------
        -- contador de colunas
        -- default 3 colunas pois inicia a contagem a partir das 3 primeiras colunas
        w_INC_COL_CNT <= '1' when (r_STATE = s_RIGHT_SHIFT) else '0';
        w_RST_COL_CNT <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_STATE = s_DOWN_SHIFT or r_STATE = s_INC_SEL_OUT) else '0';

        -- fim coluna quando contador = numero de coluna 
        w_END_COL <= '1' when (r_CNT_COL = {self.qtCols}) else '0';
        ---------------------------------

        ---------------------------------
        -- Sinais para deslocamento a baixo
        ---------------------------------
        -- contador de linhas
        -- default 3 linhas pois inicia a contagem a partir das 3 primeiras linhas 
        w_INC_ROW_CNT <= '1' when (r_STATE = s_DOWN_SHIFT) else '0';
        w_RST_ROW_CNT <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_STATE = s_INC_SEL_OUT) else '0';    
        -- fim linha quando contador = numero de linha 
        w_END_ROW <= '1' when (r_CNT_ROW = {self.qtRows}) else '0';
        ---------------------------------
        ---------------------------------

        -- enderecamento dos pesos
        w_RST_WEIGHT_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else '0';
        w_INC_WEIGHT_ADDR <= '1' when (r_STATE = s_WEIGHT_INC_ADDR) else '0';
        
          w_RST_WEIGHT_CNTR <= '1' when (r_STATE = s_BIAS_VERIFY_ADDR) else '0';

        w_RST_BIAS_ADDR <= '1' when (i_CLR = '1' or r_STATE = s_IDLE) else '0';
        w_INC_BIAS_ADDR <= '1' when (r_BIAS_CNTR = "10" and r_STATE = s_LOAD_PIX) else '0';

        w_RST_BIAS_CNTR <= '1' when (r_STATE = s_LOAD_PIX) else '0';
        w_INC_BIAS_CNTR <= '1' when (r_STATE = s_BIAS_INC_ADDR) else '0';

        w_RST_NUM_WEIGHT <= '1' when ((r_STATE = s_WEIGHT_VERIFY_ADDR and r_NUM_WEIGHT_FILTER > {self.qtFiltersPerChannel}) or i_CLR = '1' or r_STATE = s_IDLE) else '0';
        w_INC_NUM_WEIGHT <= '1' when (r_STATE = s_WEIGHT_INC_ADDR) else '0';


        w_RST_NC_ADDRESS <= '1' when (i_CLR = '1' or r_STATE = s_IDLE or r_STATE = s_INC_SEL_OUT) else '0';
        w_INC_NC_ADDRESS <= '1' when (r_NUM_WEIGHT_FILTER = {self.qtFiltersPerChannel} and r_STATE = s_WEIGHT_INC_ADDR) else '0';

        w_RST_WEIGHT_COL_CNTR <= '1' when (i_CLR = '1' or (r_STATE = s_WEIGHT_VERIFY_ADDR and r_WEIGHT_COL_CNTR = "11")) else '0';
        w_INC_WEIGHT_COL_CNTR <= '1' when (r_STATE = s_WEIGHT_INC_ADDR) else '0';

        w_RST_WEIGHT_ROW_CNTR <= '1' when ((i_CLR = '1' or r_STATE = s_IDLE) or (r_STATE = s_WEIGHT_VERIFY_ADDR and r_WEIGHT_ROW_CNTR = "11")) else '0';
        w_INC_WEIGHT_ROW_CNTR <= '1' when (r_WEIGHT_COL_CNTR = "10" and r_STATE = s_WEIGHT_INC_ADDR) else '0';

        w_RST_OUT_SEL <= '1' when (r_STATE = s_IDLE) else '0';
        w_INC_OUT_SEL <= '1' when (r_STATE = s_INC_SEL_OUT) else '0';

        o_OUT_SEL <= r_OUT_SEL;

        -- sinal para rom de pesos
        o_WEIGHT_READ_ENA <= '1' when (r_STATE = s_WEIGHT_READ_ENA) else '0';
        o_WEIGHT_READ_ADDR <= r_WEIGHT_ADDR;
        -- SINAL PARA ROM DE BIAS E SCALES
        o_BIAS_READ_ENA <= '1' when (r_STATE = s_BIAS_READ_ENA) else '0';
        -- offset para scale
        o_BIAS_READ_ADDR <= r_BIAS_ADDR when (r_BIAS_CNTR = "00") else std_logic_vector(unsigned(r_BIAS_ADDR) + to_unsigned({self.qtFilters}, {self.lengthBiasAddress}));

        -- habilita escrita nos registradores de bias e scale
        o_BIAS_WRITE_ENA <= '1' when (r_STATE = s_BIAS_WRITE_ENA and r_BIAS_CNTR = "00") else '0';
        o_SCALE_WRITE_ENA <= '1' when (r_STATE = s_BIAS_WRITE_ENA and r_BIAS_CNTR = "01") else '0';

        -- endereco do NC para carregar pesos     
        o_NC_ADDR <= r_NC_ADDR;

        -- seleciona linha dos registradores de deslocamento
        o_WEIGHT_ROW_SEL <= r_WEIGHT_ROW_CNTR;

        -- habilita shift dos pesos 
        o_WEIGHT_SHIFT_ENA <= '1' when (r_STATE = s_WEIGHT_WRITE_ENA) else '0';

        -- sinaliza fim maq estado
        o_READY <= '1' when (r_STATE = s_END) else '0';
        """
        self.addInternalSignalWire(name='w_IN_READ_ADDR',dataType=f'std_logic_vector ({self.addWidth-1} downto 0)')
        self.addInternalSignalWire(name=f'w_INC_IN_ADDR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_IN_ADDR',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_ADDR_0_OFF',dataType=f'std_logic_vector ({self.addWidth-1} downto 0)')
        self.addInternalSignalWire(name=f' w_INC_IN_ADDR_0',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_IN_ADDR_0',dataType=f'std_logic')
        
      
        self.addInternalSignalWire(name=f'r_ADDR_1_OFF',dataType=f'std_logic_vector ({self.addWidth-1} downto 0)')
        self.addInternalSignalWire(name=f' w_INC_IN_ADDR_1',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_IN_ADDR_1',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_ADDR_2_OFF',dataType=f'std_logic_vector ({self.addWidth-1} downto 0)')
        self.addInternalSignalWire(name=f' w_INC_IN_ADDR_2',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_IN_ADDR_2',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_CNT_REG_PIX',dataType=f'std_logic_vector (1 downto 0)', initialValue="(others => '0')")
        self.addInternalSignalWire(name=f'w_INC_CNT_REG_PIX',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'W_CNT_REG_PIX_RST',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_NC_O_SEL',dataType=f'std_logic_vector({self.ncSelWidth-1} downto 0)', initialValue=f"(others => '0')")
        self.addInternalSignalWire(name=f'w_NC_O_SEL_INC',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_NC_O_SEL_RST',dataType=f'std_logic')
        
        self.addInternalSignalWire(name=f'r_ROW_SEL',dataType=f'std_logic_vector(1 downto 0)')
        self.addInternalSignalWire(name=f'W_ROW_SEL_RST',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'W_ROW_SEL_INC',dataType=f'std_logic')


        self.addInternalSignalWire(name=f'r_CNT_COL',dataType=f'std_logic_vector(4 downto 0)', initialValue=f'"00010"')
        self.addInternalSignalWire(name=f'w_INC_COL_CNT',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_COL_CNT',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_END_COL',dataType=f'std_logic')
        
        self.addInternalSignalWire(name=f'r_CNT_ROW',dataType=f'std_logic_vector(5 downto 0)', initialValue='"000010"')
        self.addInternalSignalWire(name=f'w_INC_ROW_CNT',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_ROW_CNT',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_END_ROW',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_WEIGHT_ADDR',dataType=f'std_logic_vector({self.lengthWeightAddress-1} downto 0)')
        self.addInternalSignalWire(name=f'r_WEIGHT_CNTR',dataType=f'std_logic_vector({self.lengthWeightAddress-1} downto 0)')
        self.addInternalSignalWire(name=f'w_RST_WEIGHT_ADDR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_WEIGHT_ADDR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_WEIGHT_CNTR',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_NUM_WEIGHT_FILTER',dataType=f'std_logic_vector(4 downto 0)')
        self.addInternalSignalWire(name=f'w_RST_NUM_WEIGHT',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_NUM_WEIGHT',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_WEIGHT_ROW_CNTR',dataType=f'std_logic_vector(1 downto 0)')
        self.addInternalSignalWire(name=f'r_WEIGHT_COL_CNTR',dataType=f'std_logic_vector(1 downto 0)')
        self.addInternalSignalWire(name=f'w_RST_WEIGHT_COL_CNTR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_WEIGHT_COL_CNTR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_WEIGHT_ROW_CNTR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_WEIGHT_ROW_CNTR',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_BIAS_ADDR',dataType=f'std_logic_vector({self.lengthBiasAddress-1} downto 0)')
        self.addInternalSignalWire(name=f'r_BIAS_CNTR',dataType=f'std_logic_vector({self.lengthBiasAddress-1} downto 0)')
        self.addInternalSignalWire(name=f'w_RST_BIAS_ADDR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_BIAS_ADDR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_RST_BIAS_CNTR',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_BIAS_CNTR',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_NC_ADDR',dataType=f'std_logic_vector({self.ncAddrWidth-1} downto 0)', initialValue=f"(others => '0')")
        self.addInternalSignalWire(name=f'w_RST_NC_ADDRESS',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_NC_ADDRESS',dataType=f'std_logic')

        self.addInternalSignalWire(name=f'r_OUT_SEL',dataType=f'std_logic_vector({self.outSelWidthBuffers-1} downto 0)', initialValue="(others => '0')")
        self.addInternalSignalWire(name=f'w_RST_OUT_SEL',dataType=f'std_logic')
        self.addInternalSignalWire(name=f'w_INC_OUT_SEL',dataType=f'std_logic')


        self.addInternalComponent(component = Counter(dataWidth=self.addWidth,
                                                      bitStep=1),
                                  componentCallName='u_INPUT_ADDR',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_IN_ADDR',
                                  'i_INC':'w_INC_IN_ADDR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'w_IN_READ_ADDR'}                                              
                                  )
        
        self.addInternalComponent(component = Counter(dataWidth=self.addWidth,
                                                      bitStep=self.ifMapWidth),
                                  componentCallName='u_ADDR0_OFFSET',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_IN_ADDR_0',
                                  'i_INC':'w_INC_IN_ADDR_0',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_ADDR_0_OFF'}                                              
                                  )
        self.addInternalComponent(component = Counter(dataWidth=self.addWidth,
                                                      bitStep=self.ifMapWidth),
                                  componentCallName='u_ADDR1_OFFSET',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_IN_ADDR_1',
                                  'i_INC':'w_INC_IN_ADDR_1',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_ADDR_1_OFF'}                                              
                                  )
        
        self.addInternalComponent(component = Counter(dataWidth=self.addWidth,
                                                      bitStep=self.ifMapWidth),
                                  componentCallName='u_ADDR2_OFFSET',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_IN_ADDR_2',
                                  'i_INC':'w_INC_IN_ADDR_2',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_ADDR_2_OFF'}                                              
                                  )
        
        self.addInternalComponent(component = Counter(dataWidth=2,
                                                      bitStep=1),
                                  componentCallName='u_ROW_SEL',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'W_ROW_SEL_RST',
                                  'i_INC':'W_ROW_SEL_INC',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_ROW_SEL'}                                              
                                  )
        self.addInternalComponent(component = Counter(dataWidth=2,
                                                      bitStep=1),
                                  componentCallName='u_CNT_REG_PIX',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'W_CNT_REG_PIX_RST',
                                  'i_INC':'w_INC_CNT_REG_PIX',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_CNT_REG_PIX'}                                              
                                  )
        
        self.addInternalComponent(component = Counter(dataWidth=self.ncSelWidth,
                                                      bitStep=1),
                                  componentCallName='u_NC_O_SEL',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_NC_O_SEL_RST',
                                  'i_INC':'w_NC_O_SEL_INC',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_NC_O_SEL'}                                              
                                  )
        
        self.addInternalComponent(component = Counter(dataWidth=5,
                                                      bitStep=1),
                                  componentCallName='u_CNT_COL ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_COL_CNT',
                                  'i_INC':'w_INC_COL_CNT',
                                  'i_RESET_VAL':'"00010"',
                                  'o_Q':'r_CNT_COL'}
                                    )
        self.addInternalComponent(component = Counter(dataWidth=6,
                                                      bitStep=1),
                                  componentCallName='u_CNT_ROW ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_ROW_CNT',
                                  'i_INC':'w_INC_ROW_CNT',
                                  'i_RESET_VAL':'"000010"',
                                  'o_Q':'r_CNT_ROW'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=self.lengthWeightAddress,
                                                      bitStep=1),
                                  componentCallName='u_WEIGHT_ADDR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_WEIGHT_ADDR',
                                  'i_INC':'w_INC_WEIGHT_ADDR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_WEIGHT_ADDR'}
                                    )
        self.addInternalComponent(component = Counter(dataWidth=self.lengthWeightAddress,
                                                      bitStep=1),
                                  componentCallName='u_WEIGHT_CNTR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_WEIGHT_CNTR',
                                  'i_INC':'w_INC_WEIGHT_ADDR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_WEIGHT_CNTR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=self.lengthBiasAddress,
                                                      bitStep=1),
                                  componentCallName='u_BIAS_ADDR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_BIAS_ADDR',
                                  'i_INC':'w_INC_BIAS_ADDR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_BIAS_ADDR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=self.lengthBiasAddress,
                                                      bitStep=1),
                                  componentCallName='u_BIAS_CNTR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_BIAS_CNTR',
                                  'i_INC':'w_INC_BIAS_CNTR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_BIAS_CNTR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=5,
                                                      bitStep=1),
                                  componentCallName='u_WEIGHT_FILTER_CNTR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_NUM_WEIGHT',
                                  'i_INC':'w_INC_NUM_WEIGHT',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_NUM_WEIGHT_FILTER'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=self.ncAddrWidth,
                                                      bitStep=1),
                                  componentCallName='u_NC_ADDRESS ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_NC_ADDRESS',
                                  'i_INC':'w_INC_NC_ADDRESS',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_NC_ADDR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=2,
                                                      bitStep=1),
                                  componentCallName='u_WEIGHT_COL_CNTR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_WEIGHT_COL_CNTR',
                                  'i_INC':'w_INC_WEIGHT_COL_CNTR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_WEIGHT_COL_CNTR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=2,
                                                      bitStep=1),
                                  componentCallName='u_WEIGHT_ROW_CNTR ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_WEIGHT_ROW_CNTR',
                                  'i_INC':'w_INC_WEIGHT_ROW_CNTR',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_WEIGHT_ROW_CNTR'}
                                    )
        
        self.addInternalComponent(component = Counter(dataWidth=self.outSelWidthBuffers,
                                                      bitStep=1),
                                  componentCallName='u_OUT_SEL ',
                                  portmap = {'i_CLK':'i_CLK',
                                  'i_RESET':'w_RST_OUT_SEL',
                                  'i_INC':'w_INC_OUT_SEL',
                                  'i_RESET_VAL':"(others => '0')",
                                  'o_Q':'r_OUT_SEL'}
                                    )
        self.OutputEntityAndArchitectureFile()



