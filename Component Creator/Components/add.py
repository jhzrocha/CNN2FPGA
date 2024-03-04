from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic
from Components.add1 import Add1
class Add(ComponentCommonMethods):

   
    def __init__(self, qt_bits):
        self.startInstance()
        self.minimalComponentFileName = f"add{qt_bits}"
        self.portMap =   { 'in': [
                                Port('a',f"std_logic_vector({qt_bits-1} DOWNTO 0)"),
                                Port('b',f"std_logic_vector({qt_bits-1} DOWNTO 0)"),
                                Port('cin','std_logic')
                            ],
                            'out': [Port('sum1',f"std_logic_vector({qt_bits-1} DOWNTO 0)"),
                                    Port('cout','std_logic'),
                                    Port('overflow','std_logic'),
                                    Port('underflow','std_logic')] 
                    }
        
        self.addInternalSignalWire('w_SIGNAL_BIT', 'std_logic')
        self.addInternalSignalWire('w_OVERFLOW', 'std_logic')
        self.addInternalSignalWire('w_UNDERFLOW', 'std_logic')
        self.addMultipleInternalSignalWires(qt_bits-1,{'name': 'c', 'dataType': 'std_logic', 'initialValue':''})
        self.addInternalSignalWire('w_SUM_OUT', f"std_logic_vector({qt_bits-1} DOWNTO 0)")
        self.addInternalComponents(qt_bits)
        self.internalOperations = """
        w_SUM_OUT(31) <= w_SIGNAL_BIT;           
        w_UNDERFLOW <= a(31) and b(31) and not w_SIGNAL_BIT;
        sum1 <= "10000000000000000000000000000000" when (w_UNDERFLOW = '1') else 
                "01111111111111111111111111111111" when (w_OVERFLOW= '1') else 
                w_SUM_OUT;
        overflow <=  w_OVERFLOW; 
        underflow <= w_UNDERFLOW;
        """
        self.OutputEntityAndArchitectureFile()


    def addInternalComponents(self,qtAdders):
        self.addInternalComponent(Add1(),f"D_adder0", {'a':'a(0)', 
                                                       'b':'b(0)', 
                                                       'cin':'cin',
                                                       'sum': 'w_SUM_OUT(0)', 
                                                       'cout':'c_0'})
        for x in range(1,qtAdders-1):
            self.addInternalComponent(Add1(),f"D_adder{x}", {'a':f"a({x})", 
                                                       'b':f"b({x})", 
                                                       'cin':f"c_{x-1}",
                                                       'sum': f"w_SUM_OUT({x})", 
                                                       'cout':f"c_{x}"})

        self.addInternalComponent(Add1(),f"D_adder{qtAdders-1}", {'a':f"a({qtAdders-1})", 
                                                       'b':f"b({qtAdders-1})", 
                                                       'cin':f"c_{qtAdders-2}",
                                                       'sum': 'w_SIGNAL_BIT', 
                                                       'cout':'cout'})