import xlsxwriter
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DIR_CSV = BASE_DIR + '/Plan_CSV'
DIR_XLSX = BASE_DIR + '/Plan_XLSX'
DICT_EXTENSIONS = {
    'xlsx': DIR_XLSX,
    'csv': DIR_CSV,
}


def file_extension(file_name):
    extension = file_name.split('.')[-1].lower()
    file_path = DICT_EXTENSIONS.get(extension)
    return extension, file_path


def xlsx_manipulate(data, file, mode):
    # if 'w' in mode:

    excel = xlsxwriter.Workbook(file)
    plan1 = excel.add_worksheet()
    lin = 0
    col = 0

    for row in data:
        for i in row:
            plan1.write(lin, col, i)
            if col >= 6:
                col = 0
            else:
                col += 1
        lin += 1
    excel.close()

    #else:
        # implementar código para realizar leitura de arquivos xlsx.
        #pass


def change_file(func):

    def open_file(*args, **kwargs):

        file_name = kwargs.get('file_name')
        mode = kwargs.get('mode')
        extension, file_path = file_extension(file_name)
        file = os.path.join(file_path, file_name)

        data = args[0].bkpsec
        xlsx_manipulate(data, file, mode)

        '''if extension == 'xlsx':
        
        
        elif extension == 'csv':
            file = open(os.path.join(file_path, file_name), mode)
            a = func
            file.close()
'''
    return open_file
