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
        self.generics = [Generic('p_QT_BITS','natural','1')]
        self.internalOperations = """
            proc:
            process(i_ENA, i_CLK)
                variable cont : integer := 0;
            begin
                if (i_ENA = '1') then
                    if(cont < 8) then
						w_OPTION <= to_unsigned(cont, 4);
                        w_DATA <= i_DATA(cont*p_QT_BITS to (p_QT_BITS*(cont+1))-1);
					    cont := cont + 1;
					end if;
                end if;
            end process proc;
        """
        self.setOutputPorts(qtimagePixels,qtKernelPixels)

        self.setInternalComponents(qtimagePixels, qtKernelPixels)
        self.addInternalSignalWire('w_MATRIX_MULT_O', 'integer', 0)
        matrixMultiplierPortmap = {'i_DATA': 'w_DATA',
                                        'i_KERNEL': 'i_KERNEL',
                                        'i_ENA': 'i_ENA',
                                        'o_VALUE':'w_MATRIX_MULT_O'
                                   }        
        self.setInternalComponentPortMap('MatrixMultiplier',matrixMultiplierPortmap)

        self.OutputEntityAndArchitectureFile()

    def setOutputPorts(self, qtimagePixels, qtKernelPixels):
        qtPorts = 0
        for i in range((qtimagePixels[0] - qtKernelPixels[0])+1):
            for j in range((qtimagePixels[1] - qtKernelPixels[1])+1):
                self.addOutputPortByParameters(f"O_VALUE_{i}_{j}",'integer', f"w_VALUE_O_{i}_{j}")
                qtPorts = qtPorts+1

    def setSwitcher(self, qtimagePixels, qtKernelPixels):
        qtPorts = 0
        component = Switcher(self.getQtOutputs(qtimagePixels,qtKernelPixels))
        self.addInternalComponent(component, 'switcher')
        self.processment = self.internalOperations.format(self.getQtOutputs(qtimagePixels,qtKernelPixels)-1, component.getQtBitsInputOption())
        self.addInternalSignalWire('w_OPTION',f"unsigned(0 to {component.getQtBitsInputOption()}-1)",f'"{self.getInitialOptionValue(component)}"')
        self.addInternalSignalWire('w_DATA', f"signed(0 to p_QT_BITS*{qtKernelPixels[0]*qtKernelPixels[1]}-1)", '')

        internalSwitcherParameters = {'i_ENA':'i_ENA',
                                      'i_VALUE' :'w_MATRIX_MULT_O',
                                      'i_OPTION' : 'w_OPTION'}
        for i in range((qtimagePixels[0] - qtKernelPixels[0])+1):
            for j in range((qtimagePixels[1] - qtKernelPixels[1])+1):
                internalSwitcherParameters[f"o_PORT_{qtPorts}"] = f"O_VALUE_{i}_{j}"
                qtPorts = qtPorts + 1
        self.setInternalComponentPortMap('switcher',internalSwitcherParameters)
    
    def getQtOutputs(self, qtimagePixels, qtKernelPixels):
        return (((qtimagePixels[0]-qtKernelPixels[0])+1)*((qtimagePixels[1]-qtKernelPixels[1])+1))
    
    def qtOutputsBinary(self, integer):
        return "{0:b}".format(integer)

    def setInternalComponents(self,qtimagePixels,qtKernelPixels):
        self.setSwitcher(qtimagePixels,qtKernelPixels)
        self.setMatrixMultiplier(qtimagePixels,qtKernelPixels)
        self.setInternalComponentGenerics('MatrixMultiplier','p_QT_BITS','p_QT_BITS')

    def setMatrixMultiplier(self,qtimagePixels,qtKernelPixels):
        matrixMultiplier = MatrixMultiplier(qtKernelPixels[0]*qtKernelPixels[1])
        self.addInternalComponent(matrixMultiplier, 'MatrixMultiplier')
    
    def getInitialOptionValue(self,switcher):
        initialValue = ''
        for i in range(switcher.getQtBitsInputOption()):
            initialValue = initialValue + '0'
        
        return initialValue