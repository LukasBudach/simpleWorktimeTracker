from io import StringIO
from datastructures import Time
from utils.cmd_input_utils import *

from datetime import date
import unittest
from unittest.mock import patch


class TestCmpInputUtils(unittest.TestCase):
    def testIsLastCharSpace(self):
        self.assertTrue(is_last_char_space('Last char space '))
        self.assertFalse(is_last_char_space('Last char not space'))

    def test_make_last_char_space(self):
        self.assertEqual('Last char space ', make_last_char_space('Last char space '))
        self.assertEqual('Last char space ', make_last_char_space('Last char space'))

    def test_format_binary_question(self):
        self.assertEqual('Question? (y/n) ', format_binary_question('Question?'))
        self.assertEqual('Question? (y/n) ', format_binary_question('Question? '))
        self.assertEqual('Question? (y/n) ', format_binary_question('Question? (y/n)'))
        self.assertEqual('Question? (y/n) ', format_binary_question('Question? (y/n) '))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_binary_question_input_valid_yes(self, mock_print):
        with patch('builtins.input', return_value='y'):
            self.assertTrue(binary_question_input('Question?'))
        with patch('builtins.input', return_value='Y'):
            self.assertTrue(binary_question_input('Question?'))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_binary_question_input_valid_no(self, mock_print):
        with patch('builtins.input', return_value='n'):
            self.assertFalse(binary_question_input('Question?'))
        with patch('builtins.input', return_value='N'):
            self.assertFalse(binary_question_input('Question?'))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_binary_question_input_invalid(self, mock_print):
        with patch('builtins.input', return_value='x'):
            with self.assertRaises(Exception) as ex:
                binary_question_input('Question?')
            self.assertEqual('Detected invalid input.', str(ex.exception))

    def test_format_time_input(self):
        self.assertEqual('Time please. (hh:mm) ', format_time_input('Time please.'))
        self.assertEqual('Time please. (hh:mm) ', format_time_input('Time please. '))
        self.assertEqual('Time please. (hh:mm) ', format_time_input('Time please. (hh:mm)'))
        self.assertEqual('Time please. (hh:mm) ', format_time_input('Time please. (hh:mm) '))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_time_input_valid(self, mock_print):
        with patch('builtins.input', return_value='6:12'):
            self.assertEqual(Time(6, 12, False), time_input('Time please.'))
        with patch('builtins.input', return_value='13:42'):
            self.assertEqual(Time(13, 42, False), time_input('Time please.'))
        with patch('builtins.input', return_value='-2:34'):
            self.assertEqual(Time(2, 34, True), time_input('Time please.'))
        with patch('builtins.input', return_value='-21:16'):
            self.assertEqual(Time(21, 16, True), time_input('Time please.'))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_time_input_invalid(self, mock_print):
        with patch('builtins.input', return_value='x'):
            with self.assertRaises(Exception) as ex:
                time_input('Time please.')
            self.assertEqual('Detected invalid input.', str(ex.exception))

    def test_format_date_input(self):
        self.assertEqual('Date please. (dd.mm.yyyy) ', format_date_input('Date please.'))
        self.assertEqual('Date please. (dd.mm.yyyy) ', format_date_input('Date please. '))
        self.assertEqual('Date please. (dd.mm.yyyy) ', format_date_input('Date please. (dd.mm.yyyy)'))
        self.assertEqual('Date please. (dd.mm.yyyy) ', format_date_input('Date please. (dd.mm.yyyy) '))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_date_input_valid(self, mock_print):
        with patch('builtins.input', return_value='04.05.2020'):
            self.assertEqual(date(2020, 5, 4), date_input('Date please.'))
        with patch('builtins.input', return_value='04.05.2020'):
            self.assertEqual(date(2020, 5, 4), date_input('Date please.', empty_for_today=True))
        with patch('builtins.input', return_value=''):
            self.assertEqual(date.today(), date_input('Date please.', empty_for_today=True))

    @patch('builtins.print', side_effect=Exception('Detected invalid input.'))
    def test_date_input_invalid(self, mock_print):
        # test invalid input
        with patch('builtins.input', return_value='x'):
            with self.assertRaises(Exception) as ex:
                date_input('Date please.')
            self.assertEqual('Detected invalid input.', str(ex.exception))
        # test invalid input while allowing empty
        with patch('builtins.input', return_value='x'):
            with self.assertRaises(Exception) as ex:
                date_input('Date please.', empty_for_today=True)
            self.assertEqual('Detected invalid input.', str(ex.exception))
        # test invalid empty input
        with patch('builtins.input', return_value=''):
            with self.assertRaises(Exception) as ex:
                date_input('Date please.')
            self.assertEqual('Detected invalid input.', str(ex.exception))


if __name__ == '__main__':
    unittest.main()
