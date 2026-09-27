import math

an = float(input('Digite o angulo que vocce deseja:'))
seno = math.sin(math.radians(an))
cono = math.cos(math.radians(an))
tan = math.tan(math.radians(an))
print('o angulo em seno é {:.2f}, cono {:.2f} e a tan é {:.2f}'.format(seno,cono,tan))
