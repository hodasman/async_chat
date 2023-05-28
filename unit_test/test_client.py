import unittest
from client import create_presence, process_ans
from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestCase(unittest.TestCase):
    def test_create_presence(self):
        """
        Тест правильного формирования сообщения
        """
        test_msg = create_presence()
        test_msg[TIME] = 234.235
        self.assertEqual(test_msg, {ACTION: PRESENCE, TIME: 234.235, USER: {ACCOUNT_NAME: "Guest"}})

    def test_answer200(self):
        """Тест функции process_ans на код 200 """
        message = {RESPONSE: 200}
        test_answer = process_ans(message)
        self.assertEqual(test_answer, '200 : OK')

    def test_answer_400(self):
        """Тест функции process_ans на код 400 """
        message = {RESPONSE: 400, ERROR: 'Bad Request'}
        test_answer = process_ans(message)
        self.assertEqual(test_answer, '400 : Bad Request')

    def test_incorrect_msq(self):
        """Тест функции process_ans не корректное или пустое сообщение """
        self.assertRaises(Exception, process_ans, {})


if __name__ == '__main__':
    unittest.main()
