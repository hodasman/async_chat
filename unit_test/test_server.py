import unittest
import time

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from server import process_client_message


class TestCase(unittest.TestCase):
    """Тестирование функции process_client_message
    """

    dct_400 = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_no_action(self):
        """Нет ключа action"""
        message = {TIME: time.time(), USER: {ACCOUNT_NAME: "Guest"}}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, self.dct_400)

    def test_no_presence(self):
        """Знaчение ключа action не presence"""
        message = {ACTION: 'authentication', TIME: time.time(), USER: {ACCOUNT_NAME: "Guest"}}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, self.dct_400)

    def test_no_time(self):
        """Нет ключа time"""
        message = {ACTION: PRESENCE, USER: {ACCOUNT_NAME: "Guest"}}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, self.dct_400)

    def test_no_user(self):
        """Нет ключа user"""
        message = {ACTION: PRESENCE, TIME: time.time()}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, self.dct_400)

    def test_unknown_user(self):
        """Неизвестный пользователь"""
        message = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: "User"}}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, self.dct_400)

    def test_correct_msg(self):
        """Корректное сообщение"""
        message = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: "Guest"}}
        test_answer = process_client_message(message)
        self.assertEqual(test_answer, {RESPONSE: 200})


if __name__ == '__main__':
    unittest.main()
