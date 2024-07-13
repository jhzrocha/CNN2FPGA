from Components.nucleoConvolucional import NucleoConvolucional
from Components.averageTree import AverageTree
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = AverageTree(6,8)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


