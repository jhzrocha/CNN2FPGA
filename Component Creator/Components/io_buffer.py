from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class IOBuffer(ComponentCommonMethods):

#    Não testado no modelsim
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = f"Relu"
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
            -- atribui 0 aos numeros negativos, identificados pelo oitavo bit em 1
            o_PIX <= i_PIX; -- "00000000" when (i_PIX(DATA_WIDTH - 1) = '1') else i_PIX;
        """
        self.OutputEntityAndArchitectureFile()
