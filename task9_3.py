"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
 Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
  (использовать модуль tabulate).
"""
from task9_2 import host_range_ping
from tabulate import tabulate


def host_range_ping_tab():
    beginin_ip_adr = input('Введите значение начального ip-адреса: ')
    count_adress = input('Введите количество проверяемых хостов начиная от начального: ')
    print(tabulate(host_range_ping(beginin_ip_adr, int(count_adress)), headers='keys', tablefmt='pipe'))


if __name__ == '__main__':
    host_range_ping_tab()