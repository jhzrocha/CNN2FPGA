from FileHandler.fileHandler import FileHandler

class Spinal():
    
    def start(self):
        self.topEntityComponent.createDesignFile()
        FileHandler('Output').addCoreFiles()
    
    def setTopEntityComponent(self, component):
        self.topEntityComponent = component
    
    def setFPGADevice(self, device):
        self.fpgaDevice = device
    
