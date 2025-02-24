from Spinal.Spinal import Spinal
from Components.poolingOperator import PoolingOperator
from Components.poolingLayer import PoolingLayer
from Components.fullyConnectedOperator import FullyConnectedOperator
from Components.fullyConnectedLayer import FullyConnectedLayer
from Components.neuron import Neuron

projectSpinal = Spinal()
obj = FullyConnectedLayer(numUnits=1, weightsFileName='conv1.mif', biasFileName='conv2_bias.mif')
projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()


