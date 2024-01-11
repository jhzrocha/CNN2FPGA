import os

class fileHandler:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def ler_arquivo(self):
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                conteudo = arquivo.read()
                return conteudo
        except FileNotFoundError:
            return f"O arquivo '{self.caminho_arquivo}' não foi encontrado."

    def escrever_arquivo(self, conteudo):
        with open(self.caminho_arquivo, 'w') as arquivo:
            arquivo.write(conteudo)
        print(f"Conteúdo escrito no arquivo '{self.caminho_arquivo}'.")

    def apendar_arquivo(self, conteudo):
        with open(self.caminho_arquivo, 'a') as arquivo:
            arquivo.write(conteudo)
        print(f"Conteúdo adicionado ao arquivo '{self.caminho_arquivo}'.")

    def createComponentsFolder(self):
        fullPath = os.path.join('ComponentsOutput')
        print(fullPath)
        if not os.path.exists(fullPath):
            os.makedirs(fullPath)

