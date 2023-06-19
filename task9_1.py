"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
 Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
  В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
  («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции
  ip_address().
"""


import ipaddress
import subprocess


def host_ping(lst_ip_adress: list, timeout=1.0, count=1):
    result_dict = {'Reachable':[], 'Unreachable':[]}
    for host in lst_ip_adress:
        try:
            adress = ipaddress.ip_address(host)
        except ValueError:
            adress = host
        proc = subprocess.Popen(['ping', f'{adress}', f'-t {timeout}', f'-c {count}'], shell=False,
                                stdout=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            print(f'{host} - узел доступен')
            result_dict['Reachable'].append(host)
        else:
            print(f'{host} - узел не доступен')
            result_dict['Unreachable'].append(host)
    return result_dict


if __name__ == "__main__":
    lst = ['192.168.100.1', 'yandex.ru', '2.2.2.2', '192.168.0.55']
    print(host_ping(lst, 2.0, 1))