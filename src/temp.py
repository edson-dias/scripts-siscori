'''
def multiplica(funcao):
    def teste_multiplica(**kwargs):
        p = kwargs.get('j', 'Não achou nada')
        print(p)
        a = funcao(**kwargs)
        return a * (2+p)
    return teste_multiplica


@multiplica
def func(**kwargs):
    j = kwargs.get('j')
    return j


b = func(j=4)
print(b)



def teste(n):
    def multiplica(funcao):
        def teste_multiplica(*args):
            a = funcao(*args)
            print('Decorador!')
            return a * 2
        return teste_multiplica
    return multiplica


@teste(2)
def func(j):
    return j


a = func(2)
print(a)

'''

join('teste', 'teste')
a = ('teste', 'olá')
a.join(',')
print(a)
