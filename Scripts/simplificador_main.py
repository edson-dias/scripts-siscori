#!/usr/bin/env python3

"""
Script main realiza as configurações para simplificar o arquivo .csv e criar o arquivo .xlsx.
Autores: Edson, Henrique.
Versão: 1.0
"""

from classes_imp import *
import sys


def inicializacao_arquivos(caminho_r, caminho_arq_csv=None, caminho_arq_filtros=None):
    """
    Inicializa os arquivos necessários para determinar os atributos das classes.

    :param caminho_r: caminho raiz do sistema.
    :param caminho_arq_csv: caminho do arquivo path.txt
    :param caminho_arq_filtros: caminho do arquivo  filtros.txt
    :return: retorna chamadas dos métodos set_path ou lista com os valores escolhidos pelo usuário.

    Melhorar este módulo adaptando-o como parte da classe DataPath!!
    """

    lista_temp2 = list()
    if caminho_arq_csv is not None:
        objeto = DataPath(caminho_r, caminho_arq_csv)

        if not objeto.file_check():
            objeto.criar_arquivo()

        lista_temp = objeto.get_dados()
        for row in lista_temp:
            lista_temp2.append(row[0])

        if not lista_temp2:
            cabecalho_inicio(cor(' Arquivos de Configuração: Path ', 'yellow', '1'))
            print('Não há caminhos para arquivos CSV salvos no sistema.')
            chosen_path = caminho_r + input(f'Complemente o caminho "{caminho_r}": \n')
            objeto.set_dados(chosen_path + '\n', 'at')
            cabecalho_final()
            return chosen_path
        else:
            return objeto.set_path(lista_temp2, cor(' Caminho Arquivo CSV ', 'yellow', '1'))

    elif caminho_arq_filtros is not None:
        objeto = DataPath(caminho_r, caminho_arq_filtros)

        if not objeto.file_check():
            objeto.criar_arquivo()

        lista_temp = objeto.get_dados()

        if not lista_temp:
            cabecalho_inicio(cor(' Arquivos de Configuração: Filtros PA/PC ', 'yellow', '1'))
            print('Não há filtros de países salvos no sistema.')
            string_temp = ''
            while True:
                chosen_path = input(f'Digite os filtros ou pressione "f" para sair: ')
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


caminho_csv_escolhido = inicializacao_arquivos(caminho_raiz, caminho_csv_backup)
filtro_paises_escolhido = inicializacao_arquivos(caminho_raiz, None, caminho_filtros_backup)

cabecalho_inicio(cor(' Arquivo CSV - XLSX ', 'blue', '1'))
nome_csv = 'CAPI' + input('Digite o nome do arquivo sem "CAPI" e sem ".csv": ') + '.CSV'
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
importacoes = Simplificador(nome_csv, caminho_csv_escolhido, ncm=ncm_list, pa=filtro_paises_escolhido, pc=filtro_paises_escolhido)
print('Iniciando a leitura do arquivo .csv ...')
importacoes.get_csv()
importacoes.set_del()
print('Filtrando arquivo csv...')
importacoes.set_filtro()
print('Criando arquivo xlsm...')
importacoes.create_xlsm(caminho_csv_escolhido, nome_xlsx)
print('Finalizado!')
cabecalho_final()
