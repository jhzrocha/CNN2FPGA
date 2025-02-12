import os
import shutil
import zipfile

class FileHandler:
    def __init__(self, directoryName):
        self.directoryName = directoryName
        self.directoryPath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir),self.directoryName))
        self.makeDirectory()

    def makeDirectory(self):
        if not os.path.exists(self.directoryPath):
            os.makedirs(self.directoryPath)

    def addFile(self, fileName, texto):
        filePath = os.path.join(self.directoryPath, fileName)
        for file in os.listdir(self.directoryPath):
            if(f"{fileName}.vhd" == file):
                os.remove(filePath)        
        with open(filePath, 'w') as file:
            file.write(texto)
        print(f"File '{fileName}' create sucessfully on {self.directoryName}.")
    
    def clean(self):
        for file in os.listdir(self.directoryPath):
            filePath = os.path.join(self.directoryPath, file)
            os.remove(filePath)
        print(f" '{self.directoryName}' directory cleaned.")

    def verifyIfFileExists(self, fileName, directoryName):
        self.directoryName = directoryName
        filePath = os.path.join(self.directoryPath, fileName)
        if os.path.isfile(filePath):
            return True
        else:
            return False
    
    def addCoreFiles(self):
        origem = os.path.abspath(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir),'Cores'))
        for arquivo in os.listdir(origem):
            caminho_origem = os.path.join(origem, arquivo)
            if os.path.isfile(caminho_origem):
                caminho_destino = os.path.join(self.directoryPath, arquivo)
                shutil.copy2(caminho_origem, caminho_destino)
    
    def addTypesToPackageFile(self, typesToPackage):
        if(len(typesToPackage)> 0):        
            declarations = ''

            filePath = os.path.join(self.directoryPath, 'types_pkg.vhd')

            if (self.verifyIfFileExists('types_pkg', self.directoryName)):
                with open(filePath, 'r') as file:
                    fileContent = file.read()

            for type in typesToPackage:
                declarations = declarations + type.getDeclaration() + '\n'

            defaultContent = f'''
    LIBRARY ieee;
    USE ieee.std_logic_1164.ALL;

    PACKAGE types_pkg IS
{declarations}
    END PACKAGE types_pkg;'''
            with open(filePath, 'w') as file:
                file.write(defaultContent)

    def addMemoryInitializationComponents(self, type, fpga):
        origem = os.path.abspath(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir),f'MemoryInitializationComponents/Files/{type}/{fpga}'))
        for arquivo in os.listdir(origem):
            caminho_origem = os.path.join(origem, arquivo)
            if os.path.isfile(caminho_origem):
                caminho_destino = os.path.join(self.directoryPath, arquivo)
                shutil.copy2(caminho_origem, caminho_destino)
