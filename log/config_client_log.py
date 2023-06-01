import logging
import sys

CLIENT_LOGGER = logging.getLogger('client')
CLIENT_FORMATTER = logging.Formatter("%(levelname)-10s %(asctime)s %(filename)s %(message)s")

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.ERROR)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)


PATH = './logs/client_logs/client.log'
FILE_HANDLER = logging.FileHandler(PATH, encoding='utf8')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)
CLIENT_LOGGER.addHandler(FILE_HANDLER)
CLIENT_LOGGER.addHandler(STREAM_HANDLER)
CLIENT_LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    CLIENT_LOGGER.critical('Критическая ошибка')
    CLIENT_LOGGER.error('Ошибка')
    CLIENT_LOGGER.debug('Отладочная информация')
    CLIENT_LOGGER.info('Информационное сообщение')