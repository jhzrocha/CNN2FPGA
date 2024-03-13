from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.demux_1x import Demux_1x
class NucleoConvolucional(ComponentCommonMethods):
   
    def __init__(self, qtRows, qtColumns, qtPixelsPerRow):
        self.startInstance()
        self.qtRows = qtRows
        self.qtColumns = qtColumns
        self.qtPixelsPerRow = qtPixelsPerRow
        self.minimalComponentFileName = f"nucleoConvolucional"
        self.portMap =   { 'in': [
                                Port('i_CLK ','STD_LOGIC'),
                                Port('i_CLR','STD_LOGIC'),
                                Port('i_PIX_SHIFT_ENA','STD_LOGIC'),
                                Port('i_WEIGHT_SHIFT_ENA','STD_LOGIC'),
                                Port('i_WEIGHT','STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)')
                                ],
                            'out': [Port('o_PIX','STD_LOGIC_VECTOR (o_DATA_WIDTH - 1 downto 0)')]
                        }
        self.addMultipleGeneratedInputPorts(name='i_PIX_ROW', 
                                            qtPorts=qtRows,
                                            dataType='STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)')
        self.addGenericByParameters(name='i_DATA_WIDTH', 
                                    dataType='integer',
                                    initialValue=8)
        self.addGenericByParameters('w_CONV_OUT', 'integer',16)
        self.addGenericByParameters('o_DATA_WIDTH', 'integer',32)
        self.addArrayTypeOnArchitecture('t_MAT','STD_LOGIC_VECTOR(i_DATA_WIDTH - 1 downto 0)',qtRows-1)
        self.addArrayTypeOnArchitecture('t_MULT_OUT_MAT','STD_LOGIC_VECTOR(w_CONV_OUT - 1 downto 0)',qtRows*qtColumns-1)
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_PIX_ROW',
                                                     'dataType':'t_MAT ',
                                                     'initialValue':"(others =>  ( others => '0'))"})
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_WEIGHT_ROW',
                                                     'dataType':'t_MAT ',
                                                     'initialValue':"(others =>  ( others => '0'))"})
        self.addMultipleInternalSignalWires(qtRows, {'name': 'w_i_WEIGHT_ROW',
                                                     'dataType':'STD_LOGIC_VECTOR (i_DATA_WIDTH - 1 downto 0)',
                                                     'initialValue':''})
        self.addInternalSignalWire(name='w_MULT_OUT',dataType='t_MULT_OUT_MAT',initialValue="(others =>  ( others => '0'))")
        # internalDemux = Demux_1x(qtRows,) 
        # self.addInternalComponent(internalDemux, 'u_DEMUX_PEX')
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
"""
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