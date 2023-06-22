import argparse
import logging
import socket
import sys
import json
import time
from select import select

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, TEXT_MESSAGE, SENDER, DEFAULT_IP_ADDRESS, DESTINATION, EXIT
from common.utils import get_message, send_message
import log.config_server_log
from decos import log

SERVER_LOGGER = logging.getLogger('server')


# Парсер аргументов коммандной строки.
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Server():
    def __init__(self, listen_address, listen_port):
        self.listen_port = listen_port
        self.listen_address = listen_address
        self.clients = []  # Список всех подключившихся клиентов
        self.messages = []  # Список сообщений от клиентов
        self.names = dict()  # Словарь, содержащий имена пользователей и соответствующие им сокеты.

    def init_socket(self):
        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.listen_port} , адрес с которого принимаются '
            f'подключения: {self.listen_address}.')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(1)
        self.sock = transport
        self.sock.listen()

    def process_client_message(self, message, client):
        #Если сообщение о присутствии
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME]:
            if message[USER][ACCOUNT_NAME] in self.names.keys():
                send_message(client, {
                    RESPONSE: 400,
                    ERROR: 'Пользователь с таким именем уже существует'
                })
                self.clients.remove(client)
                client.close()
            else:
                #Если пользователя нет в словаре names то добавляем
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, {RESPONSE: 200})
            return
        # Если обычное сообщение
        elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
                and TEXT_MESSAGE in message and DESTINATION in message \
                and SENDER in message:
            self.messages.append(message)
            return
            # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.clients.remove(self.names[ACCOUNT_NAME])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return
        else:
            send_message(client, {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            })
            return

    def process_message(self, message, listen_socks):
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            SERVER_LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    def main_loop(self):
        # Инициализация Сокета
        self.init_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Подключился клиент с адресом {client_address}')
                self.clients.append(client)

            r_clients = []
            w_clients = []
            e_clients = []
            try:
                if self.clients:
                    r_clients, w_clients, e_clients = select(self.clients, self.clients, [], 0)
            except OSError:
                pass  # Ничего не делать, если какой-то клиент отключился

            if r_clients:
                for client_with_message in r_clients:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except Exception as e:

                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.{e}')
                        self.clients.remove(client_with_message)

            for i in self.messages:
                try:
                    self.process_message(i, w_clients)
                except Exception:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    self.clients.remove(self.names[i[DESTINATION]])
                    del self.names[i[DESTINATION]]
            self.messages.clear()

def main():
    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    listen_address, listen_port = arg_parser()

    # Создание экземпляра класса - сервера.
    server = Server(listen_address, listen_port)
    server.main_loop()

if __name__ == '__main__':
    main()