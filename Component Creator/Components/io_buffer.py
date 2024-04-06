from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class IOBuffer(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = 'IOBuffer'
        self.portMap =   { 'in': [
                                    Port(name='i_CLK',dataType=f"std_logic"),
                                    Port(name='i_CLR',dataType=f"std_logic"),
                                    Port(name='i_DATA',dataType=f"std_logic_vector (DATA_WIDTH - 1 downto 0)"),
                                    Port(name='i_READ_ENA',dataType=f"std_logic"),
                                    Port(name='i_WRITE_ENA',dataType=f"std_logic"),
                                    Port(name='i_SEL_LINE',dataType=f"std_logic_vector (1 downto 0)"),
                                    Port(name='i_READ_ADDR0',dataType=f"std_logic_vector (ADDR_WIDTH - 1 downto 0)", initialValue="(others => '0')"),
                                    Port(name='i_READ_ADDR1',dataType=f"std_logic_vector (ADDR_WIDTH - 1 downto 0)",initialValue="(others => '0')"),
                                    Port(name='i_READ_ADDR2',dataType=f"std_logic_vector (ADDR_WIDTH - 1 downto 0)",initialValue="(others => '0')"),
                                    Port(name='i_WRITE_ADDR',dataType=f"std_logic_vector (ADDR_WIDTH - 1 downto 0)",initialValue="(others => '0')")
                                ],
                            'out': [ Port(name='o_DATA_ROW_0',dataType=f"std_logic_vector (DATA_WIDTH - 1 downto 0)"),
                                     Port(name='o_DATA_ROW_1',dataType=f"std_logic_vector (DATA_WIDTH - 1 downto 0)"),
                                     Port(name='o_DATA_ROW_2',dataType=f"std_logic_vector (DATA_WIDTH - 1 downto 0)")
                                   
                                   ]
                    }
        self.addGenericByParameters(name='NUM_BLOCKS',dataType='integer',initialValue=3)
        self.addGenericByParameters(name='DATA_WIDTH',dataType='integer',initialValue=8)
        self.addGenericByParameters(name='ADDR_WIDTH',dataType='integer',initialValue=10)
        self.addArrayTypeOnArchitecture(name='t_BLOCKS_DATA',type='STD_LOGIC_VECTOR(DATA_WIDTH - 1 downto 0)',size=3)
        self.addArrayTypeOnArchitecture(name='t_BLOCKS_ADDR',type='STD_LOGIC_VECTOR(ADDR_WIDTH - 1 downto 0)',size=3)
        self.addInternalSignalWire(name='w_ADDRs',dataType='t_BLOCKS_ADDR',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_BLOCK_OUT',dataType='t_BLOCKS_DATA',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_WRITE_ENA',dataType='STD_LOGIC_VECTOR(2 downto 0)',initialValue="(others => '0')")
        self.internalOperations = f"""            
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
        """
        self.OutputEntityAndArchitectureFile()
