#!/usr/bin/env python3

"""
Script main realiza as configurações para simplificar o arquivo .csv e criar o arquivo .xlsx.
Autores: Edson, Henrique.
Versão: 1.0
"""

import sys

from src.utils import color, DICT_FILTERS, MONTHS_CONVERSION
from src.decorators import header
from src.siscori_classes import SiscoriData


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
        choice = choice[0].replace(" ", "").split(',')
        for itens in choice:
            _filter[itens][1] = (input(f'Filtro {color(text=f"[{itens}]", cor="red", effect="bold")}: '))

    return _filter


def _months_to_numbers(month_str):

    months_numb = [MONTHS_CONVERSION[key] for key in month_str if key in MONTHS_CONVERSION.keys()]

    return months_numb


def get_files_names(*args):

    temp_list = list()
    files_list = list()

    ncm_list = sorted(args[0].replace(" ", "").split(','))
    months_temp = args[1].replace(" ", "").split(',')
    years_list = args[2].replace(" ", "").split(',')

    months_list = _months_to_numbers(months_temp)

    [temp_list.append(ncm_item[0:2] + months_item + years_item[2:4] + '.csv') for ncm_item in ncm_list
     if ncm_item[0:2] not in temp_list for months_item in months_list for years_item in years_list]

    files_list.append('Files')
    files_list.append(', '.join(temp_list))

    return files_list


def data_confirm():
    while True:
        cond = input('\nConfirma os dados acima? (Y/N): ')
        if cond not in 'YyNn':
            print('Entrada Inválida! Digite novamente.')
        else:
            if cond in 'Yy':
                break
            else:
                print('Saindo do script...')
                sys.exit()


if __name__ == '__main__':

    set_header(format=True, text='Simplificador Siscori - V1.1',
               cor='red', effect='bold')

    filters = get_filters()
    filters['5'] = get_files_names(filters['3'][1], filters['4'][1], filters['5'][1])

    set_header(format=True, head=False)

    [print(f'{color(text=f"{v[0]}", cor="red")} - {v[-1]}') for k, v in filters.items()]

    data_confirm()

    set_header(format=True, text='Processando os dados...',
               cor='lblue', effect='bold')

    origin = filters.get('1')[1]
    acquisition = filters.get('2')[1]
    ncm = filters.get('3')[1]

    for files in filters['5'][1].replace(" ", "").split(','):

        data = SiscoriData(countries_list=origin, sec_countries_list=acquisition, ncm_list=ncm)
        data.get_csv(file_name=files)
        data.set_del()
        data.set_filtro()

# Flag: Deletar o objeto data criado a cada ciclo do for, assim como jogar as informações de data para o BD a cada ciclo
# Atenção !!! Os objetos dados não foram testados fora dos testes unitários.
# Perguntar antes do for se deseja criar arquivos do excel, jogar para o BD ou fazer ambos.


'''
importacoes.get_csv()
importacoes.set_del()
print('Filtrando arquivo csv...')
importacoes.set_filtro()
print('Criando arquivo xlsm...')
importacoes.create_xlsm(caminho_csv_escolhido, nome_xlsx)
print('Finalizado!')
cabecalho_final()
'''
