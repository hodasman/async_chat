import unittest, time
from client import create_presence, process_ans
from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestCase(unittest.TestCase):
    def test_create_presence(self):
        test_msg = create_presence()
        test_msg[TIME] = 234.235
        self.assertEqual(test_msg, {ACTION: PRESENCE, TIME: 234.235, USER: {ACCOUNT_NAME: "Guest"}})

    def test_answer200(self):
        message = {RESPONSE: 200}
        test_answer = process_ans(message)
        self.assertEqual(test_answer, '200 : OK')

    def test_answer_400(self):
        message = {RESPONSE: 400, ERROR: 'Bad Request'}
        test_answer = process_ans(message)
        self.assertEqual(test_answer, '400 : Bad Request')

    def test_incorrect_msq(self):
        self.assertRaises(Exception, process_ans, {})


if __name__ == '__main__':
    unittest.main()
