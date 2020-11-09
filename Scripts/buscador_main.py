#!/usr/bin/env/ python3

from classes_imp import *

caminho_raiz = '/home/afdt/Documentos/Projeto Imp/'
caminho_bd_sucesso = 'BD/Sucesso/'
caminho_bd_limbo = 'BD/Limbo/'
caminho_siscori_backup = 'Scripts/Config/siscori_backup.txt'

cabecalho_sec(cor('Módulo Buscador - Versão: 1.0', 'lblue', '1'))


lista_temp = list()
lista_temp2 = list()

objeto = DataPath(caminho_raiz, caminho_siscori_backup)

if not objeto.file_check():
    objeto.criar_arquivo()

lista_temp = objeto.get_dados()
for row in lista_temp:
    lista_temp2.append(row[0])

if not lista_temp2:
    print('Não há caminhos para arquivos xlsx salvos no sistema.')
    chosen_path = caminho_raiz + input(f'Complemente o caminho "{caminho_raiz}": \n')
    objeto.set_dados(chosen_path + '\n', 'at')
else:
    chosen_path = objeto.set_path(lista_temp2, cor(' Caminho Arquivo Siscori ', 'yellow', '1'), 1)

cabecalho_inicio(cor(' Nome Arq. Siscori ', 'green', '1'))

nome_siscori = input('Digite o nome do arquivo siscori: ')

cabecalho_final()

cabecalho_inicio(cor(' Processos ', 'purple', '1'))

print('Iniciando extração dos dados...')

obj_siscori = Buscador(chosen_path, nome_siscori)
obj_bd = Buscador(caminho_raiz, caminho_bd_sucesso, 'BD_Sucesso')
obj_limbo = Buscador(caminho_raiz, caminho_bd_limbo, 'BD_Limbo')

lista_siscori = obj_siscori.get_xlsx()
lista_bd = obj_bd.get_xlsx()
lista_limbo = obj_limbo.get_xlsx()

print('Buscando keywords...')

obj_siscori.comparador_bd(lista_siscori, lista_bd, lista_limbo)

print('Gravando dados...')

obj_bd.set_infos()
obj_bd.set_infos(lista_limbo, 'BD_Limbo', caminho_bd_limbo)

print('Processos executados com sucesso!')

cabecalho_final()
