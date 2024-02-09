import os

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
