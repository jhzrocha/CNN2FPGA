from Spinal.Spinal import Spinal

from Components.fullyConnectedLayer import FullyConnectedLayer

projectSpinal = Spinal()
obj = FullyConnectedLayer(weightsFileName='test1.mif', biasFileName='test2.mif')


projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


