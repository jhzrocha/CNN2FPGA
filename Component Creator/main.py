from Components.arvore_soma_conv import ArvoreSomaConv
from Spinal.Spinal import Spinal


projectSpinal = Spinal()

registrador1 = ArvoreSomaConv(9)

projectSpinal.setTopEntityComponent(registrador1)
projectSpinal.start()


