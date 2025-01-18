from Components.io_buffer import IOBuffer
from Spinal.Spinal import Spinal
from Components.fullyConnectedOperator import FullyConnectedOperator

projectSpinal = Spinal()
obj = FullyConnectedOperator()

projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()

