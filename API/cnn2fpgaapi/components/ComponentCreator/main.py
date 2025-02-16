from Spinal.Spinal import Spinal
from Components.poolingOperator import PoolingOperator
from Components.poolingLayer import PoolingLayer

projectSpinal = Spinal()
obj = PoolingLayer()
projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


