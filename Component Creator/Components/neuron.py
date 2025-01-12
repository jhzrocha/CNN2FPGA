from ComponentBases.ComponentCommonMethods import ComponentCommonMethods
from ComponentBases.port import Port
from Components.registrador import Registrador
from Components.multiplicador_conv import MultiplicadorConv

class Neuron(ComponentCommonMethods):
    # Não finalizado
    # Não Compilado
    # Não testado
       def __init__(self, inDataWidth=8,outDataWidth=32):
              self.startInstance()
              self.minimalComponentFileName = f'neuron_{inDataWidth}_{outDataWidth}'
              self.portMap =   { 'in': [Port('i_CLK','STD_LOGIC'),
                                   Port('i_CLR','STD_LOGIC'),
                                   Port('i_ACC_ENA','STD_LOGIC'),
                                   Port('i_REG_PIX_ENA','STD_LOGIC'),
                                   Port('i_REG_PES_ENA','STD_LOGIC'),
                                   Port('i_ACC_CLR','STD_LOGIC'),
                                   Port('i_PIX',f'STD_LOGIC_VECTOR ({inDataWidth-1} downto 0)'),
                                   Port('i_PES',f'STD_LOGIC_VECTOR ({inDataWidth-1} downto 0)')],
                            'out': [Port('o_PIX',f'STD_LOGIC_VECTOR ({outDataWidth-1} downto 0)')] 
                            }
              
              self.addInternalSignalWire(name='w_MULT_OUT',
                                          dataType=f'std_logic_vector({outDataWidth-1} downto 0)',
                                          initialValue="(others => '0')")
              self.addInternalSignalWire(name='w_ADD_OUT',
                                          dataType=f'std_logic_vector({inDataWidth-1} downto 0)',
                                          initialValue="(others => '0')")
              self.addInternalSignalWire(name='r_PIX',
                                          dataType=f'std_logic_vector({outDataWidth-1} downto 0)')
              self.addInternalSignalWire(name='r_WEIGHT', #r_PES
                                          dataType=f'std_logic_vector({inDataWidth-1} downto 0)')
              self.addInternalSignalWire(name='r_ACC',
                                          dataType=f'std_logic_vector({outDataWidth-1} downto 0)')
              
              self.addInternalComponent(component=Registrador(inDataWidth),
                                   componentCallName= 'u_REG_WEIGHT',
                                   portmap={'i_CLK': 'i_CLK',
                                                 'i_CLR': 'i_CLR',
                                                 'i_ENA': 'i_REG_WEIGHT_ENA',
                                                 'i_A' : 'i_WEIGHT',
                                                 'o_Q' : 'r_WEIGHT'}
                                          )
              self.addInternalComponent(component=Registrador(inDataWidth),
                                   componentCallName= 'u_REG_PIX',
                                   portmap={'i_CLK': 'i_CLK',
                                            'i_CLR': 'i_CLR',
                                            'i_ENA': 'i_REG_PIX_ENA',
                                            'i_A' : 'i_PIX',
                                            'o_Q' : 'r_PIX'}
                                          ) 
              self.addInternalComponent(component=Registrador(outDataWidth),
                                   componentCallName= 'u_REG_ACC',
                                   portmap={'i_CLK': 'i_CLK',
                                            'i_CLR': '(i_CLR or i_ACC_CLR)',
                                            'i_ENA': 'i_ACC_ENA',
                                            'i_A' : 'w_ADD_OUT',
                                            'o_Q' : 'r_ACC'}
                                          )
              
              self.addInternalComponent(component=MultiplicadorConv(),
                     componentCallName= 'u_MULT',
                     portmap={'i_DATA_1': 'r_PIX',
                                   'i_DATA_2': 'r_WEIGHT',
                                   'o_DATA': 'w_MULT_OUT(15 downto 0)'}
                                       )
              self.internalOperations = f"""
         -- extende sinal
       w_MULT_OUT({outDataWidth-1} downto 16) <= (others => '1') when (w_MULT_OUT(15) = '1') else
       (others                             => '0');

       -- somador
       w_ADD_OUT <= std_logic_vector(signed(r_ACC) + signed(w_MULT_OUT));

       -- saida
       o_PIX <= w_ADD_OUT;
"""

              self.OutputEntityAndArchitectureFile()

