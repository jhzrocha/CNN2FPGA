from Components.nucleoConvolucional import NucleoConvolucional
from Components.poolingControl import PoolingController
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = PoolingController()

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


