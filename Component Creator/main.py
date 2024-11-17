from Components.nucleoConvolucional import NucleoConvolucional
from Components.parallelMultiply import ParallelMultiplicator
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = ParallelMultiplicator(inputQtBits=8)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


