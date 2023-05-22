'''
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, 
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью 
параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

import yaml

data = {'10A_class': ['Ivanov', 'Petrov', 'Sidorov', 'Gorbachev', 'Gumelev'],
        'quantity': 5,
        'money_on_curtains': {'Ivanov': '10€', 'Petrov': '15€', 'Sidorov': '1€', 'Gorbachev': '10€', 'Gumelev': '16€'}
        }

with open('file.yaml', 'w') as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode = True)

with open('file.yaml') as f_r:
    content = yaml.load(f_r, Loader=yaml.SafeLoader)
    print(content)