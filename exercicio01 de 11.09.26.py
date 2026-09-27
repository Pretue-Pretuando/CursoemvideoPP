from random import shuffle

n1 =input('Nome do aluno:')
n2 =input("Nome do aluno:")
n3 =input("Nome do aluno:")
n4 =input("Nome do aluno")
lista =[n1,n2,n3,n4]
shuffle(lista)
print('A ordem de apresentaçao é {},{},{},{}'.format(*lista))