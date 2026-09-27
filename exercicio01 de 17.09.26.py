velocidade =float(input('Digite a sua velocidade:'))
if velocidade > 80:
   print('Você foi multado')
   print('Quantos km acima do limite ele andou? {:.2f}'.format(velocidade - 80))
   multa = (velocidade - 80) * 7
   print('Sua multa foi de RS {:.2f}'.format(multa))