from fileHandler import fileHandler 
import os
# Criando uma instância do ManipuladorDeArquivos
nome_do_arquivo = 'exemplo.txt'
pasta_especifica = 'pasta_exemplo'

# Criando o caminho completo para o arquivo na pasta específica
caminho_completo = os.path.join(pasta_especifica, nome_do_arquivo)

# Criando uma instância do ManipuladorDeArquivos com o caminho completo
manipulador = fileHandler(caminho_completo)

manipulador.createComponentsFolder()