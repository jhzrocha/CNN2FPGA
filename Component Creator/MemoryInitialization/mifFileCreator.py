from FileHandler.fileHandler import FileHandler

class MIFFileCreator():

    width = 0
    depth = 0
    addressRadix = 'UNS'
    dataRadix = 'BIN'

    def createMifFileByParameters(self, fileName, width, depth, addressRadix, dataRadix, values):
        template = f'''
-- begin_signature
-- ROM
-- end_signature
WIDTH={width};
DEPTH={depth};
ADDRESS_RADIX={addressRadix};
DATA_RADIX={dataRadix};

CONTENT BEGIN
{self.getValuesAsMifContent(values,width)}
END;
        '''

        fileHandler = FileHandler("Output")
        fileHandler.addFile(f'{fileName}.mif', template)

    def getValuesAsMifContent(self, s, size):
        lines = [f"{i}: {s[j:j+size].ljust(size, '0')}" for i, j in enumerate(range(0, len(s), size))]
        return "\n".join(reversed(lines))
    
    def createFileByFile(self, fileName, fileContent):
        fileHandler = FileHandler("Output")
        fileHandler.addFile(f'{fileName}.mif', fileContent)
