salario =float(input('Qual é o salario do funcionario? Rs:'))
novo = salario + (salario * 15/100)
print('o funcionario que ganhava {:.2f}, com aumento de 15%, passou a ganhar {:.2f}'.format(salario,novo))