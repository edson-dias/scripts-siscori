from src.utils import file_manipulate
from src.decorators import header


class SiscoriData:

    def __init__(self, backup=None, bkpsec=None, **kwargs):
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

    @header
    def get_csv(self, **kwargs):
        kwargs['data'] = self.backup
        kwargs['mode'] = 'rt'
        file_manipulate(**kwargs)
        return self.backup

    @header
    def set_del(self, colunas_del=None):
        if not colunas_del:
            colunas_del = [0, 0, 1, 1, 2, 3, 3,
                           3, 4, 4, 4, 4, 4, 6, 6, 7, 7, 7]

        try:
            for row in self.backup:
                for col in colunas_del:
                    del row[col]
                for j in range(len(row)):
                    row[j] = row[j].strip()
        except IndexError:
            # Criar função que contabilize quantas colunas tem na planilha e retorne um valor, sugerindo a correção.
            print('Número inválido para remoção de colunas!')

        return self.backup

    @header
    def set_filtro(self):

        self.bkpsec = [row_csv for row_csv in self.backup
                       for ncm_number in self.ncm_list if ncm_number in row_csv[0]
                       for country in self.countries_list if country in row_csv[1]
                       for row in self.sec_countries_list if row in row_csv[2]]

        self.bkpsec.insert(0, self.backup[0])
        del self.backup
        return self.bkpsec

    @header
    def set_data_file(self, **kwargs):

        if 'data' not in kwargs.keys():
            kwargs['data'] = self.bkpsec

        file_manipulate(**kwargs)


class DbIo:
    pass
