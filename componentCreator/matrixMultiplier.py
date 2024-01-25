from ComponentCommonMethods import ComponentCommonMethods
from generic import Generic
from port import Port
from adder import AdderComponent
from multiplicator import Multiplicator


class MatrixMultiplier(ComponentCommonMethods):


    def __init__(self, qtPixels):
        self.minimalComponentFileName = 'MatrixMultiplier'
        self.portMap = { 'in': [Port('i_DATA',f"signed(0 to p_QT_BITS*{qtPixels}-1)"),
                                Port('i_KERNEL',f"signed(0 to p_QT_BITS*{qtPixels}-1)")],
                         'out': [Port('o_VALUE','integer')] 
                }
        self.generics = [Generic('p_QT_BITS','natural','8')]

        self.internalOperations = """
        multiplicacoes:
        process({})
        begin
        o_VALUE <= {};           
        end process multiplicacoes;"""

        self.addInternalComponent(AdderComponent(qtPixels), 'adder')
        self.AddMultipliers(qtPixels)

    def AddMultipliers(self, qtPixels):
        for i in range(qtPixels):
            self.addInternalComponent(Multiplicator(),f"Multi_{i}")