import hashlib
import unittest

import jdatetime
from django.utils.datetime_safe import new_date
from jdatetime import datetime
from openpyxl.styles.builtins import percent

from exeptions import InvalidDateError
from utils import hash_password, str_to_datetime, calculate_time_span, apply_discount


class TestUtils(unittest.TestCase):
    def test_hash_password_returns_string(self):
        hashed_password = hash_password("<PASSWORD>")
        self.assertIsInstance(hashed_password, str)
    def test_hash_password_is_deterministic(self):
        hashed_password_1 = hash_password("<PASSWORD>")
        hashed_password_2 = hash_password("<PASSWORD>")

        self.assertEqual(hashed_password_1, hashed_password_2)
    def test_hash_password_result_is_correct(self):
        hashed_password = hash_password("<PASSWORD>")
        expected_hash = hashlib.sha256("<PASSWORD>".encode('utf8')).hexdigest()

        self.assertEqual(hashed_password, expected_hash)

    def test_str_to_datetime_returns_datetime_for_valid_formats(self):
        format_1 = "1400-01-01"
        format_2 = "1400-1-1"
        self.assertIsInstance(str_to_datetime(format_1), jdatetime.datetime)
        self.assertIsInstance(str_to_datetime(format_2), jdatetime.datetime)
    def test_str_to_date_raise_error_for_invalid_input(self):
        input_none = None
        input_string = "birthday"
        input_invalid_1 = "1400-13-1"
        input_invalid_2 = "1400-121-1"

        with self.assertRaises(InvalidDateError):
            str_to_datetime(input_string)
        with self.assertRaises(InvalidDateError):
            str_to_datetime(input_invalid_1)
        with self.assertRaises(InvalidDateError):
            str_to_datetime(input_invalid_2)
        with self.assertRaises(InvalidDateError):
            str_to_datetime(input_none)

    def test_calculate_time_span_returns_correct_type(self):
        new_date = jdatetime.datetime.now() + jdatetime.timedelta(days=20)
        time_span = calculate_time_span(jdatetime.datetime.now() , new_date)

        self.assertIsInstance(time_span, jdatetime.timedelta)
    def test_calculate_time_span_raises_exception(self):
        incorrect_type = "1400-10-2"
        self.assertRaises(TypeError, calculate_time_span, incorrect_type)

    def test_apply_discount_returns_correct(self):
        price = 100
        twenty_percent = 20
        zero_percent = 0
        hundred_percent = 100

        self.assertEqual(apply_discount(price , twenty_percent) , 80)
        self.assertEqual(apply_discount(price , zero_percent) , price)
        self.assertEqual(apply_discount(price , hundred_percent) , 0)
