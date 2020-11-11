#!/usr/bin/env python3

"""
Script main realiza as configurações para simplificar o arquivo .csv e criar o arquivo .xlsx.
Autores: Edson, Henrique.
Versão: 1.0
"""

import sys

from siscori_classes import SiscoriData
from utils import file_manipulate
from decorators import header


@header
def set_header(**kwargs):
    pass


if __name__ == '__main__':

    set_header(format=True, text='Simplificador Siscori - V1.1',
               cor='red', effect='bold')

    filters = file_manipulate(mode='rt', file_name='filters.txt')

    teste = ['a', 'b', 'c']

    for x in zip(filters, teste):
        print(f'{x[0]}: {x[1]}')

# STOP MARK: CONTINUAR O PRINT DOS FILTROS ACIMA!!

    '''print(f'Pai')

    countries_origin, countries_aquisition, ncm = (line for line in filters)

    
    if input(f'Alterar filtros?')'''
'''


        
            print('Não há filtros de países salvos no sistema.')
            string_temp = ''
            while True:
                chosen_path = input(
                    f'Digite os filtros ou pressione "f" para sair: ')
                if chosen_path not in 'Ff':
                    if string_temp == '':
                        string_temp = chosen_path
                    else:
                        string_temp = string_temp + ',' + chosen_path
                else:
                    break
            cabecalho_final()
            objeto.set_dados(string_temp + '\n', 'at')
            return string_temp.split(',')
        else:
            return objeto.set_path(lista_temp, cor(' Filtros Países ', 'green', '1'))


cabecalho_sec(cor('Módulo Simplificador - Versão: 1.0', 'lblue', '1'))

caminho_raiz = '/home/afdt/Documentos/Projeto Imp/'
caminho_csv_backup = 'Scripts/Config/csv_backup.txt'
caminho_filtros_backup = 'Scripts/Config/filtros_backup.txt'
ncm_list = list()


caminho_csv_escolhido = inicializacao_arquivos(
    caminho_raiz, caminho_csv_backup)
filtro_paises_escolhido = inicializacao_arquivos(
    caminho_raiz, None, caminho_filtros_backup)

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
