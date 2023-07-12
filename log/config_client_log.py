import logging
import os
import sys
from Acync_chat.common.variables import LOGGING_LEVEL

#Создаем форматтер для сообщений
CLIENT_FORMATTER = logging.Formatter("%(asctime)-25s %(levelname)-10s %(module)s %(message)s")

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
LOGGER = logging.getLogger('client')
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')