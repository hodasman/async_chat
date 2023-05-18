'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового 
представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
'''

lst_words = ['разработка', 'администрирование', 'protocol', 'standard']

lst_bytes = [word.encode('utf-8') for word in lst_words]
print(lst_bytes)

for byte in lst_bytes:
    print(byte.decode('utf-8'))