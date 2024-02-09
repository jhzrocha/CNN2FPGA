from Components.convolutionalLayer import ConvolutionalLayer
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

multiplicador = ConvolutionalLayer([4,4],[2,2])


projectSpinal.setTopEntityComponent(multiplicador)

projectSpinal.start()


