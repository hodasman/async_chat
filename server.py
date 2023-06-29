import argparse
import configparser
import logging
import socket
import sys
import json
import threading
import time
from select import select

from server_database import ServerStorage
from metaclasses import ServerMaker
from descript import Port
from common.variables import *
from common.utils import get_message, send_message
import log.config_server_log
from decos import log


# Флаг что был подключён новый пользователь, нужен чтобы не мучать BD
# постоянными запросами на обновление
new_connection = False
conflag_lock = threading.Lock()

SERVER_LOGGER = logging.getLogger('server')


# Парсер аргументов коммандной строки.
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Server(threading.Thread, metaclass=ServerMaker):
    listen_port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.listen_port = listen_port
        self.listen_address = listen_address
        self.database = database
        self.clients = []  # Список всех подключившихся клиентов
        self.messages = []  # Список сообщений от клиентов
        self.names = dict()  # Словарь, содержащий имена пользователей и соответствующие им сокеты.
        super().__init__()

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
        global new_connection

        #Если сообщение о присутствии
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем, иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
            # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and TEXT_MESSAGE in message and self.names[message[SENDER]] == client:
            self.messages.append(message)
            self.database.process_message(message[SENDER], message[DESTINATION])
            return
            # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.database.user_logout(message[ACCOUNT_NAME])
            SERVER_LOGGER.info(
                f'Клиент {message[ACCOUNT_NAME]} корректно отключился от сервера.')
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            with conflag_lock:
                new_connection = True
            return

            # Если это запрос контакт-листа
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                 self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            send_message(client, response)

        # Если это добавление контакта
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, RESPONSE_200)

        # Если это удаление контакта
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, RESPONSE_200)

        # Если это запрос известных пользователей
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            send_message(client, response)
        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
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

    def run(self):
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
                        for name in self.names:
                            if self.names[name] == client_with_message:
                                self.database.user_logout(name)
                                del self.names[name]
                                break
                        self.clients.remove(client_with_message)

            for i in self.messages:
                try:
                    self.process_message(i, w_clients)
                except Exception:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    self.clients.remove(self.names[i[DESTINATION]])
                    self.database.user_logout(i[DESTINATION])
                    del self.names[i[DESTINATION]]
            self.messages.clear()

def main():

    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    listen_address, listen_port = arg_parser()
    # Создание экземпляра класса базы данных
    database = ServerStorage()
    # Создание экземпляра класса - сервера.
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

if __name__ == '__main__':
    main()