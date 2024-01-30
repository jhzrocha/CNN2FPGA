import os

class FileHandler:
    def __init__(self, directoryName,path):
        self.directoryName = directoryName
        self.path = path
        self.directoryPath = os.path.join(self.path, self.directoryName)
        self.makeDirectory()

    def makeDirectory(self):
        if not os.path.exists(self.directoryPath):
            os.makedirs(self.directoryPath)
            print(f"Directory '{self.directoryName}' created sucessfully.")
        else:
            print(f"Directory '{self.directoryName}' already exists.")

    def addFile(self, nome_file, texto):
        filePath = os.path.join(self.directoryPath, nome_file)
        with open(filePath, 'w') as file:
            file.write(texto)
        print(f"File '{nome_file}' create sucessfully on {self.directoryName}.")

    def clean(self):
        for file in os.listdir(self.directoryPath):
            filePath = os.path.join(self.directoryPath, file)
            os.remove(filePath)
        print(f"files removidos da pasta '{self.directoryName}'.")
