"""Программа-сервер"""
import logging
import socket
import sys
import json
import time
from select import select

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, TEXT_MESSAGE, SENDER, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
import log.config_server_log
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message: dict, message_list: list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    отправляет словарь-ответ для клиента, cобирает все сообщения
    в список

    :param message:
    :param message_list:
    :param client:
    :return:
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return {RESPONSE: 200}

    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and TEXT_MESSAGE in message:
        message_list.append((message[ACCOUNT_NAME], message[TEXT_MESSAGE]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Подключился клиент с адресом {client_address}')
            clients.append(client)
        finally:
            r_clients = []
            w_clients = []
            e_clients = []
            try:
                r_clients, w_clients, e_clients = select(clients, clients, [], 0)
            except OSError:
                pass  # Ничего не делать, если какой-то клиент отключился

        try:
            if r_clients:
                for client_with_message in r_clients:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
        except:
            SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                               f'отключился от сервера.')
            clients.remove(client_with_message)
        if messages and w_clients:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                TEXT_MESSAGE: messages[0][1]
            }
            del messages[0]
            for waiting_client in w_clients:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
