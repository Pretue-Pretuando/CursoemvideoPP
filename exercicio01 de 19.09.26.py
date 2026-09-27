salario = float(input('Qual o seu salario:'))
if salario <= 1250:
    aumento = salario * 0.10
else:
    aumento = salario * 0.15
novosalario = salario + aumento
print('o aumento é de {:.2f}'.format(aumento))
print('o novo salario é de {:.2f}'.format(novosalario))
