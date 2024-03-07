from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic
from Components.add1 import Add1
class MultiplicadorConv(ComponentCommonMethods):

   
    def __init__(self):
        self.startInstance()
        self.minimalComponentFileName = f"multiplicador_conv"
        self.addGenericByParameters('i_DATA_WIDTH','INTEGER',8)
        self.addGenericByParameters('o_DATA_WIDTH','INTEGER',16)

        self.portMap =   { 'in': [
                                Port('i_DATA_1 ',f"STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)"),
                                Port('i_DATA_2',f"STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)")
                                ],
                            'out': [
                                    Port('o_DATA   ',f"STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)")
                                   ] 
                    }
        self.addInternalSignalWire('w_A','STD_LOGIC_VECTOR (i_DATA_WIDTH downto 0)',"(others => '0')")
        self.addInternalSignalWire('w_B','STD_LOGIC_VECTOR (i_DATA_WIDTH downto 0)',"(others => '0')")
        self.addInternalSignalWire('w_DATA','STD_LOGIC_VECTOR (17 downto 0)')

        self.internalOperations = """
            w_A(i_DATA_WIDTH - 1 downto 0) <= i_DATA_1;

            w_B(i_DATA_WIDTH - 1 downto 0) <= i_DATA_2;
            w_B(i_DATA_WIDTH) <= i_DATA_2(i_DATA_WIDTH - 1); -- estende bit de sinal do peso

            -- multiplicacao
            w_DATA <= STD_LOGIC_VECTOR(signed(w_A) * signed(w_B));

            o_DATA <= w_DATA(o_DATA_WIDTH - 1 downto 0);
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