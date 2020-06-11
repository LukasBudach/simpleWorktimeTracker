from datastructures import Time

import unittest


class TestTimeObject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._str_positive_small = '8:25'
        cls._str_positive_large = '15:50'
        cls._str_positive_huge = '125:40'
        cls._str_negative_small = '-8:25'
        cls._str_negative_large = '-15:50'
        cls._str_negative_huge = '-125:40'

    # test loading from string
    def test_from_string_positive(self):
        time = Time.from_string(self._str_positive_huge)
        self.assertEqual(125, time.hours())
        self.assertEqual(40, time.minutes())
        self.assertTrue(time.is_positive())

    def test_from_string_negative(self):
        time = Time.from_string(self._str_negative_huge)
        self.assertEqual(125, time.hours())
        self.assertEqual(40, time.minutes())
        self.assertTrue(time.is_negative())

    # test whether a correct Time object is calculated when time required is asked for
    def test_time_required_calculation(self):
        time = Time.required_time_calculation(21, 11.5)
        self.assertEqual(34, time.hours())
        self.assertEqual(30, time.minutes())
        self.assertTrue(time.is_positive())

    # test conversion to string
    def test_as_string_small_positive(self):
        time = Time.from_string(self._str_positive_small)
        self.assertEqual('08:25', time.as_string())

    def test_as_string_large_positive(self):
        time = Time.from_string(self._str_positive_large)
        self.assertEqual('15:50', time.as_string())

    def test_as_string_huge_positive(self):
        time = Time.from_string(self._str_positive_huge)
        self.assertEqual('125:40', time.as_string())

    def test_as_string_small_negative(self):
        time = Time.from_string(self._str_negative_small)
        self.assertEqual('-08:25', time.as_string())

    def test_as_string_large_negative(self):
        time = Time.from_string(self._str_negative_large)
        self.assertEqual('-15:50', time.as_string())

    def test_as_string_huge_negative(self):
        time = Time.from_string(self._str_negative_huge)
        self.assertEqual('-125:40', time.as_string())

    # test representation of time object as string
    def test_str_positive(self):
        time = Time.from_string(self._str_positive_large)
        self.assertEqual('15:50', str(time))

    def test_repr_positive(self):
        time = Time.from_string(self._str_positive_large)
        self.assertEqual('15:50', repr(time))

    def test_str_negative(self):
        time = Time.from_string(self._str_negative_large)
        self.assertEqual('-15:50', str(time))

    def test_repr_negative(self):
        time = Time.from_string(self._str_negative_large)
        self.assertEqual('-15:50', repr(time))

    # test the value function
    def test_value_positive(self):
        time = Time.from_string(self._str_positive_small)
        self.assertEqual(505, time.value())

    def test_value_negative(self):
        time = Time.from_string(self._str_negative_huge)
        self.assertEqual(-7540, time.value())

    # test the hashing function
    def test_hash_positive(self):
        time = Time.from_string(self._str_positive_huge)
        self.assertEqual(hash(7540), hash(time))

    def test_hash_negative(self):
        time = Time.from_string(self._str_negative_huge)
        self.assertEqual(hash(-7540), hash(time))

    # test the addition of Time objects
    def test_add_small_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_small)
        res = time_1 + time_2
        self.assertEqual(16, res.hours())
        self.assertEqual(50, res.minutes())
        self.assertTrue(res.is_positive())

    def test_add_large_positives(self):
        time_1 = Time.from_string(self._str_positive_large)
        time_2 = Time.from_string(self._str_positive_large)
        res = time_1 + time_2
        self.assertEqual(31, res.hours())
        self.assertEqual(40, res.minutes())
        self.assertTrue(res.is_positive())

    def test_add_huge_positives(self):
        time_1 = Time.from_string(self._str_positive_huge)
        time_2 = Time.from_string(self._str_positive_huge)
        res = time_1 + time_2
        self.assertEqual(251, res.hours())
        self.assertEqual(20, res.minutes())
        self.assertTrue(res.is_positive())

    def test_add_small_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_small)
        res = time_1 + time_2
        self.assertEqual(16, res.hours())
        self.assertEqual(50, res.minutes())
        self.assertTrue(res.is_negative())

    def test_add_large_negatives(self):
        time_1 = Time.from_string(self._str_negative_large)
        time_2 = Time.from_string(self._str_negative_large)
        res = time_1 + time_2
        self.assertEqual(31, res.hours())
        self.assertEqual(40, res.minutes())
        self.assertTrue(res.is_negative())

    def test_add_huge_negatives(self):
        time_1 = Time.from_string(self._str_negative_huge)
        time_2 = Time.from_string(self._str_negative_huge)
        res = time_1 + time_2
        self.assertEqual(251, res.hours())
        self.assertEqual(20, res.minutes())
        self.assertTrue(res.is_negative())

    def test_add_result_zero(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        res = time_1 + time_2
        self.assertEqual(0, res.hours())
        self.assertEqual(0, res.minutes())
        self.assertTrue(res.is_positive())

    def test_add_result_negative(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_large)
        res = time_1 + time_2
        self.assertEqual(7, res.hours())
        self.assertEqual(25, res.minutes())
        self.assertTrue(res.is_negative())

    def test_add_result_positive(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_positive_huge)
        res = time_1 + time_2
        self.assertEqual(117, res.hours())
        self.assertEqual(15, res.minutes())
        self.assertTrue(res.is_positive())

    def test_add_invalid_type(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 + time_2

    # test the subtraction of Time objects
    def test_sub_positives_result_positive(self):
        time_1 = Time.from_string(self._str_positive_large)
        time_2 = Time.from_string(self._str_positive_small)
        res = time_1 - time_2
        self.assertEqual(7, res.hours())
        self.assertEqual(25, res.minutes())
        self.assertTrue(res.is_positive())

    def test_sub_positives_result_negative(self):
        time_1 = Time.from_string(self._str_positive_large)
        time_2 = Time.from_string(self._str_positive_huge)
        res = time_1 - time_2
        self.assertEqual(109, res.hours())
        self.assertEqual(50, res.minutes())
        self.assertTrue(res.is_negative())

    def test_sub_negatives_result_positive(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_huge)
        res = time_1 - time_2
        self.assertEqual(117, res.hours())
        self.assertEqual(15, res.minutes())
        self.assertTrue(res.is_positive())

    def test_sub_negatives_result_negative(self):
        time_1 = Time.from_string(self._str_negative_large)
        time_2 = Time.from_string(self._str_negative_small)
        res = time_1 - time_2
        self.assertEqual(7, res.hours())
        self.assertEqual(25, res.minutes())
        self.assertTrue(res.is_negative())

    def test_sub_negative_from_positive(self):
        time_1 = Time.from_string(self._str_positive_large)
        time_2 = Time.from_string(self._str_negative_small)
        res = time_1 - time_2
        self.assertEqual(24, res.hours())
        self.assertEqual(15, res.minutes())
        self.assertTrue(res.is_positive())

    def test_sub_positive_from_negative(self):
        time_1 = Time.from_string(self._str_negative_large)
        time_2 = Time.from_string(self._str_positive_huge)
        res = time_1 - time_2
        self.assertEqual(141, res.hours())
        self.assertEqual(30, res.minutes())
        self.assertTrue(res.is_negative())

    def test_sub_invalid_type(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 - time_2

    # test equal and not equal
    def test_eq_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertTrue(time_1 == time_1)
        self.assertFalse(time_1 == time_2)

    def test_ne_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertTrue(time_1 != time_2)
        self.assertFalse(time_1 != time_1)

    def test_eq_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertTrue(time_1 == time_1)
        self.assertFalse(time_1 == time_2)

    def test_ne_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertTrue(time_1 != time_2)
        self.assertFalse(time_1 != time_1)

    def test_eq(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertFalse(time_1 == time_2)

    def test_ne(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertTrue(time_1 != time_2)

    def test_eq_invalid_type(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 == time_2

    def test_ne_invalid_type(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 != time_2

    # test less than and less equal
    def test_lt_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertFalse(time_1 < time_1)
        self.assertTrue(time_1 < time_2)
        self.assertFalse(time_2 < time_1)

    def test_le_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertTrue(time_1 <= time_2)
        self.assertTrue(time_1 <= time_1)
        self.assertFalse(time_2 <= time_1)

    def test_lt_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertFalse(time_1 < time_1)
        self.assertTrue(time_2 < time_1)
        self.assertFalse(time_1 < time_2)

    def test_le_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertFalse(time_1 <= time_2)
        self.assertTrue(time_1 <= time_1)
        self.assertTrue(time_2 <= time_1)

    def test_lt(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertFalse(time_1 < time_2)
        self.assertTrue(time_2 < time_1)

    def test_le(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertFalse(time_1 <= time_2)
        self.assertTrue(time_2 <= time_1)

    def test_lt_invalid_type(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 < time_2

    def test_le_invalid_type(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 <= time_2

    # test greater than and greater equal
    def test_gt_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertFalse(time_1 > time_1)
        self.assertFalse(time_1 > time_2)
        self.assertTrue(time_2 > time_1)

    def test_ge_positives(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_positive_large)
        self.assertFalse(time_1 >= time_2)
        self.assertTrue(time_1 >= time_1)
        self.assertTrue(time_2 >= time_1)

    def test_gt_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertFalse(time_1 > time_1)
        self.assertFalse(time_2 > time_1)
        self.assertTrue(time_1 > time_2)

    def test_ge_negatives(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = Time.from_string(self._str_negative_large)
        self.assertTrue(time_1 >= time_2)
        self.assertTrue(time_1 >= time_1)
        self.assertFalse(time_2 >= time_1)

    def test_gt(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertTrue(time_1 > time_2)
        self.assertFalse(time_2 > time_1)

    def test_ge(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = Time.from_string(self._str_negative_small)
        self.assertTrue(time_1 >= time_2)
        self.assertFalse(time_2 >= time_1)

    def test_gt_invalid_type(self):
        time_1 = Time.from_string(self._str_negative_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 > time_2

    def test_ge_invalid_type(self):
        time_1 = Time.from_string(self._str_positive_small)
        time_2 = 45
        with self.assertRaises(AssertionError):
            time_1 >= time_2


if __name__ == '__main__':
    unittest.main()
