from FileHandler.fileHandler import FileHandler

class FileManager:
    def __init__(self):
        self.usedComponents = {}

    
    def addUsedComponent(self, component):
        self.usedComponents[component.minimalComponentFileName] = component

    def verifyIfIsUsed(self, component):
        if component.minimalComponentFileName not in self.usedComponents.keys():
            self.addUsedComponent(component)
        print(self.usedComponents)
        


    
