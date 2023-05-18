'''
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
Unicode и вывести его содержимое.
'''
import chardet

txt = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']

with open('test_file.txt', 'w+') as f:
    f.writelines(txt)
    
with open('test_file.txt', 'rb') as fb:
    txt_bytes = fb.read()
    unicode_format = chardet.detect(txt_bytes)
    print(unicode_format)

with open('test_file.txt', 'r', encoding=unicode_format['encoding']) as fr:
    print(fr.read())



