nome =input('Digite seu nome:')
cores = {
         'azul': '\033[34m',
         'roxo': '\033[35m',
         'amarelo': '\033[33m',
         'verde': '\033[32m',
         'limpa': '\033[33m',
}
print('Seja bem vindo, {}{}{}!!!'.format(cores['azul'], nome ,cores['limpa']))