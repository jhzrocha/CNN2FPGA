from Components.add import Add
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = Add(32)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


