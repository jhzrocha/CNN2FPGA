from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.greaterComparissonTree import GreaterComparissonTree
from Components.averageTree import AverageTree

class Pooling(ComponentCommonMethods):
   
    def __init__(self, pixelDataWidth =8, qtPixelsPerRow = 2, qtPixelsRows = 2, poolingType='Max'):
        self.startInstance()
        self.minimalComponentFileName = f'{poolingType}Pooling'
        self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                  Port('i_CLR','STD_LOGIC'),
                                  Port('i_PIX_SHIFT_ENA','STD_LOGIC')],
                           'out': [
                                   Port('o_PIX',f'STD_LOGIC_VECTOR ({pixelDataWidth-1} downto 0)')] 
                         }
        
       
        self.addMultipleGeneratedInputPorts(qtPixelsRows,f'STD_LOGIC_VECTOR ({pixelDataWidth - 1} downto 0)','i_PIX_ROW')
        self.addArrayTypeOnArchitecture('t_MAT',f'STD_LOGIC_VECTOR({pixelDataWidth-1} downto 0)',qtPixelsPerRow)
        self.addMultipleInternalSignalWires(qtPixelsRows,{'name': 'w_PIX_ROW',
                                                          'dataType': 't_MAT',
                                                           "initialValue":"(others =>  ( others => '0'))"})
        
        poolingPortmap = self.getPoolingPortmap(qtPixelsRows,qtPixelsRows)
        if (poolingType == 'max'):
            self.addInternalComponent(component=GreaterComparissonTree(qtInputs=qtPixelsPerRow*qtPixelsRows,
                                                                       dataWidth=pixelDataWidth),
                                      componentCallName='Tree',
                                      portmap=poolingPortmap)
        
        if (poolingType == 'avg'):
            self.addInternalComponent(component=AverageTree(qtInputs=qtPixelsPerRow*qtPixelsRows,
                                                            inputDataWidth=pixelDataWidth),
                                      componentCallName='Tree',
                                      portmap=poolingPortmap)
        self.internalOperations = """ """
        self.setInternalProcess(qtPixelsRows,qtPixelsPerRow)
        self.OutputEntityAndArchitectureFile()


    def getPoolingPortmap(self,qtPixelsRows,qtPixelsPerRow):
        portmap = {}
        counter = 0
        for i in range(0,qtPixelsRows):
            for j in range(0,qtPixelsPerRow):
                portmap[f'i_PIX_{counter}'] = f'w_PIX_ROW_{i}({j})'
                counter = counter + 1

        portmap['o_PIX'] = 'o_PIX'
        return portmap

    def setInternalProcess(self,qtPixelsRows,qtPixelsPerRow):

        self.addInternalOperationLine('''
        p_DESLOCAMENTO : process (i_CLR, i_CLK)
            begin
                if (i_CLR = '1') then ''')
        
        for i in range(qtPixelsRows):
            self.addInternalOperationLine(f"                    w_PIX_ROW_{i} <= (others =>  ( others => '0'));")

        self.addInternalOperationLine('''
                elsif (rising_edge(i_CLK)) then
                    if (i_PIX_SHIFT_ENA = '1') then ''')
        
        for i in range(0,qtPixelsRows):
            for j in range(0,qtPixelsPerRow-1):            
                self.addInternalOperationLine(f'                        w_PIX_ROW_{i}({j+1}) <= w_PIX_ROW_{i}({j});')

        self.addInternalOperationLine('')
        for i in range(0,qtPixelsRows):
            self.addInternalOperationLine(f'                        w_PIX_ROW_{i}(0) <= i_PIX_ROW_{i};')

        self.addInternalOperationLine('''
                    end if;           
                end if;        
            end process;
        ''')
