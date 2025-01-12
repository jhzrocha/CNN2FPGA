from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port

class Conv1Op(ComponentCommonMethods):
    def __init__(self):
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'conv1_crt_'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_GO','std_logic')
                                ],
                            'out': [
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),
                                    Port(name='o_OUT_DATA',dataType=f"{self.minimalComponentFileName}_outData"),

                                   ] 
                    }
        
   
        self.internalOperations = """

        """
        self.OutputEntityAndArchitectureFile()



