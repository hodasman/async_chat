"""Программа-сервер"""
import logging
import socket
import sys
import json
import time
from select import select

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, TEXT_MESSAGE, SENDER, DEFAULT_IP_ADDRESS, DESTINATION
from common.utils import get_message, send_message
import log.config_server_log
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message: dict, message_list: list, client, clients: list, names: dict):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    отправляет словарь-ответ для клиента, добавляет все сообщения клиентов
    в список message_list, добавляет сокеты всех клиентов в список clients,
    добавляет в словарь names пары имя клиента - сокет

    :param message:
    :param message_list:
    :param client:
    :param clients:
    :param names:
    :return:
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME]:
        if message[USER][ACCOUNT_NAME] in names.keys():
            send_message(client, {
                RESPONSE: 400,
                ERROR: 'Пользователь с таким именем уже существует'
            })
            clients.remove(client)
            client.close()
        else:
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, {RESPONSE: 200})
        return

    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and TEXT_MESSAGE in message and DESTINATION in message \
            and SENDER in message:
        message_list.append(message)
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(
            f'В качастве порта может быть указано только число в диапазоне от 1024 до 65535. Указан {listen_port}')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS

    except IndexError:
        SERVER_LOGGER.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)
    transport.settimeout(1)

    clients = []  # Список всех подключившихся клиентов
    messages = []  # Список сообщений от клиентов

    # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    names = dict()

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Подключился клиент с адресом {client_address}')
            clients.append(client)

        r_clients = []
        w_clients = []
        e_clients = []
        try:
            if clients:
                r_clients, w_clients, e_clients = select(clients, clients, [], 0)
        except OSError:
            pass  # Ничего не делать, если какой-то клиент отключился

        if r_clients:
            for client_with_message in r_clients:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message, clients,
                                           names)
                except Exception as e:

                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.{e}')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, w_clients)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
