"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
"""

import json

def write_order_to_json(item:str, quantity:str, price:str, buyer:str, date:str):
    '''
    Сохраняет введенные данные в файл orders.json

    :item: наименование товара
    :quantity: количество
    :price: цена
    :buyer: фамилия И.О. покупателя
    :date: дата покупки
    '''

    new_dict = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}

    with open('orders.json', 'r', encoding='utf-8') as f_n:
        dct = json.load(f_n)
        print(f_n.read())
    with open('orders.json', 'w') as f_w:
        orders_list = dct["orders"]
        orders_list.append(new_dict)
        json.dump(dct, f_w, sort_keys=True, indent=4, ensure_ascii=False)
   


write_order_to_json('Груши', '8', '1.99', 'Латушко П.В.', '21.05.2023')
write_order_to_json('Бананы', '4', '1.40', 'Цепкало А. В.', '21.05.2023')
write_order_to_json('pears', '11', '1.30', 'Budanov V.V.', '21.05.2023')


