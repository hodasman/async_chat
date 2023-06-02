import logging
import logging.handlers
import os
import sys

from common.variables import LOGGING_LEVEL

# создаем форматтер
SERVER_FORMATTER = logging.Formatter("%(levelname)-10s %(asctime)s %(filename)s %(message)s")

# Обработчик для вывода сообщений в поток
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.ERROR)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs/server_logs/server.log')

# Обработчик для вывода сообщений в файл
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='midnight')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

# создаем регистратор с именем 'server'
SERVER_LOGGER = logging.getLogger('server')
SERVER_LOGGER.addHandler(FILE_HANDLER)
SERVER_LOGGER.addHandler(STREAM_HANDLER)
SERVER_LOGGER.setLevel(LOGGING_LEVEL)  # Уровень важности для регистратора задается в файле variables

if __name__ == '__main__':
    SERVER_LOGGER.critical('Критическая ошибка')
    SERVER_LOGGER.error('Ошибка')
    SERVER_LOGGER.debug('Отладочная информация')
    SERVER_LOGGER.info('Информационное сообщение')
