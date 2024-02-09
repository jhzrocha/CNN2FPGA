from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic
from Components.matrixMultiplier import MatrixMultiplier



class ConvolutionalLayer(ComponentCommonMethods):


    def __init__(self, qtimagePixels = [], qtKernelPixels = []):
        self.minimalComponentFileName = f"ConvolutionalLayerIm{qtimagePixels[0]}x{qtimagePixels[1]}K{qtKernelPixels[0]}x{qtKernelPixels[1]}"
        self.portMap = { 'in': [Port('i_DATA',f"signed(0 to p_QT_BITS*{qtimagePixels[0]*qtimagePixels[1]}-1)"),
                                Port('i_KERNEL',f"signed(0 to p_QT_BITS*{qtKernelPixels[0]*qtKernelPixels[1]}-1)"),
                                Port('i_ENA', 'std_logic'),
                                Port('i_RST', 'std_logic'),
                                Port('i_CLK', 'std_logic')],
                          'out': []                           
                        }
        self.setOutputPorts(qtimagePixels,qtKernelPixels)
        self.generics = [Generic('p_QT_BITS','natural','8')]
        self.internalOperations = """
            multi:
            process(i_ENA,i_CLK,i_RST)            
            begin
                if (i_ENA= '1') then
                    w_O_VALUE <= TO_INTEGER(signed(i_DATA) * (signed(i_KERNEL))); 
                end if;
            end process multi;

        """        
        super().__init__()
        self.addInternalSignalWire('w_DATA', 'signed(0 to p_QT_BITS*{qtKernelPixels[0]*qtKernelPixels[1]}-1)', 'i_DATA(0*p_QT_BITS to p_QT_BITS*1-1)')
        self.addInternalSignalWire('w_MATRIX_MULT_O', 'integer', 0)


        self.addInternalComponent(MatrixMultiplier(qtKernelPixels[0]*qtKernelPixels[1]), 'MatrixMultiplier')
        matrixMultiplierPortmap = {'i_DATA': 'w_DATA',
                                        'i_KERNEL': 'i_KERNEL',
                                        'i_ENA': 'i_ENA',
                                        'o_VALUE':'w_MATRIX_MULT_O'
                                   }        
        self.setInternalComponentPortMap('MatrixMultiplier',matrixMultiplierPortmap)
        self.OutputEntityAndArchitectureFile()


    def setOutputPorts(self, qtimagePixels, qtKernelPixels):
        for i in range((qtimagePixels[0] - qtKernelPixels[0])+1):
            for j in range((qtimagePixels[1] - qtKernelPixels[1])+1):
                self.addOutputPortByParameters(f"O_Value{i}_{j}",'integer', f"w_VALUE_O{i}_{j}")
              
