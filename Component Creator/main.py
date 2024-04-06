from Components.nucleoConvolucional import NucleoConvolucional
from Components.io_buffer import IOBuffer
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = IOBuffer()

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


