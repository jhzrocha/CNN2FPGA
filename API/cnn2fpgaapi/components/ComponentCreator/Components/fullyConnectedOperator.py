from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.type import Type
from Components.neuron import Neuron
from Components.registrador import Registrador
from Components.oneHotEncoder import OneHotEncoder

#Compilado
class FullyConnectedOperator(ComponentCommonMethods):
    
    #NUM_UNITS - nrUnits
    #BIAS_ADDRESS_WIDTH - biasAddressWidth
    #SCALE_FACTOR - scaleFactor
    #SCALE_SHIFT - scaleShift
    #DATA_WIDTH - dataWidth
    def __init__(self, nrUnits=2, biasAddressWidth=6, scaleFactor='"01000000000000000000000000000000"', scaleShift=7, dataWidth =8):
        self.nrUnits = nrUnits
        self.biasAddressWidth = biasAddressWidth
        self.scaleFactor = scaleFactor
        self.scaleShift = scaleShift
        self.dataWidth = dataWidth
        self.createComponent()
    
    
    def createComponent(self):
    
        self.startInstance()
        self.minimalComponentFileName = f'FullyConnectedOperator'
        self.portMap =   { 'in': [
                                Port('i_CLK','std_logic'),
                                Port('i_CLR','std_logic'),
                                Port('i_PIX',f'std_logic_vector({self.dataWidth-1} downto 0)', "(others => '0')"),
                                Port('i_WEIGHT', f'array (0 to {self.nrUnits-1}) of std_logic_vector({self.dataWidth-1} downto 0)', "(others => (others => '0'))"),
                                Port('i_REG_PIX_ENA','std_logic'),
                                Port('i_REG_WEIGHT_ENA','std_logic'),
                                Port('i_BIAS_SCALE','std_logic_vector(31 downto 0)'),
                                Port('i_REG_BIAS_ADDR',f'std_logic_vector({self.biasAddressWidth-1} downto 0)'),
                                Port('i_REG_BIAS_ENA','std_logic'),
                                Port('i_ACC_ENA','std_logic'),
                                Port('i_ACC_CLR','std_logic'),
                                Port('i_REG_OUT_CLR','std_logic',initialValue="'0'"),
                                Port('i_REG_OUT_ENA','std_logic'),
                                Port('i_REG_OUT_ADDR','std_logic_vector(5 downto 0)',initialValue="(others => '0')"),

                                ],
                            'out': [
                                    Port(name='o_PIX',dataType=f'array (0 to 34) of std_logic_vector({self.dataWidth-1} downto 0)',initialValue="(others => (others => '0'))"),
                                   ] 
                    }
        
        self.addInternalSignalWire('w_NFC_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        
        self.addInternalSignalWire('w_ADD_BIAS_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        
        self.addInternalSignalWire('w_A', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('w_B', dataType=f'std_logic_vector(31 downto 0)', initialValue="(others => '0')")

        self.addInternalSignalWire('w_SCALE_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(63 downto 0)', initialValue="(others => (others => '0'))")

        self.addInternalSignalWire('w_CAST_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('w_SHIFT_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('w_OFFSET_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(31 downto 0)', initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('w_CLIP_OUT', dataType=f'array (0 to {self.nrUnits-1}) of std_logic_vector(7 downto 0)', initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('r_REG_OUT', dataType=self.getPortDataType('o_PIX'), initialValue="(others => (others => '0'))")
        self.addInternalSignalWire('w_BIAS_ADDR', dataType=f'std_logic_vector({self.nrUnits-1} downto 0)', initialValue="(others => '0')")
        self.addInternalSignalWire('w_SCALE', dataType=f'std_logic_vector(31 downto 0)', initialValue="(others => '0')")
        self.addInternalSignalWire('w_REG_OUT_ADDR', dataType=f'std_logic_vector(34 downto 0)', initialValue="(others => '0')")

        self.generateUnits()
        self.generateOutBuffer()
        self.internalOperations = """
  o_PIX <= r_REG_OUT;
        """

        self.addInternalComponent(component=OneHotEncoder(inputDataWidth=self.biasAddressWidth
                                                          ,outputDataWidth=self.nrUnits),
                                  componentCallName=f'u_OHE_BIAS',
                                  portmap={ 'i_DATA': 'i_REG_BIAS_ADDR',
                                            'o_DATA': 'w_BIAS_ADDR'})
        self.addInternalComponent(component=OneHotEncoder(inputDataWidth=6
                                                          ,outputDataWidth=35),
                                  componentCallName=f'u_OHE_OUT',
                                  portmap={ 'i_DATA': 'i_REG_OUT_ADDR',
                                            'o_DATA': 'W_REG_OUT_ADDR'})
        
        self.OutputEntityAndArchitectureFile()


    def generateUnits(self):
        for i in range(self.nrUnits):
            self.addInternalSignalWire(f'w_REG_BIAS_OUT_{i}',                                      
                                       dataType='std_logic_vector(31 downto 0)',
                                        initialValue="(others => '0')")
            
            self.addInternalComponent(component=Neuron(inDataWidth=8, outDataWidth=32),
                                      componentCallName=f'u_UNIT_{i}',
                                      portmap={ 'i_CLK'           : 'i_CLK',
                                                'i_CLR'           : 'i_CLR',
                                                'i_ACC_ENA'       : 'i_ACC_ENA',
                                                'i_REG_PIX_ENA'   : 'i_REG_PIX_ENA',
                                                'i_REG_WEIGHT_ENA': 'i_REG_WEIGHT_ENA',
                                                'i_ACC_CLR'       : 'i_ACC_CLR',
                                                'i_PIX'           : f'i_PIX',
                                                'i_WEIGHT'        : f"i_WEIGHT{f'({i})' if i > 0 else ''}",
                                                'o_PIX'           : f"w_NFC_OUT{f'({i})' if i > 0 else ''}"})
            self.addInternalComponent(component=Registrador(dataWidth=32),
                                      componentCallName=f'u_REG_BIAS_{i}',
                                      portmap={ 'i_CLK' : 'i_CLK',
                                                'i_CLR' : 'i_CLR',
                                                'i_ENA' : f'w_REG_BIAS_ENA_w_BIAS_ADDR_{i}',
                                                'i_A'   : f'i_BIAS_SCALE',
                                                'o_Q'   : f'w_REG_BIAS_OUT_{i}'})
            
            self.addInternalSignalWire(f'w_REG_BIAS_ENA_w_BIAS_ADDR_{i}', dataType='std_logic')
            self.addInternalOperationLine(f"     w_REG_BIAS_ENA_w_BIAS_ADDR_{i}   <= i_REG_BIAS_ENA and w_BIAS_ADDR{f'({i})' if i>1 else ''};")

            self.addInternalOperationLine(f'     w_ADD_BIAS_OUT{f"({i})" if i>1 else ""}   <= std_logic_vector(signed(w_NFC_OUT{f"({i})" if i>1 else ""}) + signed(w_REG_BIAS_OUT_{i}));')
            self.addInternalOperationLine(f'     w_A{f"({i})" if i>1 else ""}(31 downto 0) <= w_ADD_BIAS_OUT{f"({i})" if i>1 else ""};')
            self.addInternalOperationLine(f'     w_SCALE_OUT{f"({i})" if i>1 else ""} <= std_logic_vector(signed(w_A{f"({i})" if i>1 else ""}) * signed({self.scaleFactor}));')
            self.addInternalOperationLine(f'     w_CAST_OUT{f"({i})" if i>1 else ""} <= w_SCALE_OUT{f"({i})" if i>1 else ""}(62 downto 31);')
            self.addInternalOperationLine(f'     w_SHIFT_OUT{f"({i})" if i>1 else ""}({31-self.scaleShift} downto 0)  <= w_CAST_OUT{f"({i})" if i>1 else ""}(31 downto {self.scaleShift});')
            self.addInternalOperationLine(f"     w_SHIFT_OUT{f'({i})' if i>1 else ''}(31 downto {31-self.scaleShift}) <= (others => '1') when (w_CAST_OUT{f'({i})' if i>1 else ''}(31) = '1') else (others => '0');")
            self.addInternalOperationLine(f"     w_OFFSET_OUT{f'({i})' if i>1 else ''} <= w_SHIFT_OUT{f'({i})' if i>1 else ''} + std_logic_vector(to_unsigned(82, 32));")
            self.addInternalOperationLine(f"     w_CLIP_OUT{f'({i})' if i>1 else ''} <= w_OFFSET_OUT{f'({i})' if i>1 else ''}(7 downto 0);")

    def generateOutBuffer(self):
        for i in range(0, 34):
            self.addInternalSignalWire(f'w_REG_BIAS_ENA_w_BIAS_ADDR_{i}', dataType='std_logic')
            self.addInternalOperationLine(f'     w_REG_OUT_ENA_W_REG_OUT_ADDR_{i}   <= i_REG_OUT_ENA and W_REG_OUT_ADDR({i});')
            self.addInternalComponent(component=Registrador(dataWidth=8),
                                        componentCallName=f'u_REG_OUT_{i}',
                                        portmap={ 'i_CLK' : 'i_CLK',
                                                'i_CLR' : 'i_REG_OUT_CLR',
                                                'i_ENA' : f'w_REG_BIAS_ENA_w_BIAS_ADDR_{i}',
                                                'i_A'   : f'w_CLIP_OUT{f"(0)" if self.nrUnits>1 else ""}',
                                                'o_Q'   : f'r_REG_OUT({i})'})