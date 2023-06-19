"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
import sys
from ipaddress import ip_address
from task9_1 import host_ping


def host_range_ping(begin_ip_adress: str, count: int):
    """
    Функция принимает на вход начальный IP адрес в формате строки иколичество проверяемых хостов
    :param begin_ip_adress:
    :param count:
    """
    try:
        last_oct = begin_ip_adress.split('.')[3]
        if int(last_oct) + count > 254:
            raise ValueError
    except ValueError as e:
        print(f'Максимальное количество хостов для проверки {254 - int(last_oct)}, вы ввели {count}')
        sys.exit(1)
    except IndexError as e:
        print(f'Не верный формат ip-адреса (XXX.XXX.XXX.XXX)')

    host_list = []
    try:
        for i in range(count):
            host_list.append(str(ip_address(begin_ip_adress ) + i))
    except ValueError as e:
        print(f'Не верный формат ip-адреса {e}')
    return host_ping(host_list)



if __name__ == "__main__":
    host_range_ping('192.168.100.20', 10)

