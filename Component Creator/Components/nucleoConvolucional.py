from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.demux_1x import Demux_1x
from Components.multiplicador_conv import MultiplicadorConv
from Components.SumTree import SumTree
class NucleoConvolucional(ComponentCommonMethods):
    
    #Compilado
    #Testado
    #Não testado na prática    
    def __init__(self, qtRows, qtColumns, qtPixelsPerRow, inputDataWidth = 8, convolutionalOutput = 16, outputDataWidth = 32):

        self.startInstance()
        self.qtRows = qtRows
        self.qtColumns = qtColumns
        self.qtPixelsPerRow = qtPixelsPerRow
        self.minimalComponentFileName = f"nucleoConvolucional_{qtRows}_{qtColumns}_{qtPixelsPerRow}_{inputDataWidth}_{convolutionalOutput}_{outputDataWidth}"
        self.portMap =   { 'in': [
                                Port('i_CLK','STD_LOGIC'),
                                Port('i_CLR','STD_LOGIC'),
                                Port('i_PIX_SHIFT_ENA','STD_LOGIC'),
                                Port('i_WEIGHT_SHIFT_ENA','STD_LOGIC'),
                                Port('i_WEIGHT',f'STD_LOGIC_VECTOR ({inputDataWidth - 1} downto 0)')
                                ],
                            'out': [Port('o_PIX',f'STD_LOGIC_VECTOR ({outputDataWidth - 1} downto 0)')]
                        }
        self.addMultipleGeneratedInputPorts(name='i_PIX_ROW', 
                                            qtPorts=qtRows,
                                            dataType=f'STD_LOGIC_VECTOR ({inputDataWidth - 1} downto 0)')

        self.addArrayTypeOnArchitecture('t_MAT',f'STD_LOGIC_VECTOR({inputDataWidth - 1} downto 0)',qtRows)
        self.addArrayTypeOnArchitecture('t_MULT_OUT_MAT',f'STD_LOGIC_VECTOR({convolutionalOutput-1} downto 0)', qtRows*qtColumns)
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_PIX_ROW',
                                                     'dataType':'t_MAT ',
                                                     'initialValue':"(others =>  ( others => '0'))"})
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_WEIGHT_ROW',
                                                     'dataType':'t_MAT ',
                                                     'initialValue':"(others =>  ( others => '0'))"})
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_i_WEIGHT_ROW',
                                                     'dataType':f'STD_LOGIC_VECTOR ({inputDataWidth-1} downto 0)',
                                                     'initialValue':''})
        self.addInternalSignalWire(name='w_MULT_OUT',dataType='t_MULT_OUT_MAT',initialValue="(others =>  ( others => '0'))")
        internalDemux = Demux_1x(qtRows, inputDataWidth=inputDataWidth) 
        self.addInputPortByParameters(name='i_WEIGHT_ROW_SEL',
                                      dataType= f"STD_LOGIC_VECTOR ({internalDemux.getOptionLength() - 1} downto 0)")
        self.addInternalComponent(component=internalDemux, 
                                  componentCallName='u_DEMUX_PEX',
                                  portmap=self.getDemuxPortmap()
                                  )
        self.setMultiConvs(inputDataWidth, convolutionalOutput)
        self.internalOperations = f"""
        p_DESLOCAMENTO : process (i_CLR, i_CLK)
            begin
            -- reset
            if (i_CLR = '1') then
{self.getResetBehavior()}
            elsif (rising_edge(i_CLK)) then
                if (i_PIX_SHIFT_ENA = '1') then
{self.getWhenShiftBehavior()}
                end if;
{self.getWeightShiftBehavior(internalDemux)}
            end if;        
        end process;
"""
        self.addInternalComponent(SumTree(qtInputs= self.qtColumns*self.qtRows,
                                                 inputDataWidth= convolutionalOutput,
                                                 outputDataWidth= outputDataWidth
                                                 ), 'u_sumTree', self.getArvoreSomaPortmap())
        self.OutputEntityAndArchitectureFile()

    def getResetBehavior(self):
        resetbehavior = ''
        for x in range(0,self.qtRows):
            resetbehavior = resetbehavior + f"                w_PIX_ROW_{x} <= (others =>  ( others => '0'));\n"
        resetbehavior = resetbehavior + "\n" 
        for x in range(0,self.qtRows):
            resetbehavior = resetbehavior + f"                w_WEIGHT_ROW_{x} <= (others =>  ( others => '0'));\n"
        return resetbehavior

    def getWhenShiftBehavior(self):
        shiftBehavior = ''
        for pixelIndex in range(self.qtPixelsPerRow-1,0,-1):
            for pixelRowIndex in range(0,self.qtRows):
                shiftBehavior = shiftBehavior + f"                  w_PIX_ROW_{pixelRowIndex}({pixelIndex}) <= w_PIX_ROW_{pixelRowIndex}({pixelIndex-1});\n"
            shiftBehavior = shiftBehavior + "\n" 

        for pixelRowIndex in range(0,self.qtRows):
                shiftBehavior = shiftBehavior + f"                  w_PIX_ROW_{pixelRowIndex}(0) <= i_PIX_ROW_{pixelRowIndex};\n"
        
        return shiftBehavior
    
    def getWeightShiftBehavior(self,internalDemux):
        behavior = ''
        for rowIndex in range(0,self.qtRows):
            behavior = behavior + '            if (i_WEIGHT_SHIFT_ENA = ' + "'1' and i_WEIGHT_ROW_SEL = "+'"{}") then'.format(internalDemux.getIntegerInBinaryOption(rowIndex)) + '\n'
            for x in range(self.qtRows-1,0,-1):
                behavior = behavior + f"               w_WEIGHT_ROW_{rowIndex}({x}) <= w_WEIGHT_ROW_{rowIndex}({x-1});\n"    
            
            behavior = behavior + f"               w_WEIGHT_ROW_{rowIndex}({0}) <= w_i_WEIGHT_ROW_{rowIndex};\n"    

            behavior = behavior + "            end if;\n"

        return behavior
    
    def setMultiConvs(self,inputDataWidth,convolutionalOutput):
        outCounter = 0
        for i in range(self.qtRows):
            for j in range(self.qtColumns):
                self.addInternalComponent(component=MultiplicadorConv(inputDataWidth=inputDataWidth,
                                                                      outputDataWidth=convolutionalOutput),
                                        componentCallName=f"u_MUL_{outCounter}",
                                        portmap={'i_DATA_1': f"w_PIX_ROW_{i}({j})",
                                            'i_DATA_2': f"w_WEIGHT_ROW_{i}({j})",
                                            'o_DATA': f"w_MULT_OUT({outCounter})"}
                                        )
                outCounter = outCounter + 1
    
    def getDemuxPortmap(self):
        demuxPortmap = {'i_A':'i_WEIGHT',
                        'i_SEL' :'i_WEIGHT_ROW_SEL'}
        for x in range(0,self.qtRows):
           demuxPortmap[f"o_PORT_{x}"] = f"w_i_WEIGHT_ROW_{x}"
        
        return demuxPortmap
    
    def getArvoreSomaPortmap(self):
        portmap = {}
        for i in range(self.qtRows*self.qtColumns):
            portmap[f"i_PORT_{i}"] = f"w_MULT_OUT({i})"
        
        portmap['o_DATA'] = 'o_PIX'
        return portmap
