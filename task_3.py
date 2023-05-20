'''
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''

lst_word = ['attribute', 'класс', 'функция', 'type']


for word in lst_word:
    try:
        print(bytes(word, 'ascii'))
    except UnicodeEncodeError:
        print(f'слово "{word}" не возможно записать в байтовом виде')
