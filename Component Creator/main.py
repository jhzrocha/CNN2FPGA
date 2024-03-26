from Components.nucleoConvolucional import NucleoConvolucional
from Components.genericMultiplexer import Multiplexer
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = Multiplexer(2)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


