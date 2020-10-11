from xlrd import *
import xlsxwriter
import os


BASE_DIR = os.path.dirname(__file__)


class Formatacao:

    def __init__(self):
        self.text = ''
        self.cor = ''
        self.effect = ''
        self.background = ''

    def cabecalho(self, **kwargs):

        option = kwargs.get('option')
        line_size = kwargs.get('size')
        self.text = kwargs.get('text')

        if line_size is None:
            line_size = 70

        if option == 'secundario':  # Estudar formas de centralizar e ajustar itens independente do tamanha da tela.
            return '\n' + '#' * line_size + '\n' + self.text.center(line_size) + '\n' + '#' * line_size + '\n' + '\n'

        elif option == 'inicio':
            return self.text.center(line_size, '=')

        elif option == 'final':
            return '=' * line_size + '\n'

    def _get_attr_dict(self):

        dict_colors = {
            'white': '30',
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'purple': '35',
            'lblue': '36',
            'grey': '37',
        }

        dict_effects = {
            'none': '0',
            'bold': '1',
            'underline': '4',
            'negative': '7',
        }

        dict_backgrounds = {
            'white': '40',
            'red': '41',
            'green': '42',
            'yellow': '43',
            'blue': '44',
            'purple': '45',
            'lblue': '46',
            'grey': '47',
        }

        self.cor = dict_colors.get(self.cor)
        self.effect = dict_effects.get(self.effect)
        self.background = dict_backgrounds.get(self.background)

    def color(self, **kwargs):

        self.text = kwargs.get('text')
        self.cor = kwargs.get('cor')
        self.effect = kwargs.get('effect')
        self.background = kwargs.get('background')

        self._get_attr_dict()

        if self.cor is None:
            self.cor = ''
        else:
            self.cor = ';' + self.cor

        if self.effect is None:
            self.effect = ''

        if self.background is None:
            self.background = ''
        else:
            self.background = ';' + self.background

        return f'\033[{self.effect}{self.cor}{self.background}m{self.text}\033[m'


class Simplificador(Formatacao):
    """
    Classe simplificadora. Possui como função ler arquivo csv, deletar col, filtrar linhas e grava arq xlsx."""

    def __init__(self, nome, **kwargs):
        super(Simplificador, self).__init__()
        self.nome = nome
        self.backup = list()
        self.bkpsec = list()

        self.ncm = kwargs.get('ncm')
        self.pa = kwargs.get('pa')
        self.pc = kwargs.get('pc')
        self.quant = kwargs.get('quant')

    def get_csv(self):
        """
        Extrai os dados de um .csv para uma lista.
        :return: void
        """

        import csv

        with open(os.path.join(BASE_DIR, ''), encoding='latin-1') as self.nome:
            csv_temp = csv.reader(self.nome, delimiter='@')
            csv.field_size_limit(100000000)

            for row in csv_temp:
                self.backup.append(row)

    def set_del(self, **kwargs):
        """
        Deleta determinadas colunas do arquivo .csv
        :return: void """

        colunas_del = kwargs.get('colunas_del')
        indices = kwargs.get('indices')

        if not colunas_del:
            colunas_del = [0, 0, 1, 1, 2, 3, 3, 3, 4, 4, 4, 4, 4, 6, 6, 7, 7, 7]

        if not indices:
            indices = [0, 1, 2, 3, 4, 5, 6]

        for row in self.backup:
            for i in colunas_del:
                del row[i]
            for j in indices:
                row[j] = row[j].strip()

    def set_filtro(self):           # Pesquisar algum método de comparação, mais eficiente do que o abaixo.
        """
        Filtra as listas usando os atributos da classe.
        :return: void
        """

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


class DataPath:
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