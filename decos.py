import logging
import sys
import inspect
import log.config_server_log
import log.config_client_log


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    """Декоратор"""
    def safe_log(*args, **kwargs):
        """Обертка"""
        result = func(*args, **kwargs)
        LOGGER.debug(f'Функция {func.__name__} с аргументами {args} {kwargs} вызвана из функции '
                     f'{inspect.stack()[1][3]}', stacklevel=2)
        return result
    return safe_log
