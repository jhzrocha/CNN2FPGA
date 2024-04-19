
class Converter():

    arquivo = ''
    entityname = ''
    
    entityStartLine = 0
    entityEndLine = 0

    librariesAndUses = []

    genericStartLine= 0
    genericEndLine = 0
    generics = []

    portmapStartLine= 0
    portmapEndLine = 0
    portmapIn = []
    portmapOut = []

    architectureStartLine=0
    architectureDeclarationEndLine = 0


    usedComponents = {}
    internalComponents = {}
    
    internalSignal = []


    def __init__(self,filePath):
        self.arquivo = open(filePath,'r')
        self.lines = open(filePath,'r').readlines()
        self.removeCommentLines()
        self.defineEntity()
        self.setLibrariesAndUses()
        self.defineArchitecture()
    
    def __str__(self):
        return f'''
    entityName = {self.entityname}
    entityStartLine = {self.entityStartLine}
    entityEndLine = {self.entityEndLine}
    
    genericStartLine= {self.genericStartLine}
    genericEndLine = {self.genericEndLine}
    generics = {self.generics}

    portmapStartLine= {self.portmapStartLine}
    portmapEndLine = {self.portmapEndLine}
    portmapIn = {self.portmapIn}
    portmapOut = {self.portmapOut}

    architectureStartLine= {self.architectureStartLine}
    architectureDeclarationEndLine= {self.architectureDeclarationEndLine}
    
    usedComponents = {self.usedComponents}
    
    internalComponents = {self.internalComponents}

    internalSignal = {self.internalSignal}


'''
    
    def setLibrariesAndUses(self):
        for line in self.lines:
            if(line.find('use') != -1 or line.find('library') != -1):
                self.librariesAndUses.append(line)

    def removeCommentLines(self):
        i = 0
        while i < len(self.lines):
            if (self.hasComment(self.lines[i]) and self.lines[i].strip().find('--') < 1):
                self.lines.pop(i)
                i = i-1
            i = i + 1

    def hasComment(self,line):
        if(line.find('--') != -1):
            return True
        else:
            return False

    def setEntityStartLine(self):
        counter = 0
        for line in self.lines:        
            if line.find('entity') != -1 and self.hasComment(line) == False:
                self.entityStartLine = counter
                break       
            counter = counter + 1

    def setEntityEndLine(self):
        for index in range(self.entityStartLine,len(self.lines)-1):
            line = self.lines[index]
            if line.find('end ') != -1 and self.hasComment(line) == False:
                self.entityEndLine = index
                break       

    def setEntityName(self,entityLine):
        self.entityname = entityLine.split(' ')[1]

    def setGeneric(self):
        counter = self.entityStartLine
        for line in self.lines[self.entityStartLine:self.entityEndLine]:        
            if line.find('generic') != -1 :
                self.genericStartLine = counter
                break
            counter = counter + 1
        for line in self.lines[self.genericStartLine:self.entityEndLine]:        
            generic = []
            if line.find(');') != -1 :
                self.genericEndLine = counter
                break 
            else:
                if line.find(':') != -1:
                    generic = line.replace(' ','').split(';')[0].split(':')
                    if (len(generic) == 3):
                        generic[2] = generic[2].replace('=','')
                    else:
                       if (generic[1].find('\n') != -1):
                           generic[1] = generic[1].replace('\n','')
                       generic.append('')
                    self.generics.append(generic)
            counter = counter + 1
    
    def setPortmap(self):
        counter = self.genericEndLine
        for line in self.lines[self.genericEndLine:self.entityEndLine]:        
            if not self.isInLine('port',line):
                self.portmapStartLine = counter
                break       
            counter = counter + 1
        for line in self.lines[self.portmapStartLine:self.entityEndLine]:        
            if ':' in line:
                if (self.isInLine('in',line)):
                    self.addInputPort(line)
                elif (self.isInLine('out',line)):
                    self.addOutputPort(line)
            counter = counter + 1
    
    def iniciateInternalComponents(self):
        for usedComponent in self.usedComponents:
                self.internalComponents[usedComponent] = {}

    def isArchitectureStartLine(self, line):
        return True if 'architecture' in line else False

    def setArchitectureFirstLine(self):
        for index in range(self.entityEndLine,len(self.lines)-1):
            line = self.lines[index]            
            if self.isArchitectureStartLine(line) :
                self.architectureStartLine = index
                break
    
    def setArchitectureDeclarationEndLine(self):
        for index in range(self.architectureStartLine,len(self.lines)-1):
            line = self.lines[index]
            if 'begin' in line:
                self.architectureDeclarationEndLine = index
                break

    def setArchitectureDeclarations(self):
        self.setGenericComponentDeclarations()
        self.setSignalDeclarations()
        
    def setSignalDeclarations(self):
        for index in range(self.architectureStartLine,self.architectureDeclarationEndLine):
            line = self.lines[index]            
            
            if(line.find('signal') != -1):
                signal = line.replace('signal','').strip().split(';')[0].split(':')
                if(len(signal) != 3):
                    signal.append('')
                else:
                    signal[2] = signal[2].replace('=','',1).strip()
                
                signal[0] = signal[0].strip()
                signal[1] = signal[1].strip()
                self.internalSignal.append(signal)    
    
    def setGenericComponentDeclarations(self):
        for index in range(self.architectureStartLine,self.architectureDeclarationEndLine):
            line = self.lines[index]
            if('component' in line and 'component;' not in line):
                componentname = line.strip().split(' ')[1]
                self.usedComponents[componentname] = {}
                internalIndex = index
                internalLine = self.lines[internalIndex]
                while 'end component;' not in internalLine.lower():
                    if ('generic ' in internalLine.lower() or 'generic(' in internalLine.lower() or ' generic(' in internalLine.lower()):                    
                        genericLines = ''
                        self.usedComponents[componentname]['generic'] = []
                        while 'port' not in internalLine and 'PORT' not in internalLine and 'Port' not in internalLine:
                            genericLines = genericLines + internalLine
                            internalIndex = internalIndex + 1
                            internalLine = self.lines[internalIndex]
                        genericLines = genericLines.replace('\n','')[genericLines.find('(') + 1:genericLines.find(');')]
                        generics = genericLines.strip().replace(');','').split(';')
                        for generic in generics:
                            addedGeneric = generic.split('--')[0].split(':')
                            addedGenericName = addedGeneric[0].strip()
                            addedGenericType = addedGeneric[1].strip()
                            addedGenericValue = addedGeneric[2].replace('=','').strip()
                            self.usedComponents[componentname]['generic'].append([addedGenericName,addedGenericType,addedGenericValue])
                        index = internalIndex
                    if('port' in internalLine.lower()):
                        self.usedComponents[componentname]['portmap'] = {}
                        self.usedComponents[componentname]['portmap']['in'] = []
                        self.usedComponents[componentname]['portmap']['out'] = []
                        portmapLines = ''
                        while ':' in internalLine or ');' not in internalLine:
                            portmapLines = portmapLines + internalLine
                            internalIndex = internalIndex + 1
                            internalLine = self.lines[internalIndex]
                        portmaps = portmapLines.replace('PORT','port').replace('\n','').replace('\t','').replace('port','').replace('(','',1).split(';')
                        for port in portmaps:
                            portmap = port.split('--')[0].split(':')
                            portName = portmap[0].strip()
                            portType = portmap[1]
                            portValue = ''
                            if len(portmap) == 3:
                                portValue = portmap[2].replace('=','',1)
                            
                            if ' in ' in port.lower():
                                self.usedComponents[componentname]['portmap']['in'].append([portName,portType.replace(' in','').replace(' IN','').strip(),portValue.strip()])

                            if ' out ' in port.lower():
                                self.usedComponents[componentname]['portmap']['out'].append([portName,portType.replace(' out','').replace(' OUT','').strip(),portValue])

                    internalIndex = internalIndex + 1
                    internalLine = self.lines[internalIndex]
    
    def defineArchitecture(self):
        self.setArchitectureFirstLine()
        self.setArchitectureDeclarationEndLine()
        self.setArchitectureDeclarations()        
        self.iniciateInternalComponents()
        for index in range(self.architectureDeclarationEndLine,len(self.lines)-1):
            line = self.lines[index]

            for usedComponent in self.usedComponents:
                portMap = {}
                if f" : {usedComponent}" in line: 
                    splitedLine = line.split(' : ')
                    internalName = splitedLine[0].replace('\n','').strip()
                    componentName = splitedLine[1].replace('\n','').strip()                    

                    for i in range(index,len(self.lines)-1):
                        line = self.lines[i]
                        if(line.find(');') != -1):
                            break
                        if(line.find('=>') != -1): 
                            portLine = line.split('--')[0].strip()
                            port = portLine.split(',')[0].split('=>')[0].strip()
                            portConexion = portLine.split(',')[0].split('=>')[1].strip()
                            portMap[port] = portConexion
                    
                    self.internalComponents[componentName][internalName] = portMap

    def strip(self,array):
        for i in range(len(array)-1):
            array[i] = array[i].strip()
            

    def defineEntity(self):
        self.setEntityStartLine()
        self.setEntityName(self.lines[self.entityStartLine])
        self.setEntityEndLine()        
        self.setGeneric()
        self.setPortmap()

    def isInLine(self, substring, line):
        if substring.lower() in line.lower():
            return True
        return False
    
    def addInputPort(self,line):
        port = line.replace(' in ','').replace(' IN ','').split(';')[0].split(':')        
        if (len(port) == 3):
            port[2] = port[2].replace('=','',1)
        else:
            port.append('')                    
        self.strip(port)
        self.portmapIn.append(port)

    def addOutputPort(self,line):
        port = line.replace('\n','').replace(' out ','').replace(' OUT ','').split(';')[0].split(':')
        if (len(port) == 3):
            port[2] = port[2].replace('=','')
        else:
            port.append('')
        self.strip(port)
        self.portmapOut.append(port)
