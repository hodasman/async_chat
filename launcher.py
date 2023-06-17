"""Программа-лаунчер"""

import subprocess

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen(['python3', 'server.py']))
        PROCESSES.append(subprocess.Popen(['python3', 'client.py', '-n test1']))
        PROCESSES.append(subprocess.Popen(['python3', 'client.py', '-n test2']))
        PROCESSES.append(subprocess.Popen(['python3', 'client.py', '-n test3']))

    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
