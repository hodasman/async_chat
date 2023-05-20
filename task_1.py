'''
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и
содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые 
представление в формат Unicode и также проверить тип и содержимое переменных.
'''

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'

list_word = [word_1, word_2, word_3]

for word in list_word:
    print(word, type(word))

unicode_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
unicode_2 = '\u0441\u043e\u043a\u0435\u0442'
unicode_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

unicode_list = [unicode_1, unicode_2, unicode_3]

for unicode in unicode_list:
    print(unicode, type(unicode))

 