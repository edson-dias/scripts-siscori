from time import sleep
from xlrd import *
import xlsxwriter


def cabecalho_sec(texto=''):
    """
    Cabeçalho inicial do programa
    :param texto: título do cabeçalho
    :return: void
    """
    print('\n')
    print('#' * 60 + '\n')
    print(texto.center(67))
    print('\n' + '#' * 60 + '\n')
    sleep(1)
    print('\n')


def cor(string_col, string_cor, string_tip='0', back=''):
    """
    Retorna a cor selecionada.
    :param string_col: String à ser colorida.
    :param string_cor: Cor escolhida.
    :param string_tip: Efeito na string - 0=none; 1=bold; 4=underline ; 7=negative
    :param back: 40=branco; 41=vermelho; 42=verde; 43=amarelo; 44=azul; 45=roxo; 46=lblue; 47=cinza.
    :return: Cor escolhida
    """

    if back is not '':
        back = ';' + back

    if string_cor.lower == 'white':
        return f'\033[{string_tip};30{back}m{string_col}\033[m'

    elif string_cor.lower() == 'red':
        return f'\033[{string_tip};31{back}m{string_col}\033[m'

    elif string_cor.lower() == 'green':
        return f'\033[{string_tip};32{back}m{string_col}\033[m'

    elif string_cor.lower() == 'yellow':
        return f'\033[{string_tip};33{back}m{string_col}\033[m'

    elif string_cor.lower() == 'blue':
        return f'\033[{string_tip};34{back}m{string_col}\033[m'

    elif string_cor.lower() == 'purple':
        return f'\033[{string_tip};35{back}m{string_col}\033[m'

    elif string_cor.lower() == 'lblue':
        return f'\033[{string_tip};36{back}m{string_col}\033[m'

    elif string_cor.lower() == 'grey':
        return f'\033[{string_tip};37{back}m{string_col}\033[m'


def cabecalho_inicio(texto=''):
    """
    Parte superior dos cabeçalhos intermediários.
    :param texto: string
    :return: void
    """
    print('{:=^70}'.format(texto))


def cabecalho_final():
    print('=' * 60 + '\n')


class Simplificador(object):
    """
    Classe simplificadora. Possui como função ler arquivo csv, deletar col, filtrar linhas e grava arq xlsx."""

    def __init__(self, nome, caminho, **kwargs):
        """
        Construtor da classe.
        :param nome: Nome do arquivo .csv
        :param caminho: Caminho do arquivo .csv
        :param ncm: lista com ncm a ser filtrado.
        :param pa: lista com filtro de países.
        :param pc: lista com filtro de países.
        :param quant: void.
        :param backup: lista com os dados encontrados.
        :param bkpsec: lista secundária com dados encontrados."""

        self.nome = nome
        self.caminho = caminho
        self.ncm = kwargs.get('ncm')
        self.pa = kwargs.get('pa')
        self.pc = kwargs.get('pc')
        self.quant = kwargs.get('quant')
        self.backup = list()
        self.bkpsec = list()

    def get_csv(self):
        """
        Extrai os dados de um .csv para uma lista.
        :return: void
        """

        import csv

        with open(self.caminho + self.nome, encoding='latin-1') as self.nome:
            csv_temp = csv.reader(self.nome, delimiter='@')
            csv.field_size_limit(100000000)

            for row in csv_temp:
                self.backup.append(row)

    def set_del(self):
        """
        Deleta determinadas colunas do arquivo .csv
        :return: void """

        colunas_del = [0, 0, 1, 1, 2, 3, 3, 3, 4, 4, 4, 4, 4, 6, 6, 7, 7, 7]
        indices = [0, 1, 2, 3, 4, 5, 6]  # melhorar com a sintaxe [:]

        for row in self.backup:
            for i in colunas_del:
                del row[i]
            for j in indices:
                row[j] = row[j].strip()

    def set_filtro(self):
        """
        Filtra as listas usando os atributos da classe.
        :return: void
        """

        if self.ncm is None:
            self.ncm = []

        if self.pa is None:
            self.pa = []

        if self.pc is None:
            self.pc = []

        if self.bkpsec is None:
            self.bkpsec = []

        self.bkpsec.append(self.backup[0])

        for row in self.backup:
            for i in self.ncm:
                if i in row[0]:
                    for lin in self.pa:
                        if lin in row[1].lower():
                            for line in self.pc:
                                if line in row[2].lower():
                                    self.bkpsec.append(row)

    def create_xlsm(self, caminho_xlsx, nome_xlsx):
        """
        Cria arquivo xlsl.
        :param caminho_xlsx: caminho onde o arquivo será salvo
        :param nome_xlsx: Nome do arquivo.
        :return: void.
        """

        lin = 0
        col = 0

        excel = xlsxwriter.Workbook(caminho_xlsx + nome_xlsx + '.xlsx')
        plan1 = excel.add_worksheet()

        for row in self.bkpsec:
            for i in row:
                plan1.write(lin, col, i)
                if col >= 6:
                    col = 0
                else:
                    col += 1
            lin += 1
        excel.close()


class DataPath(object):
    """
    Classe para tratamento dos dados
    """

    def __init__(self, caminho_raiz='/home', caminho_arq='/home'):
        """
        Construtor da classe DataPath.
        :param caminho_raiz: caminho raiz do sistema.
        :param caminho_arq: caminho dos arquivos de configuração
        """

        self.caminho_raiz = caminho_raiz
        self.caminho_arq = caminho_arq

    def file_check(self):
        """
        Checa se uma planilha existe ou não.
        :return: Boolean
        """

        try:
            a = open(self.caminho_raiz + self.caminho_arq, 'rt')
            a.close()
        except FileNotFoundError:
            return False
        else:
            return True

    def criar_arquivo(self):
        """
        Cria arquivo .txt no diretório informado.
        :return: void
        """

        try:
            a = open(self.caminho_raiz + self.caminho_arq, 'wt+')
            a.close()
        except FileExistsError:
            print('Houve um erro com a criação do arquivo!')
        else:
            pass

    def get_dados(self):
        """
        Extrai os dados do arquivo .txt
        :return: list()
        """
        arquivo_temp = None
        lista = list()

        try:
            arquivo_temp = open(self.caminho_raiz + self.caminho_arq, 'rt')
        except FileExistsError:
            print('Houve um erro com o arquivo!')
        else:
            for lin in arquivo_temp:
                temp = lin.replace('\n', '').split(',')
                lista.append(temp)
        finally:
            arquivo_temp.close()
            return lista

    def set_path(self, lista_temp, texto, flag=0):
        """
        Realiza a escolha dos caminhos/filtros de acordo com o valor digitado no terminal
        :param lista_temp: list()
        :param texto: string
        :param flag: int para indicar qual texto deve ser mostrado (0 = simplificador / 1 = buscador)
        :return: list() ou string
        """

        cabecalho_inicio(texto)

        for i in range(0, len(lista_temp)):
            print(f'{lista_temp[i]}'.ljust(57) + '[' + cor(f'{i + 1}', 'red', '1') + ']')

        if flag == 0:
            print(f'Add novos caminhos de arquivos CSV'.ljust(57) + '[' + cor('0', 'red', '1') + ']')
            print(f'Add novos filtros de países.'.ljust(56) + '[' + cor('-1', 'red', '1') + ']' + '\n')
        elif flag == 1:
            print(f'Add novos caminhos de arquivos xlsx: '.ljust(57) + '[' + cor('0', 'red', '1') + ']')

        a = int(input(cor('Escolha uma das opções acima: ', 'red', '1')))

        cabecalho_final()

        if a == 1:
            return lista_temp[0]

        elif a == 2:
            return lista_temp[1]

        elif a == 3:
            return lista_temp[2]

        elif a == 0:
            temp = self.caminho_raiz + 'Data/' + input(f'Complemente o caminho "{self.caminho_raiz}Data/": ')

            if len(lista_temp) > 2:

                while len(lista_temp) > 2:
                    del lista_temp[2]

                self.set_dados(temp + '\n', 'wt+')

                for row in lista_temp:
                    self.set_dados(row + '\n', 'at')
            else:

                self.set_dados(temp + '\n', 'at')

            return temp

        elif a == -1:
            string_temp = string_temp2 = ''
            while True:
                temp = input(f'Digite os países a serem filtrados ou pressione "f" para sair: ')
                if temp not in 'Ff':
                    if string_temp == '':
                        string_temp = temp
                    else:
                        string_temp = string_temp + ',' + temp
                else:
                    break

            while len(lista_temp) > 2:
                del lista_temp[2]

            self.set_dados(string_temp + '\n', 'wt+')

            for row in lista_temp:
                for piece in row:
                    if string_temp2 == '':
                        string_temp2 = piece
                    else:
                        string_temp2 = string_temp2 + ',' + piece

                self.set_dados(string_temp2 + '\n', 'at')
                string_temp2 = ''

            return string_temp.split(',')

    def set_dados(self, temp, modo_de_escrita='wt+'):

        """ Insere os dados no arquivo de backup.
        Cuidado ao utilizar wt+ no modo_de_escrita. Sobrescreve o arquivo backup.

        :param temp: String a ser guardada no arquivo backup.
        :param modo_de_escrita: wt+, rt, at, rt+.
        :return: void. """

        try:
            a = open(self.caminho_raiz + self.caminho_arq, modo_de_escrita)

        except FileNotFoundError:
            print('Houve um erro na abertura do arquivo.')

        else:
            try:
                a.write(temp)

            except IOError:
                print('Houve um erro ao inserir os dados')

            else:
                a.close()


class Buscador(DataPath):
    """
    Compara os arquivos simplificados com as keywords do banco de dados.
    """

    def __init__(self, caminho_r='', path_arq='', nome_arq=''):

        """
        Construtor da classe buscadora.
        :param caminho_r: string com o caminho de instalação do sistema.
        :param path_arq: string com o caminho para o arquivo a ser aberto.
        :param nome_arq: string contendo o nome do arquivo a ser aberto.

        """

        super().__init__()
        self.caminho_r = caminho_r
        self.path_arq = path_arq
        self.nome_arq = nome_arq

    def comparador_bd(self, lista_siscori=None, lista_bd=None, lista_limbo=None):

        """
        Compara as keywords da lista banco de dados com as descrições da lista do sistema.
        :param lista_siscori: lista contendo os dados da planilha siscori.
        :param lista_bd: lista contendo os dados do banco de dados.
        :param lista_limbo: lista contendo os dados do banco de dados limbo
        :return:
        """

        flag = 0

        if lista_siscori is None:
            lista_siscori = list()

        if lista_bd is None:
            lista_bd = list()

        if lista_limbo is None:
            lista_limbo = list()

        # Possível problema: linha 59 - A string do siscori pode conter a keyword do BD, porém ser de outra marca.
        # Solucionar com duas keywords e um and?
        for linha in lista_siscori:
            for row in lista_bd:
                if row[7] in linha[3]:
                    row.append(
                        str(linha[4]) + '/' + str(linha[5]) + '/' + self.nome_arq[4:])
                    flag = 1
            if flag == 0:
                lista_limbo.append(linha)
            flag = 0

    def set_infos(self, lista=None, nome=None, caminho_arq=None):

        """
        Cria uma nova planilha e armazena os dados das listas nesta planilha.
        :param lista: lista a ser inserida no arquivo xlsx.
        :param nome: Nome do arquivo xlsx.
        :param caminho_arq: Caminho do arquivo xlsx.
        :return: void.
        Caso não seja explicitado as varíaveis na chamada do método, serão considerados os valores da instância.
        """

        if nome is None:
            nome = self.nome_arq
        if caminho_arq is None:
            caminho_arq = self.path_arq
        if lista is None:
            lista = list()

        lin = 0

        excel = xlsxwriter.Workbook(self.caminho_r + caminho_arq + nome + '.xlsx')
        plan1 = excel.add_worksheet()

        for row in lista:
            for col in range(0, len(row)):
                plan1.write(lin, col, row[col])
            lin += 1
        excel.close()

    def get_xlsx(self):

        lista_temp = list()

        temp = open_workbook(self.caminho_r + self.path_arq + self.nome_arq + '.xlsx')
        temp_sheet = temp.sheet_by_index(0)

        for row in range(temp_sheet.nrows):
            lista_temp.append(temp_sheet.row_values(row))

        return lista_temp
