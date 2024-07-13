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
        
        if (poolingType.lower == 'max'):
            self.addInternalComponent(component=GreaterComparissonTree(,pixelDataWidth))
        
        if (poolingType.lower == 'avg'):
            self.addInternalComponent(component=AverageTree(qtInputs=qtPixelsPerRow*qtPixelsRows,
                                                            inputDataWidth=pixelDataWidth),
                                      componentCallName='Tree'))
        self.internalOperations = """ """
        self.addSumTree(qtInputs,inputDataWidth)
        self.OutputEntityAndArchitectureFile()




