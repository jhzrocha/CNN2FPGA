from Spinal.Spinal import Spinal
from Components.poolingOperator import PoolingOperator
from Components.poolingLayer import PoolingLayer
from Components.fullyConnectedOperator import FullyConnectedOperator
from Components.fullyConnectedLayer import FullyConnectedLayer
from Components.fullyConnectedControl import FullyConnectedControl


projectSpinal = Spinal()
obj = FullyConnectedLayer(numUnits=1,weightsFileName='conv1.mif', biasFileName= 'conv2_bias.mif')
projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


# print(len(bin(64)[2:]))