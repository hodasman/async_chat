"""Программа-клиент"""
import logging
import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import log.config_client_log

CLIENT_LOGGER = logging.getLogger('client')


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


def main():
    """Загружаем параметы коммандной строки"""
    # client.py 192.168.1.2 8079
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.info(f'Запущен клиент с параметрами порт:{server_port} адрес:{server_address}')
    except ValueError:
        CLIENT_LOGGER.critical(f'В качестве порта может быть указано только число в диапазоне от 1024 до 65535. вы указали {server_port}')
        sys.exit(1)

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
    except ConnectionRefusedError:
        CLIENT_LOGGER.error(f'Не удалось подключиться к серверу {server_address}:{server_port}')


if __name__ == '__main__':
    main()
