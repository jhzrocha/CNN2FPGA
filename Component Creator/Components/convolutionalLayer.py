from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from ComponentBases.generic import Generic
from Components.matrixMultiplier import MatrixMultiplier
from Components.switcher import Switcher



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
        self.generics = [Generic('p_QT_BITS','natural','8')]
        self.internalOperations = f"""
            proc:
            process(i_ENA)            
            begin
                if (i_ENA= '1') then
                    for i in 0 to {self.getQtOutputs(qtimagePixels,qtKernelPixels)} loop
                        
                        wait on w_MATRIX_MULT_O;
                        
                    end loop;
                end if;
            end process proc;

        """
        super().__init__()
        self.addInternalSignalWire('w_DATA', f"signed(0 to p_QT_BITS*{qtKernelPixels[0]*qtKernelPixels[1]}-1)", 'i_DATA(0*p_QT_BITS to p_QT_BITS*1-1)')
        self.addInternalSignalWire('w_MATRIX_MULT_O', 'integer', 0)
        self.addInternalComponent(Switcher(self.getQtOutputs(qtimagePixels,qtKernelPixels)), 'switcher')
        self.setOutputPortsAndSwitcher(qtimagePixels,qtKernelPixels)



        self.addInternalComponent(MatrixMultiplier(qtKernelPixels[0]*qtKernelPixels[1]), 'MatrixMultiplier')
        matrixMultiplierPortmap = {'i_DATA': 'w_DATA',
                                        'i_KERNEL': 'i_KERNEL',
                                        'i_ENA': 'i_ENA',
                                        'o_VALUE':'w_MATRIX_MULT_O'
                                   }        
        self.setInternalComponentPortMap('MatrixMultiplier',matrixMultiplierPortmap)

        self.OutputEntityAndArchitectureFile()


    def setOutputPortsAndSwitcher(self, qtimagePixels, qtKernelPixels):
        qtPorts = 0
        self.addInternalSignalWire('w_OPTION','unsigned(0 to 4-1)','"0000"')
        internalSwitcherParameters = {'i_ENA':'i_ENA',
                                      'i_VALUE' :'w_MATRIX_MULT_O',
                                      'i_OPTION' : 'w_OPTION'}
        for i in range((qtimagePixels[0] - qtKernelPixels[0])+1):
            for j in range((qtimagePixels[1] - qtKernelPixels[1])+1):
                self.addInternalSignalWire(f"w_VALUE_O_{i}_{j}",'integer',0)
                self.addOutputPortByParameters(f"O_VALUE_{i}_{j}",'integer', f"w_VALUE_O_{i}_{j}")
                internalSwitcherParameters[f"o_PORT_{qtPorts}"] = f"w_VALUE_O_{i}_{j}"
                qtPorts = qtPorts+1

        self.setInternalComponentPortMap('switcher',internalSwitcherParameters)
    
    def getQtOutputs(self, qtimagePixels, qtKernelPixels):
        return (((qtimagePixels[0]-qtKernelPixels[0])+1)*((qtimagePixels[1]-qtKernelPixels[1])+1))
    

