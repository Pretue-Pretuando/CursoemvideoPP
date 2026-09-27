larg = float(input('digite a largura da parede:'))
alt = float(input("digite a altura da parede:"))
area = larg * alt
print('sua parede tem uma dimensao de {}x{} e uma area de {} m²'.format(larg,alt,area))
tinta = area/2
print('voce vai precisar de {}l de tinta para pintar a parede'.format(tinta))