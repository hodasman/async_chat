from socket import *
import time
import sys
import json
from func import send_msg
from conf import DEFAULT_PORT


def handler_client_msg(data:bytes):
    input = json.loads(data.decode('utf-8'))
    if input["action"] and input["time"] and input["user"] \
          and input["user"]['account_name']:
        return {
            'response': 200
        }
    else:
        return {
            'response': 400,
            'error': 'Bad request'
        }


def main():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if port < 1024 or port > 65535:
                raise ValueError
    except IndexError:
         print('После параметра -p нужно указать номер порта')
    except ValueError:
         print("Значение порта должно быть целым числом от 1024 до 65535")

    try:
        if '-a' in sys.argv:
            ip = sys.argv[sys.argv.index('-a') + 1]
        else:
             ip = ''
    except IndexError:
        print('После параметра -a укажите адрес который будет слушать сервер')

    s = socket(AF_INET, SOCK_STREAM)   # Создает сокет TCP
    s.bind((ip, port))                 # Присваивает порт 8888
    s.listen(5)                        # Переходит в режим ожидания запросов;

    while True:
        client, addr = s.accept()
        try:
            data = client.recv(640)
            print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ',
            addr)
            msg = json.dumps(handler_client_msg(data)) 
            send_msg(client, msg)
            client.close()
        except (ValueError, json.JSONDecodeError):
                print('Принято некорретное сообщение от клиента.')
                client.close()


if __name__ == '__main__':
     main()