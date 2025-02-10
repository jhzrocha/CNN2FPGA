from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.ram import RAM
class IOBuffer(ComponentCommonMethods):

#    Testado no modelsim
    def __init__(self, qtBlocks=3, dataWidth=8, addrWidth=10, RAMsize =128):
        self.startInstance()
        self.minimalComponentFileName = f'IOBuffer_{qtBlocks}b_{dataWidth}dw_{addrWidth}adw_{RAMsize}ramSize'
        self.portMap =   { 'in': [
                                    Port(name='i_CLK',dataType="std_logic"),
                                    Port(name='i_DATA',dataType=f"std_logic_vector ({dataWidth-1} downto 0)"),
                                    Port(name='i_WRITE_ENA',dataType="std_logic"),
                                    Port(name='i_SEL_LINE',dataType=f"std_logic_vector ({len(bin(qtBlocks)[2:])-1} downto 0)"),
                                    Port(name='i_WRITE_ADDR',dataType=f"std_logic_vector ({addrWidth-1} downto 0)",initialValue="(others => '0')")
                                ],
                            'out': []
                    }

        self.addArrayTypeOnArchitecture(name='t_BLOCKS_ADDR',datatype=f'STD_LOGIC_VECTOR({addrWidth-1} downto 0)',size=3)
        self.addInternalSignalWire(name='w_ADDRs',dataType='t_BLOCKS_ADDR',initialValue="(others => (others => '0'))")
        self.addInternalSignalWire(name='w_WRITE_ENA',dataType=f'STD_LOGIC_VECTOR({qtBlocks-1} downto 0)',initialValue="(others => '0')")
        
        self.addMultipleGeneratedOutputPorts(qtBlocks,f"std_logic_vector ({dataWidth-1} downto 0)",'o_DATA_ROW')
        self.addMultipleGeneratedInputPorts(qtPorts=qtBlocks,
                                            dataType=f"std_logic_vector ({addrWidth-1} downto 0)", 
                                            name='i_READ_ADDR',
                                            initialValue="(others => '0')")
                
        self.addRAM(qtBlocks,dataWidth, addrWidth,RAMsize)
        self.internalOperations = ""
        self.addInternalConnections(qtBlocks=qtBlocks)
        self.OutputEntityAndArchitectureFile()

    def addRAM(self,qtBlocks,dataWidth, addrWidth,RAMsize):
        for i in range(qtBlocks):
            self.addInternalComponent(component = RAM(dataWidth= dataWidth,
                                                      addrWidth= addrWidth,
                                                      size= RAMsize),
                                      componentCallName=f'ram{i}',
                                      portmap= {'i_CLK':'i_CLK',
                                                'i_ADDR':f'w_ADDRs({i})',
                                                'i_DATA':'i_DATA',
                                                'i_WRITE':f'w_WRITE_ENA({i})',
                                                'o_DATA':f'o_DATA_ROW_{i}'}
                                      )
    def addInternalConnections(self,qtBlocks):
        for i in range(qtBlocks):
            self.addInternalOperationLine(f"            w_ADDRs({i}) <= i_WRITE_ADDR when (i_WRITE_ENA = '1') else i_READ_ADDR_{i};")            
            self.addInternalOperationLine(f"            w_WRITE_ENA({i}) <= '1' " + f'when (i_SEL_LINE = "{bin(i)[2:].zfill( len(bin(qtBlocks)[2:]))}") and ' + "(i_WRITE_ENA = '1') else '0';")
