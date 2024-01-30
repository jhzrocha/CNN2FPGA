from components.adder import AdderComponent
from components.multiplicator import Multiplicator
from components.matrixMultiplier import MatrixMultiplier
from port import Port
from fileHandler import FileHandler
import os
# Criando uma instância do ManipuladorDeArquivos

multiplicador = MatrixMultiplier(9)

print(multiplicador.getEntityAndArchitectureFile())

gerenciador = FileHandler("Output", os.path.dirname(os.path.abspath(__file__)))

# gerenciador.addFile("arquivo1.txt", "Conteúdo do arquivo 1.")
gerenciador.clean()
