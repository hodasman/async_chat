import logging
import sys

logger = logging.getLogger('server')


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {value}. '
                f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
            sys.exit(1)
        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, name):
        self.my_attr = name