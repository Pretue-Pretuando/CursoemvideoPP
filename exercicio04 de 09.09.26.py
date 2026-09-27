import random

aluno1 =input('digite o nome do aluno 1:')
aluno2 =input('digite o nome do aluno 2:')
aluno3 =input('digite o nome do aluno 3:')
aluno4 =input('digite o nome do aluno 4:')
lista = (aluno1, aluno1, aluno2, aluno3, aluno4)
print(random.choice(lista))
