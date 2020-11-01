import unittest
import os
import xlrd
from Scripts.classes_imp import Formatacao, SiscoriData
from Scripts.IO_formats import DIR_XLSX


class TestFormatacao(unittest.TestCase):
    def setUp(self):
        self.text = 'teste'
        self.cor = 'red'
        self.effect = 'bold'
        self.background = 'blue'

    def test_cabecalho_inicio(self):
        teste = Formatacao()
        cabecalho_inicio = teste.cabecalho(text=self.text, option='inicio', size=11)
        expected_value = '===teste==='
        self.assertEqual(cabecalho_inicio, expected_value)

    def test_cabecalho_final(self):
        teste = Formatacao()
        cabecalho_final = teste.cabecalho(text=self.text, option='final', size=11)
        expected_value = '=' * 11 + '\n'
        self.assertEqual(cabecalho_final, expected_value)

    def test_cabecalho_secundario(self):
        teste = Formatacao()
        cabecalho_secundario = teste.cabecalho(text=self.text, option='secundario', size=6)
        expected_value = '\n######\n' + 'teste'.center(6) + '\n######\n\n'
        self.assertEqual(cabecalho_secundario, expected_value)

    def test_color(self):
        teste = Formatacao().color(text=self.text, cor=self.cor, effect=self.effect, background=self.background)
        expected_value = f'\033[1;31;44mteste\033[m'
        self.assertEqual(teste, expected_value)


class TestCsvConverter(unittest.TestCase):
    def setUp(self):
        self.nome_csv = 'teste.csv'
        self.nome_xlsx = 'teste.xlsx'
        self.csv_content = [['ncm_col', 'pa_col', 'pc_col'], ['ncm1', 'pa1', 'pc1'], ['ncm1', 'pa1', 'pc2'],
                            ['ncm2', 'pa1', 'pc1'], ['ncm1', 'pa2', 'pc2']]

    def test_get_csv(self):
        teste = SiscoriData().get_csv(file_name=self.nome_csv, delimiter='@')
        expected_value = [['1', 'a', 'teste1'], ['2', 'b', 'teste2'], ['3', 'c', 'teste3'], ['4', 'd', 'teste4']]
        self.assertEqual(teste, expected_value)

    def test_set_del(self):  # Alterar conforme o test_set_filtro
        _teste = SiscoriData()
        _teste.get_csv(file_name=self.nome_csv, delimiter='@')
        teste = _teste.set_del([0, 1])
        expected_value = [['a'], ['b'], ['c'], ['d']]
        self.assertEqual(teste, expected_value)

    def test_set_filtro(self):
        teste = SiscoriData(backup=self.csv_content, ncm_list=['ncm1'], countries_list=['pa1'], sec_countries_list=['pc1'])
        teste = teste.set_filtro()
        expected_value = [['ncm_col', 'pa_col', 'pc_col'], ['ncm1', 'pa1', 'pc1']]
        self.assertEqual(teste, expected_value)

    def test_set_data(self):
        teste = SiscoriData(bkpsec=self.csv_content)
        teste.set_data_file(file_name=self.nome_xlsx, mode='wt+')

        expected_value = list()

        temp = xlrd.open_workbook(os.path.join(DIR_XLSX, self.nome_xlsx))
        temp_sheet = temp.sheet_by_index(0)

        for row in range(temp_sheet.nrows):
            expected_value.append(temp_sheet.row_values(row))
        self.assertEqual(self.csv_content, expected_value)
