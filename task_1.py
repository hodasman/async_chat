"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv, chardet, re


headers_list = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def get_data(headers_list:list, *args:str):
    '''
    Функция принимает в качестве аргументов список заголовков, значения которых необходимо извлечь из текстовых файлов, адреса которых передаются следующими аргументами. Возвращает функция главный список с найдеными значениями.

    :headers_list: Список заголовков в строковом формате из четырех элементов
    :args: адреса текстовых файлов из которых необходимо парсить занчения заголовков, указываются через запятую
    :return: список списков с найденными значениями в каждом файле
    '''
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    
    for arg in args:
        with open(arg, 'rb') as fb:
            txt_bytes = fb.read()
            unicode_format = chardet.detect(txt_bytes)

        with open(arg, 'r', encoding=unicode_format['encoding']) as f_n:
            for line in f_n:
                if re.match(headers_list[0], line):
                    _prod = re.search(r'\s{2}.+$', line)
                    os_prod_list.append(_prod.group(0).strip())
                elif re.match(headers_list[1], line):
                    _name = re.search(r'\s{2}.+$', line)
                    os_name_list.append(_name.group(0).strip())
                elif re.match(headers_list[2], line):
                    _code = re.search(r'\s{2}.+$', line)
                    os_code_list.append(_code.group(0).strip())
                elif re.match(headers_list[3], line):
                    _type = re.search(r'\s{2}.+$', line)
                    os_type_list.append(_type.group(0).strip())
     
    list_tuple = list(zip(os_prod_list, os_name_list, os_code_list, os_type_list))
    main_data = list(map(list, list_tuple))
    main_data.insert(0, headers_list)
    return main_data


def write_to_csv(path_csv:str, headers_list:list, *args:str):
    '''
    Функция записывает данные которые возвращает функция get_data в файл csv

    :path_csv: Путь куда будет сохранен отчет в формате csv
    :headers_list: Список заголовков в строковом формате из четырех элементов
    :args: адреса текстовых файлов из которых необходимо парсить занчения заголовков, указываются через запятую
    :return: список списков с найденными значениями в каждом файле
    '''
    data = get_data(headers_list, *args)
    with open(path_csv, 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        f_n_writer.writerows(data)


if __name__ == "__main__":
    write_to_csv('report.csv', headers_list, 'info_1.txt', 'info_2.txt', 'info_3.txt')