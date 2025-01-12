from Components.io_buffer import IOBuffer
from Spinal.Spinal import Spinal
from Components.conv1_op import Conv1Op

projectSpinal = Spinal()
obj = Conv1Op()

projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


