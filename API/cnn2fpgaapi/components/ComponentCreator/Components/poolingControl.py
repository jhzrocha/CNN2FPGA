from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.counter import Counter

class PoolingController(ComponentCommonMethods):
    # Compilado

    def __init__(self, qtAddrs=2, dataWidth = 8, addWidth = 10, maxAddr='0110000000'):
        self.startInstance()
        self.minimalComponentFileName = f'poolingController_{qtAddrs}_{dataWidth}_{addWidth}_{maxAddr}'
        self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                  Port('i_CLR','STD_LOGIC'),
                                  Port('i_GO','STD_LOGIC')],
                           'out': [Port('o_READY','STD_LOGIC'),
                                   Port('o_PIX_SHIFT_ENA','STD_LOGIC'),
                                   Port('o_OUT_WRITE_ENA','std_logic'),
                                   Port('o_OUT_WRITE_ADDR',f'std_logic_vector ({addWidth-1} downto 0)',initialValue="(others => '0')")
                                   ] 
                         }
        
        self.addMultipleGeneratedOutputPorts(qtAddrs,f'std_logic_vector ({addWidth-1} downto 0)','o_IN_READ_ADDR')       
        self.addStateTypeOnArchitecture(name='t_STATE',
                                        states=['s_IDLE','s_LOAD_PIX1','s_REG_PIX1','s_LOAD_PIX2','s_REG_PIX2','s_WRITE_OUT','s_LAST_ROW','s_END'])
        
        
        self.addInternalComponent(component=Counter(dataWidth=addWidth,
                                                    bitStep=1),
                                  componentCallName='u_INPUT_ADDR',
                                  portmap={'i_CLK':'i_CLK',
                                           'i_RESET':'w_RST_IN_ADDR',
                                           'i_INC':'w_INC_IN_ADDR',
                                           'i_RESET_VAL':"(others => '0')",
                                           'o_Q':'w_IN_READ_ADDR'}
                                  )
        
        self.addInternalSignalWire('r_STATE','t_STATE')
        self.addInternalSignalWire('w_NEXT','t_STATE')
        self.addInternalSignalWire('w_IN_READ_ADDR',f'std_logic_vector ({addWidth-1} downto 0)')
        self.addInternalSignalWire('w_INC_IN_ADDR','std_logic')
        self.addInternalSignalWire('w_RST_IN_ADDR','std_logic')
        self.addInternalSignalWire('w_END_ROW','std_logic')
        self.addInternalSignalWire('w_INC_OUT_ADDR','std_logic')
        self.internalOperations = f"""
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
        
{self.getAddrBehavior(qtAddrs)}        
        
        w_END_ROW <= '1' when (w_IN_READ_ADDR = "{maxAddr}") else '0';
        
        o_PIX_SHIFT_ENA <= '1' when (r_STATE = s_REG_PIX1 or r_STATE = s_REG_PIX2) else '0';

        w_INC_OUT_ADDR <= '1' when (r_STATE = s_WRITE_OUT) else '0';
        o_OUT_WRITE_ENA <= w_INC_OUT_ADDR;

        o_READY <= '1' when (r_STATE = s_END) else '0';
 """

        self.addInternalComponent(component=Counter(dataWidth=addWidth,
                                                    bitStep=1),
                                  componentCallName='u_OUTPUT_ADDR',
                                  portmap={'i_CLK':'i_CLK',
                                           'i_RESET':'i_CLR',
                                           'i_INC':'w_INC_OUT_ADDR',
                                           'i_RESET_VAL':"(others => '0')",
                                           'o_Q':'o_OUT_WRITE_ADDR'}
                                 )
        self.OutputEntityAndArchitectureFile()


    def getAddrBehavior(self,qtAddrs):
        behavior = ''
        for addr in range(qtAddrs):
            behavior = behavior + f'        o_IN_READ_ADDR_{addr} <= w_IN_READ_ADDR;\n'
        return behavior