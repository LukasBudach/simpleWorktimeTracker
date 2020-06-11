from datastructures.Dates import Month

import unittest


class TestMonthObject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._month = Month(month=5, year=2020)

    def test_from_summary_string(self):
        test_month = Month.from_summary_string('May 2020')
        self.assertEqual(self._month, test_month)

    # test conversion to string
    def test_as_string(self):
        self.assertEqual('May 2020', self._month.as_string())

    # test representation of dates object as string
    def test_str(self):
        self.assertEqual('May 2020', str(self._month))

    def test_repr(self):
        self.assertEqual('May 2020', repr(self._month))

    # test the accessor functions for the fields
    def test_month_accessor(self):
        self.assertEqual(5, self._month.month())

    def test_year_accessor(self):
        self.assertEqual(2020, self._month.year())

    # test equal and not equal
    def test_eq(self):
        test_month = Month(6, 2020)
        self.assertTrue(self._month == self._month)
        self.assertFalse(self._month == test_month)

    def test_ne(self):
        test_month = Month(6, 2020)
        self.assertFalse(self._month != self._month)
        self.assertTrue(self._month != test_month)

    def test_eq_invalid_type(self):
        no_month_object = '05.2020'
        with self.assertRaises(AssertionError):
            self._month == no_month_object

    def test_ne_invalid_type(self):
        no_month_object = '05.2020'
        with self.assertRaises(AssertionError):
            self._month != no_month_object

    # test less than and less equal
    def test_lt(self):
        test_month = Month(6, 2020)
        self.assertFalse(self._month < self._month)
        self.assertTrue(self._month < test_month)
        self.assertFalse(test_month < self._month)

    def test_le(self):
        test_month = Month(6, 2020)
        self.assertTrue(self._month <= self._month)
        self.assertTrue(self._month <= test_month)
        self.assertFalse(test_month <= self._month)

    def test_lt_invalid_type(self):
        no_month_object = '06.2020'
        with self.assertRaises(AssertionError):
            self._month < no_month_object

    def test_le_invalid_type(self):
        no_month_object = '06.2020'
        with self.assertRaises(AssertionError):
            self._month <= no_month_object

    # test greater than and greater equal
    def test_gt(self):
        test_month = Month(4, 2020)
        self.assertFalse(self._month > self._month)
        self.assertTrue(self._month > test_month)
        self.assertFalse(test_month > self._month)

    def test_ge(self):
        test_month = Month(4, 2020)
        self.assertTrue(self._month >= self._month)
        self.assertTrue(self._month >= test_month)
        self.assertFalse(test_month >= self._month)

    def test_gt_invalid_type(self):
        no_month_object = '04.2020'
        with self.assertRaises(AssertionError):
            self._month > no_month_object

    def test_ge_invalid_type(self):
        no_month_object = '04.2020'
        with self.assertRaises(AssertionError):
            self._month >= no_month_object


if __name__ == '__main__':
    unittest.main()
