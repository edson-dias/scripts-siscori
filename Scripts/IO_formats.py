import csv
import os
import xlsxwriter

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DIR_CSV = BASE_DIR + '/Plan_CSV'
DIR_XLSX = BASE_DIR + '/Plan_XLSX'

DICT_EXTENSIONS = {
    'xlsx': DIR_XLSX,
    'csv': DIR_CSV,
}


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


DICT_FUNCTIONS_EXTENSIONS = {
    'w-xlsx': _xlsx_writing,
    'w-txt': _txt_writing,
    'r-csv': _csv_reading,
}


def file_extension(file_name):
    extension = file_name.split('.')[-1].lower()
    file_path = DICT_EXTENSIONS.get(extension)
    return extension, file_path


def file_manipulate(**kwargs):

    _data = kwargs.get('data')
    mode = kwargs.get('mode')
    file_name = kwargs.get('file_name')

    extension, file_path = file_extension(file_name)
    _file = os.path.join(file_path, file_name)

    if 'w' in mode:  # or a ??
        DICT_FUNCTIONS_EXTENSIONS.get('w-' + extension)(_data, _file, **kwargs)

    elif 'r' in mode:
        return DICT_FUNCTIONS_EXTENSIONS.get('r-' + extension)(_data, _file, **kwargs)
