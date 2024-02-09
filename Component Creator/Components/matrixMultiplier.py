from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.generic import Generic
from ComponentBases.port import Port
from Components.adder import AdderComponent
from Components.multiplicator import Multiplicator


class MatrixMultiplier(ComponentCommonMethods):


    def __init__(self, qtPixels):
        self.minimalComponentFileName = f"MatrixMultiplier_{qtPixels}px"
        self.portMap = { 'in': [Port('i_DATA',f"signed(0 to p_QT_BITS*{qtPixels}-1)"),
                                Port('i_KERNEL',f"signed(0 to p_QT_BITS*{qtPixels}-1)"),
                                Port('i_ENA', 'std_logic')],
                         'out': [Port('o_VALUE','integer')] 
                }
        self.generics = [Generic('p_QT_BITS','natural','8')]
        super().__init__()

        self.AddMultipliers(qtPixels)
        self.addInternalComponent(AdderComponent(qtPixels), 'adder')
        self.setInternalComponentsPortMap(qtPixels)
        self.OutputEntityAndArchitectureFile()

    def AddMultipliers(self, qtPixels):
        for i in range(qtPixels):
            self.addInternalComponent(Multiplicator(),f"Multi_{i}")
            
    def setInternalComponentsPortMap(self, qtPixels):
        adderParameters = {}
        for i in range(qtPixels):
            multParameters = {'i_DATA':f"i_DATA({i}*p_QT_BITS to p_QT_BITS*{i+1}-1)",
                          'i_KERNEL' : f"i_KERNEL({i}*p_QT_BITS to p_QT_BITS*{i+1}-1)",
                          'i_ENA' : 'i_ENA',
                          'o_VALUE' : f"w_MULT_{i}"
                          }
            self.addInternalSignalWire(f"w_MULT_{i}", 'integer', 0)
            self.setInternalComponentPortMap(f"Multi_{i}",multParameters)
            self.setInternalComponentGenerics(f"Multi_{i}",'p_QT_BITS','p_QT_BITS')
            adderParameters[f"i_PORT_{i}"] = f"w_MULT_{i}"
        adderParameters['o_VALUE'] = 'o_VALUE'
        self.setInternalComponentPortMap('adder',adderParameters)
