import csv
import os
import xlsxwriter


def _xlsx_writing(_data, _file, **kwargs):
    excel = xlsxwriter.Workbook(_file)
    plan1 = excel.add_worksheet()
    lin = 0
    col = 0

    for row in _data:
        for i in row:
            plan1.write(lin, col, i)
            if col >= (len(_data[0]) - 1):
                col = 0
            else:
                col += 1
        lin += 1
    excel.close()


def _txt_writing(_data, _file, **kwargs):
    mode = kwargs.get('mode')

    file = open(_file, mode)
    for row in _data:
        file.write(row)
    file.close()


def _csv_reading(_data, _file, **kwargs):

    delimiter = kwargs.get('delimiter', '@')

    with open(os.path.join(DIR_CSV, _file), encoding='latin-1') as _file:
        csv_temp = csv.reader(_file, delimiter=delimiter)
        csv.field_size_limit(100000000)

        for row in csv_temp:
            _data.append(row)


def _txt_reading(_data, _file, **kwargs):
    mode = kwargs.get('mode', 'rt')
    lista = []

    try:
        temp = open(_file, mode)
    except FileExistsError:
        print('Houve um erro com o arquivo!')
    else:
        [lista.append(lin.replace("\n", "")) for lin in temp]
        temp.close()
        return lista


def _create_file(file):
    try:
        temp = open(file, 'wt+')
    except FileExistsError:
        print('Houve um erro com a criação do arquivo!')
    else:
        temp.close()


def _get_attr_dict(**kwargs):

    cor = kwargs.get('cor')
    effect = kwargs.get('effect')
    background = kwargs.get('background')

    color_number = DICT_COLORS.get(cor, '')
    effect_number = DICT_EFFECTS.get(effect, '')
    background_number = DICT_BACKGROUNDS.get(background, '')

    return color_number, effect_number, background_number


def color(**kwargs):
    cor, effect, background = _get_attr_dict(**kwargs)
    text = kwargs.get('text', '')

    return f'\033[{effect}{cor}{background}m{text}\033[m'


def is_there_file(file):
    try:
        temp = open(file, 'rt')
    except FileNotFoundError:
        _create_file(file)
    else:
        temp.close()
        return True


def file_extension(file_name):
    extension = file_name.split('.')[-1].lower()
    file_path = DICT_EXTENSIONS.get(extension)
    return extension, file_path


def file_manipulate(**kwargs):

    _data = kwargs.get('data', list())
    mode = kwargs.get('mode', 'rt')
    file_name = kwargs.get('file_name')

    extension, file_path = file_extension(file_name)

    if 'file_path' in kwargs.keys():
        file_path = kwargs.get('file_path')

    _file = os.path.join(file_path, file_name)

    if 'w' in mode:  # or a ??
        DICT_FUNCTIONS_EXTENSIONS.get('w-' + extension)(_data, _file, **kwargs)

    elif 'r' in mode:
        return DICT_FUNCTIONS_EXTENSIONS.get('r-' + extension)(_data, _file, **kwargs)

'''
def choose_path():
    paths = []

    print('Escolha uma ou mais das opções abaixo e tecle "S" para sair.\nTecle "T" para escolher todas as opçoes. \n')
    [print('[' + str(LIST_PATHS.index(itens) + 1) + '] - ' + str(itens))
     for itens in LIST_PATHS]

    while True:
        choice = input('Pasta Escolhida: ')

        if choice in 'Ss':
            break
        else:
            if choice in 'Tt':
                paths = LIST_PATHS
                break

            else:
                try:
                    LIST_PATHS[int(choice) - 1]
                except IndexError:
                    print('Opção Inexistente!')
                else:
                    paths.append(LIST_PATHS[int(choice) - 1])
    return paths

'''

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DIR_CSV = BASE_DIR + '/Plan_CSV'
DIR_XLSX = BASE_DIR + '/Plan_XLSX'
DIR_LOGS = BASE_DIR + '/Logs'


DICT_FILTERS = {
    '1': ['Origin', 'China, Hong Kong, Taiwan, Coreia'],
    '2': ['Acquisition', 'China, Hong Kong, Taiwan, Coreia'],
    '3': ['NCM', '3919, 3926, 7326, 8529, 8531, 8535, 8536, 9107, 9405'],
    '4': ['Months', 'Jan, Fev, Mar, Abr, Mai, Jun, Jul, Ago, Set, Out, Nov, Dez'],
    '5': ['Year', '2019, 2020']
}

DICT_FUNCTIONS_EXTENSIONS = {
    'w-xlsx': _xlsx_writing,
    'w-txt': _txt_writing,
    'r-csv': _csv_reading,
    'r-txt': _txt_reading,
}

DICT_EXTENSIONS = {
    'xlsx': DIR_XLSX,
    'csv': DIR_CSV,
    'txt': DIR_LOGS,
}

DICT_COLORS = {
    'white': ';30',
    'red': ';31',
    'green': ';32',
    'yellow': ';33',
    'blue': ';34',
    'purple': ';35',
    'lblue': ';36',
    'grey': ';37',
}

DICT_EFFECTS = {
    'none': '0',
    'bold': '1',
    'underline': '4',
    'negative': '7',
}

DICT_BACKGROUNDS = {
    'white': ';40',
    'red': ';41',
    'green': ';42',
    'yellow': ';43',
    'blue': ';44',
    'purple': ';45',
    'lblue': ';46',
    'grey': ';47',
}

MONTHS_CONVERSION = {
    'Jan': '01',
    'Fev': '02',
    'Mar': '03',
    'Abr': '04',
    'Mai': '05',
    'Jun': '06',
    'Jul': '07',
    'Ago': '08',
    'Set': '09',
    'Out': '10',
    'Nov': '11',
    'Dez': '12',
}
