import logging
import os
import sys
from common.variables import LOGGING_LEVEL

#Создаем форматтер для сообщений
CLIENT_FORMATTER = logging.Formatter("%(levelname)-10s %(asctime)s %(filename)s %(message)s")

# Создаем обработчик для вывода сообщений в поток
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.ERROR)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs/client_logs/client.log')

# Создаем обработчик для вывода сообщений в файл
FILE_HANDLER = logging.FileHandler(PATH, encoding='utf8')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)

# Создаем регистратор и подключаем к нему обработчики
CLIENT_LOGGER = logging.getLogger('client')
CLIENT_LOGGER.addHandler(FILE_HANDLER)
CLIENT_LOGGER.addHandler(STREAM_HANDLER)
CLIENT_LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    CLIENT_LOGGER.critical('Критическая ошибка')
    CLIENT_LOGGER.error('Ошибка')
    CLIENT_LOGGER.debug('Отладочная информация')
    CLIENT_LOGGER.info('Информационное сообщение')