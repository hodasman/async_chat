"""Программа-клиент"""
import logging
import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, TEXT_MESSAGE, SENDER
from common.utils import get_message, send_message
import log.config_client_log
from decos import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


@log
def process_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError

@log
def create_message(sock, account_name='Guest'):
    text = input('Введите сообщение:')
    if text == 'exit':
        sock.close()
        CLIENT_LOGGER.info(f'Клиент {sock.getpeername()} вышел из чата')
        sys.exit(0)
    new_message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        TEXT_MESSAGE: text
    }
    return new_message


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and TEXT_MESSAGE in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[TEXT_MESSAGE]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[TEXT_MESSAGE]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


def main():
    """Загружаем параметы коммандной строки"""
    # client.py 192.168.1.2 8079
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        client_mode = sys.argv[3]
        if server_port < 1024 or server_port > 65535:
            CLIENT_LOGGER.critical(
                f'В качестве порта может быть указано только число в диапазоне'
                f' от 1024 до 65535. вы указали {server_port}')
            raise ValueError

        if client_mode not in ('listen', 'write'):
            CLIENT_LOGGER.critical(
                f'Указан не верный режим работы, допустимые значения:'
                f' listen и write. вы указали {client_mode}')
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        client_mode = 'listen'

    except ValueError:
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с параметрами порт:{server_port} адрес:{server_address}'
                       f'статус: {client_mode}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)

        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.debug(f'Принят ответ от сервера: {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать сообщение сервера.')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.error(f'Не удалось подключиться к серверу {server_address}:{server_port}')
        sys.exit(1)

    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'write':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'write':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
