from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.maxComparisonTree import MaxComparisonTree
from Components.averageTree import AverageTree

#Compilado
class PoolingComputer(ComponentCommonMethods):
    
    def __init__(self, dataWidth = 8, qtRows = 2, qtCols = 2, poolingType = 'MAX'):
        self.dataWidth = dataWidth
        self.qtRows = qtRows
        self.qtCols = qtCols
        self.poolingType = poolingType
        self.createComponent()
    
    def createComponent(self):    
        self.startInstance()
        self.minimalComponentFileName = f'PoolingComputer{self.dataWidth}dw_{self.qtRows}x{self.qtCols}'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_PIX_SHIFT_ENA','std_logic'),
                                ],
                            'out': [
                                Port(name='o_PIX',dataType=f'std_logic_vector ({self.dataWidth-1} downto 0)'),
                                   ] 
                    }
        self.addMultipleGeneratedInputPorts(qtPorts=self.qtRows,
                                            dataType=f'std_logic_vector ({self.dataWidth-1} downto 0)',
                                            name='i_PIX_ROW',)
        self.addArrayTypeOnArchitecture(name=f't_MAT_{self.minimalComponentFileName}',
                                        datatype=f'std_logic_vector({self.dataWidth-1} downto 0)',
                                        size=self.qtCols)
        
        self.addMultipleInternalSignalWires(quantity=self.qtRows,
                                            parameters={'name': 'w_PIX_ROW', 
                                                        'dataType': f't_MAT_{self.minimalComponentFileName}', 
                                                        'initialValue':"(others => (others => '0'))"}
                                            )
        
        self.internalOperations = f"""
  p_DESLOCAMENTO : process (i_CLR, i_CLK)
  begin
    -- reset
    if (i_CLR = '1') then
{self.getClearBehavior()}
    elsif (rising_edge(i_CLK)) then
      -- desloca registradores de pixels
      if (i_PIX_SHIFT_ENA = '1') then
{self.getShiftBehavior()}
      end if;
    end if;
  end process;
        """
        self.setComparisonTree()
        self.OutputEntityAndArchitectureFile()

    def getShiftBehavior(self):
      internalOperation = ''
      for column in range(0, self.qtCols-1):
        for row in range(0, self.qtRows):
          internalOperation += f"         w_PIX_ROW_{row}({column+1}) <= w_PIX_ROW_{row}({column});\n"
      
      for row in range(0, self.qtRows):
          internalOperation += f"         w_PIX_ROW_{row}(0) <= i_PIX_ROW_{row};\n"

      return internalOperation

    def getClearBehavior(self):
      internalOperation = ''
      for row in range(0, self.qtRows):
        internalOperation += f"         w_PIX_ROW_{row} <= (others => (others => '0'));\n"
      return internalOperation
    
    def setComparisonTree(self):
      portmap = {'o_PIX'   :'o_PIX'}
      for i in range(0, (self.qtRows* self.qtCols)):
         portmap[f'i_PIX_{i}'] = f'w_PIX_ROW_{int(i/self.qtCols)}({i%self.qtCols})'
      
      if (self.poolingType == 'MAX'):
        self.addInternalComponent(component = MaxComparisonTree(qtInputs=(self.qtRows*self.qtCols), dataWidth=self.dataWidth),
                      componentCallName = 'u_MAX_TREE',
                      portmap = portmap)
      
      if (self.poolingType == 'AVG'):
        self.addInternalComponent(component = AverageTree(qtInputs=(self.qtRows*self.qtCols), inputDataWidth=self.dataWidth),
                      componentCallName = 'u_AVG_TREE',
                      portmap = portmap)