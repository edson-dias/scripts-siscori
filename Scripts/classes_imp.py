from Scripts.IO_formats import file_manipulate


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


class SiscoriData(Formatacao):

    def __init__(self, backup=None, bkpsec=None, **kwargs):
        super(SiscoriData, self).__init__()
        if backup is None:
            self.backup = list()
        else:
            self.backup = backup

        if bkpsec is None:
            self.bkpsec = list()
        else:
            self.bkpsec = bkpsec

        self.ncm_list = kwargs.get('ncm_list')
        self.countries_list = kwargs.get('countries_list')
        self.sec_countries_list = kwargs.get('sec_countries_list')
        self.quant = kwargs.get('quant')
        # alterar para self.attr = [k=v for k,v in kwargs.items()]

    def get_csv(self, **kwargs):
        kwargs['data'] = self.backup
        kwargs['mode'] = 'rt'
        file_manipulate(**kwargs)
        return self.backup

    def set_del(self, colunas_del=None):
        if not colunas_del:
            colunas_del = [0, 0, 1, 1, 2, 3, 3, 3, 4, 4, 4, 4, 4, 6, 6, 7, 7, 7]

        try:
            for row in self.backup:
                for col in colunas_del:
                    del row[col]
                for j in range(len(row)):
                    row[j] = row[j].strip()
        except IndexError:
            # Criar função que contabilize quantas colunas tem na planilha e retorne um valor, sugerindo a correção.
            pass

        return self.backup

    def set_filtro(self):

        self.bkpsec = [row_csv for row_csv in self.backup
                       for ncm_number in self.ncm_list if ncm_number in row_csv[0]
                       for country in self.countries_list if country in row_csv[1]
                       for row in self.sec_countries_list if row in row_csv[2]]

        self.bkpsec.insert(0, self.backup[0])
        del self.backup
        return self.bkpsec

    def set_data_file(self, **kwargs):

        if 'data' not in kwargs.keys():
            kwargs['data'] = self.bkpsec

        file_manipulate(**kwargs)

