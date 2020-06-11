from datastructures import *
from TrackedMonth import TrackedMonth

import copy
from datetime import date
from pathlib import Path
import pandas as pd
import unittest


class TestTrackedMonth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ref_data = pd.DataFrame(data={'date': [date(2020, 5, 4), date(2020, 5, 4),
                                                    date(2020, 5, 6), date(2020, 5, 10)],
                                           'start': [Time.from_string('10:00'), Time.from_string('13:00'),
                                                     Time.from_string('09:25'), Time.from_string('17;45')],
                                           'end': [Time.from_string('12:30'), Time.from_string('17:20'),
                                                   Time.from_string('13:50'), Time.from_string('19:00')],
                                           'work time': [Time.from_string('02:30'), Time.from_string('04:20'),
                                                         Time.from_string('04:25'), Time.from_string('01:15')],
                                           'running total': [Time.from_string('02:30'), Time.from_string('06:50'),
                                                             Time.from_string('11:15'), Time.from_string('12:30')],
                                           'description': ['desc one', 'desc two', 'desc three', 'desc four']})
        cls._ref_tracked_month = TrackedMonth(cls._ref_data, date(2020, 5, 1))

    def _tracked_months_equal(self, reference, other):
        # shapes of internal data are equal
        self.assertEqual(reference._data.shape, other._data.shape)
        # contents of internal data are equal
        for col in reference._data.columns:
            self.assertTrue((reference._data[col] == other._data[col]).all())
        # months are the same for both
        self.assertEqual(reference._month, other._month)

    def test_validate_valid_header(self):
        self.assertIsNone(TrackedMonth.validate_header(self._ref_data))

    def test_validate_invalid_header(self):
        invalid_data = self._ref_data.drop(columns=['end'])
        with self.assertRaises(AssertionError):
            TrackedMonth.validate_header(invalid_data)

    def test_from_file(self):
        read_tracked_month = TrackedMonth.from_file(Path('./testdata/valid_reference_month.csv'))
        self._tracked_months_equal(self._ref_tracked_month, read_tracked_month)

    def test_save(self):
        out_path = Path('./testdata/tmp/2020_05_May.csv')
        self._ref_tracked_month.save(out_path.parent)
        ref_file = open(Path('./testdata/valid_reference_month.csv'), 'rb')
        out_file = open(out_path, 'rb')
        try:
            self.assertEqual(ref_file.readlines(), out_file.readlines())
        finally:
            ref_file.close()
            out_file.close()
            out_path.unlink()

    def test_sort(self):
        # get copy of tracked month with some rows swapped
        swapped_tracked_month = copy.deepcopy(self._ref_tracked_month)
        copy_row_0 = swapped_tracked_month._data.iloc[0].copy()
        swapped_tracked_month._data.iloc[0] = swapped_tracked_month._data.iloc[3].copy()
        swapped_tracked_month._data.iloc[3] = copy_row_0
        # make sure that the swapped and reference tracked month objects are now indeed different
        with self.assertRaises(AssertionError):
            self._tracked_months_equal(self._ref_tracked_month, swapped_tracked_month)
        # sort and test whether the two objects are now equal
        swapped_tracked_month.sort()
        self._tracked_months_equal(self._ref_tracked_month, swapped_tracked_month)

    def test_recalculate_running_total(self):
        # get copy of tracked month with an invalid running total
        no_rt_tracked_month = copy.deepcopy(self._ref_tracked_month)
        no_rt_tracked_month._data['running total'] = pd.Series([Time(i, i, False) for i in range(4)])
        # make sure that the tracked month object without running total and reference are now indeed different
        with self.assertRaises(AssertionError):
            self._tracked_months_equal(self._ref_tracked_month, no_rt_tracked_month)
        # sort and test whether the two objects are now equal
        no_rt_tracked_month.recalculate_running_total()
        self._tracked_months_equal(self._ref_tracked_month, no_rt_tracked_month)

    def test_overlapping_entry_exists(self):
        # define date and time that are overlapping with some existing entries (in this case both on May 4th)
        overlap_date = date(2020, 5, 4)
        overlap_start = Time(12, 0, False)
        overlap_end = Time(14, 0, False)
        # test whether the overlap is detected
        overlap_exists, overlapping_entries = self._ref_tracked_month.overlapping_entry_exists(overlap_date,
                                                                                               overlap_start,
                                                                                               overlap_end)
        self.assertTrue(overlap_exists)
        self.assertTrue((pd.Series([True, True, False, False]) == overlapping_entries).all())

    def test_no_overlapping_entry_exists(self):
        # define date and time that are not overlapping with some existing entries (in this case both on May 4th)
        overlap_date = date(2020, 5, 4)  # technically the date does overlap, so keep that name
        no_overlap_start = Time(12, 30, False)
        no_overlap_end = Time(13, 0, False)
        # test whether the overlap is detected
        overlap_exists, overlapping_entries = self._ref_tracked_month.overlapping_entry_exists(overlap_date,
                                                                                               no_overlap_start,
                                                                                               no_overlap_end)
        self.assertFalse(overlap_exists)
        self.assertFalse(overlapping_entries.all())

    def test_add_entry(self):
        # get copy of tracked month and remove one entry in the beginning
        test_tracked_month = copy.deepcopy(self._ref_tracked_month)
        test_tracked_month._data.drop(labels=1, axis=0, inplace=True)
        test_tracked_month._data = test_tracked_month._data.reindex(axis=0)
        # make sure that the tracked month object without that one entry and reference are now indeed different
        with self.assertRaises(AssertionError):
            self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)
        # sort and test whether the two objects are now equal
        test_tracked_month.add_entry(date(2020, 5, 4), '13:00', '17:20', 'desc two')
        self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)


if __name__ == '__main__':
    unittest.main()
