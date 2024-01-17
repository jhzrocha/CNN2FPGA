from adder import adderComponent
# Criando uma instância do ManipuladorDeArquivos

# a = ComponentCommonMethods('teste')

# a.addMultipleGeneratedInputPorts(4,'integer')
# a.addMultipleGeneratedOutputPorts(4,'integer')

# iconnections = ['w1','w1','w1','w1']
# oconnections = ['w2','w2','w2','w2']

# a.setPortMapConnections(iconnections,oconnections)

# print(a.getEntityAndArchitectureFile())


b = adderComponent('Adder',5)
b.addGenericByParameters('QT_BITS_P', 'integer', 0)
print(b.getEntityAndArchitectureFile())
print(b.getObjectCall('a'))