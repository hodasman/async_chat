import argparse
import logging
import socket
import sys
import json
import time
from select import select

from server_database import ServerStorage
from metaclasses import ServerMaker
from descript import Port
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


class Server(metaclass=ServerMaker):
    listen_port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.listen_port = listen_port
        self.listen_address = listen_address
        self.database = database
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
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем, иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, {RESPONSE: 200})
            else:
                response = {
                    RESPONSE: 400,
                    ERROR: 'Пользователь с таким именем уже существует'
                            }
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
            # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and TEXT_MESSAGE in message:
            self.messages.append(message)
            return
            # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            return
            # Иначе отдаём Bad request
        else:
            response = {
                    RESPONSE: 400,
                    ERROR: 'Пользователь с таким именем уже существует'
                            }
            send_message(client, response)
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
    # Создание экземпляра класса базы данных
    database = ServerStorage()
    # Создание экземпляра класса - сервера.
    server = Server(listen_address, listen_port, database)
    server.main_loop()

if __name__ == '__main__':
    main()