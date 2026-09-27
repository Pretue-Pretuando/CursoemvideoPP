import math

ca =float(input("Digite um cateto oposto:"))
co =float(input("Comprimento do cateto oposto:"))
hi =math.hypot(ca,co)
print(" a hipotenusa mede {:.2f}".format(hi))