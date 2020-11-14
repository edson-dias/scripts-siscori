#!/usr/bin/env python3

"""
Script main realiza as configurações para simplificar o arquivo .csv e criar o arquivo .xlsx.
Autores: Edson, Henrique.
Versão: 1.0
"""

from src.utils import file_manipulate, color, DICT_FILTERS
from src.decorators import header


@header
def set_header(**kwargs):
    pass


def get_filters():
    choice = list()

    _filter = DICT_FILTERS

    [print(f'[{k}]: {color(text=f"{v[0]}", cor="red")} - {v[1]}') for k, v in _filter.items()]

    choice.append(input('\nDigite os números dos filtros a serem alterados, ou tecle "C"\n'
                        'para confirmar os filtros mostrados: '))

    if choice[-1] not in "Cc":
        choice = choice[0].split(',')
        for itens in choice:
            _filter[itens][1] = (input(f'Filtro {color(text=f"[{itens}]", cor="red", effect="bold")}: '))

    return _filter


def get_files_names(*args):
    # RECEBER AS LISTAS NCM, MESES E UMA LISTA DE ANOS PARA ENTÃO "DESCOBRIR" OS NOMES DOS ARQUIVOS. PENSAR EM LIST COMPREHENSION, COM FORS ANINHADOS!

    pass


if __name__ == '__main__':

    set_header(format=True, text='Simplificador Siscori - V1.1',
               cor='red', effect='bold')

    filters = get_filters()
    set_header(format=True, head=False)



'''




cabecalho_inicio(cor(' Arquivo CSV - XLSX ', 'blue', '1'))
nome_csv = 'CAPI' + \
    input('Digite o nome do arquivo sem "CAPI" e sem ".csv": ') + '.CSV'
nome_xlsx = input('Digite o nome do arquivo sem ".xlsx": ')
cabecalho_final()

cabecalho_inicio(cor(' Filtros NCM ', 'lblue', '1'))
print('NCMs a serem filtrados (tecle "f" para finalizar): ')

while True:
    x = input()
    if x not in 'Ff':
        ncm_list.append(x)
    else:
        break
cabecalho_final()

cabecalho_inicio(cor(' Opções Escolhidas ', 'red', '1'))
print(f'Caminho arquivo csv: {caminho_csv_escolhido}')
print(f'Filtros NCM: {ncm_list}')
print(f'Filtros PA: {filtro_paises_escolhido}')
print(f'Filtros PC: {filtro_paises_escolhido}\n')

while True:
    cond = input(cor('Confirma os dados acima? (Y/N): ', 'red', '1'))
    if cond not in 'YyNn':
        print('Entrada Inválida! Digite novamente.')
    else:
        if cond in 'Yy':
            break
        else:
            print('Saindo do script...')
            sys.exit()
cabecalho_final()

cabecalho_inicio(cor(' Processos ', 'yellow', '1'))
importacoes = Simplificador(nome_csv, caminho_csv_escolhido, ncm=ncm_list,
                            pa=filtro_paises_escolhido, pc=filtro_paises_escolhido)
print('Iniciando a leitura do arquivo .csv ...')
importacoes.get_csv()
importacoes.set_del()
print('Filtrando arquivo csv...')
importacoes.set_filtro()
print('Criando arquivo xlsm...')
importacoes.create_xlsm(caminho_csv_escolhido, nome_xlsx)
print('Finalizado!')
cabecalho_final()
'''
