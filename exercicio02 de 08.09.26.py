preço =float(input('Qual é o preço do produto? Rs:'))
novo = preço - (preço * 5 /100)
print("o produto que custava {:.2f}, com a promoçao e o desconto de 5% fica {:.2f}".format(preço,novo))