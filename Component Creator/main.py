from Components.io_buffer import IOBuffer
from Spinal.Spinal import Spinal
from Components.conv1_crt import ConvCrt
from Components.maxPooling import MaxPooling

projectSpinal = Spinal()
obj = MaxPooling()

projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


