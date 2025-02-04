from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.oneHotEncoder import OneHotEncoder
from ComponentBases.type import Type


#Compilado
class Registers(ComponentCommonMethods):#Banco de Registradores
    #BHEIGHT     bheight
    #BWIDTH      bwidth
    #WADDR_WIDTH waddWidth
    #RADDR_WIDTH raddWidth
    #DATA_WIDTH  dataWidth
    def __init__(self, bheight=128, bwidth=35, waddWidth=13, raddWidth=13, dataWidth=8):
        self.bheight = bheight
        self.bwidth = bwidth
        self.waddWidth = waddWidth
        self.raddWidth = raddWidth
        self.dataWidth = dataWidth
        self.createComponent()
   

    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'Registers_{self.bheight}_{self.bwidth}_{self.waddWidth}_{self.raddWidth}_{self.dataWidth}'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_DATA',f'std_logic_vector ({self.dataWidth-1} downto 0)'),
                                Port('i_WRITE_ENA','std_logic'),
                                Port('i_WRITE_ADDR',f'std_logic_vector ({self.waddWidth-1} downto 0)', initialValue="(others => '0')"),
                                Port('i_READ_ADDR',f'std_logic_vector ({self.raddWidth-1} downto 0)', initialValue="(others => '0')")
                                ],
                            'out': [
                                    Port(name='o_DATA',dataType=f"array (0 to {self.bwidth-1}) of std_logic_vector(7 downto 0)", initialValue="(others => (others => '0'))")
                                   ] 
                    }

        self.addInternalSignalWire(name='w_BLOCK_OUT',
                                   dataType=self.getPortDataType('o_DATA'),
                                   initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_WRITE_ENA',
                                   dataType=f"std_logic_vector({self.bheight*self.bwidth} downto 0)",
                                   initialValue="(others => '0')")
        
        self.defineTypeOnTypePackage(Type(name=f'r_REGISTERS_1{self.minimalComponentFileName}', declaration=f'array (0 to {self.bheight-1}) of std_logic_vector({self.dataWidth-1} downto 0)'))
        self.addInternalSignalWire(name='r_REGISTERS',
                                   dataType=f"array ({self.bheight-1} downto 0) of r_REGISTERS_1{self.minimalComponentFileName}",
                                   initialValue="(others => (others => (others => '0')))")
        self.addInternalSignalWire(name='w_ROW_ADDR',
                                   dataType=f"std_logic_vector(6 downto 0)")
        self.addInternalSignalWire(name='w_COL_ADDR',
                                   dataType=f"std_logic_vector(5 downto 0)")
        
        self.addInternalComponent(component=OneHotEncoder(inputDataWidth=self.waddWidth,
                                                          outputDataWidth=self.bheight*self.bwidth +1),
                                                          componentCallName='u_OHE_REG',
                                                          portmap={ 'i_DATA': 'i_WRITE_ADDR',
                                                                    'o_DATA': 'w_WRITE_ENA'})
        
        self.internalOperations = f"""
  w_ROW_ADDR <= i_WRITE_ADDR(6 downto 0);
  w_COL_ADDR <= i_WRITE_ADDR(13 - 1 downto 7);

    p_REG : process (i_CLK, i_WRITE_ADDR, i_DATA, w_WRITE_ENA, i_WRITE_ENA) is
  begin

    if (rising_edge(i_CLK) and w_WRITE_ENA(to_integer(unsigned(i_WRITE_ADDR))) = '1' and i_WRITE_ENA = '1') then
      r_REGISTERS(to_integer(unsigned(w_COL_ADDR)))(to_integer(unsigned(w_ROW_ADDR))) <= i_DATA;
    end if;
  end process;
  {self.getGeneratedBlock()}

  o_DATA <= w_BLOCK_OUT;
        """
        self.OutputEntityAndArchitectureFile()



    def getGeneratedBlock(self):
        block = ''
        for i in range(0, self.bwidth-1):
            block += f'    w_BLOCK_OUT({i}) <= r_REGISTERS({i})(to_integer(unsigned(i_READ_ADDR)));'
        return block