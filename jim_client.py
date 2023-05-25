from socket import *
import sys
import json
import time

def create_presence(account_name="Guest"):
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


def send_msg(s:socket, msg:str):
    msg_bytes = msg.encode('utf-8')
    s.send(msg_bytes)


server_port = int(sys.argv[2])
server_ip = sys.argv[1]

s = socket(AF_INET, SOCK_STREAM) # Создать сокет TCP
s.connect((server_ip, server_port)) # Соединиться с сервером
presence_msg = create_presence()
send_msg(s, presence_msg)
data = s.recv(1000000)
print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
s.close()