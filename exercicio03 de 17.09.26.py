distancia =float(input('Qual a distançia percorrida em km?'))
if distancia <= 200:
  preço = distancia * 0.50
  print('O preço da viagem foi de R$ {:.2f}'.format(preço))
else:
  preço = distancia * 0.45
  print('O preço final da sua viagem é de {:.2f}'.format(preço))