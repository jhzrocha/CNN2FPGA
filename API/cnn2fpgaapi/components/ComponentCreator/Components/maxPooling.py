from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.comparisonTree import ComparisonTree

#Compilado
#Necessário alterar para quantidades relativas de linhas e colunas
#Atualmente com 2x2
class MaxPooling(ComponentCommonMethods):
    
    def __init__(self, dataWidth = 8):
        self.dataWidth = dataWidth
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'MaxPooling_{self.dataWidth}dw'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_PIX_SHIFT_ENA','std_logic'),
                                Port('i_PIX_ROW_0',f'std_logic_vector ({self.dataWidth-1} downto 0)'),
                                Port('i_PIX_ROW_1',f'std_logic_vector ({self.dataWidth-1} downto 0)')
                                ],
                            'out': [
                                Port(name='o_PIX',dataType=f'std_logic_vector ({self.dataWidth-1} downto 0)'),
                                   ] 
                    }
        
        self.addArrayTypeOnArchitecture(name=f't_MAT_{self.minimalComponentFileName}',
                                        datatype=f'std_logic_vector({self.dataWidth-1} downto 0)',
                                        size=2)

        self.addInternalSignalWire(name='w_PIX_ROW_0',
                                   dataType=f't_MAT_{self.minimalComponentFileName}',
                                   initialValue="(others => (others => '0'))")
        
        self.addInternalSignalWire(name='w_PIX_ROW_1',
                                   dataType=f't_MAT_{self.minimalComponentFileName}',
                                   initialValue="(others => (others => '0'))")
        
        self.internalOperations = """
  p_DESLOCAMENTO : process (i_CLR, i_CLK)
  begin
    -- reset
    if (i_CLR = '1') then
      w_PIX_ROW_0 <= (others => (others => '0'));
      w_PIX_ROW_1 <= (others => (others => '0'));

    elsif (rising_edge(i_CLK)) then

      -- desloca registradores de pixels
      if (i_PIX_SHIFT_ENA = '1') then

        w_PIX_ROW_0(1) <= w_PIX_ROW_0(0);
        w_PIX_ROW_1(1) <= w_PIX_ROW_1(0);

        w_PIX_ROW_0(0) <= i_PIX_ROW_0;
        w_PIX_ROW_1(0) <= i_PIX_ROW_1;

      end if;
    end if;
  end process;
        """

        self.addInternalComponent(component = ComparisonTree(qtInputs=4, dataWidth=self.dataWidth),
                            componentCallName = 'u_ARVORE_COMP',
                            portmap = {
                                'i_PIX_0' :'w_PIX_ROW_0(0)',
                                'i_PIX_1' :'w_PIX_ROW_0(1)',
                                'i_PIX_2' :'w_PIX_ROW_1(0)',
                                'i_PIX_3' :'w_PIX_ROW_1(1)',
                                'o_PIX'   :'o_PIX'
                            })
        self.OutputEntityAndArchitectureFile()



