from Spinal.Spinal import Spinal

from Components.fullyConnectedLayer import FullyConnectedLayer
from FileHandler.fileHandler import FileHandler


class ComponentCreator():

    def __init__(self):
        projectSpinal = Spinal()
        obj = FullyConnectedLayer(weightsFileName='test1.mif', biasFileName='test2.mif')
        projectSpinal.setTopEntityComponent(obj)
        projectSpinal.start()
