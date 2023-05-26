from socket import *
import sys
import json
import time
from func import send_msg
from conf import DEFAULT_IP_ADDRESS, DEFAULT_PORT


def create_presence(account_name="Guest"):
    '''
    Функция формирует presence-сообщение для сервера
    :param account_name:
    :return:
    '''
    presence_msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "Yep, I am here!"
        } 
    }

    return json.dumps(presence_msg)


def handler_server_msg(data:bytes):
    '''
    Функция обрабатывает сообщения от сервера и выдает ответ в виде строки
    :param data:
    :return:
    '''
    input = json.loads(data.decode('utf-8'))
    if input['response']:
        if input['response'] == 200:
            return '200:OK'
        if input['response'] == 400:
            return f'400: {input["error"]}'
    raise ValueError


def main():
    '''
    Функция загружает параметры из командной строки адрес и порт. Создает соединение с сервером
    Отправляет presence-сообщение на сервер и принимает ответ от сервера.
    '''
    try:
        server_port = int(sys.argv[2])
        server_ip = sys.argv[1]
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except Exception:
        server_ip = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Значение порта должно быть целым числом от 1024 до 65535')

    s = socket(AF_INET, SOCK_STREAM) # Создать сокет TCP
    s.connect((server_ip, server_port)) # Соединиться с сервером
    presence_msg = create_presence()
    send_msg(s, presence_msg)
    try:
        data = s.recv(640)
        print(handler_server_msg(data))
        s.close()
    except (ValueError, json.JSONDecodeError):  
        print('Принято некорретное сообщение от клиента.')
        s.close()

if __name__ == '__main__':
     main()