from socket import *
import time
import sys
import json




port = int(sys.argv[sys.argv.index('-p') + 1])
ip = sys.argv[sys.argv.index('-a') + 1]

s = socket(AF_INET, SOCK_STREAM)   # Создает сокет TCP
s.bind((ip, port))                 # Присваивает порт 8888
s.listen(5)                        # Переходит в режим ожидания запросов;

while True:
    client, addr = s.accept()
    data = client.recv(1000000)
    print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ',
    addr)
    msg = 'Привет, клиент' 
    client.send(msg.encode('utf-8')) 
    client.close()