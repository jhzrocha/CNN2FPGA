from Spinal.Spinal import Spinal
from Components.poolingOperator import PoolingOperator
from Components.poolingLayer import PoolingLayer
from Components.fullyConnectedOperator import FullyConnectedOperator
from Components.fullyConnectedLayer import FullyConnectedLayer
from Components.fullyConnectedControl import FullyConnectedControl
from Components.fullyConnected import FullyConnected

projectSpinal = Spinal()
obj = FullyConnected()
projectSpinal.setTopEntityComponent(obj)

projectSpinal.start()
