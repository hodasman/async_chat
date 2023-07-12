"""Константы"""

# Порт по умолчанию для сетевого ваимодействия
import logging

DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
MESSAGE = 'msg'
TEXT_MESSAGE = 'message'
SENDER = 'from'
DESTINATION = 'to'
EXIT = 'exit'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'


# Прочие ключи, используемые в протоколе
PRESENCE = 'presenc'
RESPONSE = 'response'
ERROR = 'error'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# уровень логирования событий
LOGGING_LEVEL = logging.DEBUG

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO:None
                }
# 400
RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: None
        }

# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}