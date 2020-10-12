import unittest
from Scripts.classes_imp import Formatacao, CsvConverter


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
        self.nome = 'teste.csv'

    def test_get_csv(self):
        teste = CsvConverter().get_csv(self.nome)
        expected_value = [['1,a'], ['2,b'], ['3,c'], ['4,d'], ['5,e']]
        self.assertEqual(teste, expected_value)
