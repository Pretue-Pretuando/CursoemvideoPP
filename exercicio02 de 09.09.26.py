dia = int(input('Quantos dias o carro foi alugado?'))
km = float(input("quantos km foi percorrido?"))
pago = (dia * 60) + (km * 0.15)
print('o total a pagar é {:.2f}'.format(pago))
