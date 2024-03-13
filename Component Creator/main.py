from Components.nucleoConvolucional import NucleoConvolucional

from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = NucleoConvolucional(qtRows=3,qtColumns=3,qtPixelsPerRow=3)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


