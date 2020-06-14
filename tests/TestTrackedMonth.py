from datastructures import *
from TrackedMonth import TrackedMonth

import copy
from datetime import date
from pathlib import Path
import pandas as pd
import unittest
from unittest.mock import patch


class TestTrackedMonth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ref_month = date(2020, 5, 1)
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
        cls._ref_tracked_month = TrackedMonth(cls._ref_data, cls._ref_month)
        cls._ref_empty_tracked_month = TrackedMonth(
            data=pd.DataFrame(columns=['date', 'start', 'end', 'work time', 'running total', 'description']),
            month=cls._ref_month
        )
        cls._ref_month_summary = pd.DataFrame(data={'month': [Month(cls._ref_month.month, cls._ref_month.year)],
                                                    'time done': [Time(12, 30, False)],
                                                    'running total': [Time(0, 0, False)],
                                                    'time required': [Time(31, 0, False)],
                                                    'overtime done': [Time(18, 30, True)],
                                                    'total overtime': [Time(0, 0, False)],
                                                    'hours per week': 7.0})

    def _data_frames_equal(self, reference, other):
        # shapes of data frames are equal
        self.assertEqual(reference.shape, other.shape)
        # contents of data frames are equal
        for col in reference.columns:
            self.assertTrue((reference[col] == other[col]).all())

    def _tracked_months_equal(self, reference, other):
        # data is equal
        self._data_frames_equal(reference._data, other._data)
        # months are the same for both
        self.assertEqual(reference._month, other._month)

    def test_validate_valid_header(self):
        self.assertIsNone(TrackedMonth.validate_header(self._ref_data))

    def test_validate_invalid_header(self):
        invalid_data = self._ref_data.drop(columns=['end'])
        with self.assertRaises(AssertionError):
            TrackedMonth.validate_header(invalid_data)

    def test_from_file(self):
        read_tracked_month = TrackedMonth.from_file(Path('./tests/testdata/valid_reference_month.csv'))
        self._tracked_months_equal(self._ref_tracked_month, read_tracked_month)

    def test_from_date(self):
        date_tracked_month = TrackedMonth.from_date(self._ref_month, Path('./tests/testdata/tmp'))
        self._tracked_months_equal(self._ref_empty_tracked_month, date_tracked_month)
        # add a line and save for the test_from_date_existing test
        date_tracked_month.add_entry(date(2020, 5, 2), Time.from_string('10:00'), Time.from_string('12:30'),
                                     'no description')
        date_tracked_month.save(Path('./tests/testdata/tmp'))

    def test_from_date_existing(self):
        """ Test is run after the :code:`test_from_date` test. That way the :code:`tests/testdata/tmp/2020_05_May.csv`
        file already exists, thus leading to a load from file rather than a new creation for a month.
        """
        # this should load from file
        date_tracked_month = TrackedMonth.from_date(self._ref_month, Path('./tests/testdata/tmp'))
        # create a copy of the empty data frame and add the entry that should have been in the file
        copy_ref_empty = copy.deepcopy(self._ref_empty_tracked_month)
        copy_ref_empty.add_entry(date(2020, 5, 2), Time.from_string('10:00'), Time.from_string('12:30'),
                                 'no description')
        try:
            self._tracked_months_equal(copy_ref_empty, date_tracked_month)
        finally:
            Path('./tests/testdata/tmp/2020_05_May.csv').unlink()

    def test_save(self):
        out_path = Path('./tests/testdata/tmp/2020_05_May.csv')
        self._ref_tracked_month.save(out_path.parent)
        ref_file = open(Path('./tests/testdata/valid_reference_month.csv'), 'rb')
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
        test_tracked_month.add_entry(date(2020, 5, 4), Time.from_string('13:00'), Time.from_string('17:20'), 'desc two')
        self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)

    def test_add_overlapping_entry(self):
        test_tracked_month = copy.deepcopy(self._ref_tracked_month)
        # make sure that the copy and reference are equal before the adding process
        self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)
        # attempt to add, but reject the overlapping entry
        with patch('builtins.input', return_value='y'):
            test_tracked_month.add_entry(date(2020, 5, 4), Time.from_string('12:00'), Time.from_string('14:00'),
                                         'no desc')
        # create a reference tracked month
        ref_data_overlap_added = pd.DataFrame(data={'date': [date(2020, 5, 4), date(2020, 5, 6), date(2020, 5, 10)],
                                                    'start': [Time.from_string('12:00'), Time.from_string('09:25'),
                                                              Time.from_string('17;45')],
                                                    'end': [Time.from_string('14:00'), Time.from_string('13:50'),
                                                            Time.from_string('19:00')],
                                                    'work time': [Time.from_string('02:00'), Time.from_string('04:25'),
                                                                  Time.from_string('01:15')],
                                                    'running total': [Time.from_string('02:00'),
                                                                      Time.from_string('06:25'),
                                                                      Time.from_string('07:40')],
                                                    'description': ['no desc', 'desc three', 'desc four']})
        ref_month_overlap_added = TrackedMonth(data=ref_data_overlap_added, month=self._ref_month)
        self._tracked_months_equal(ref_month_overlap_added, test_tracked_month)

    def test_dont_add_overlapping_entry(self):
        test_tracked_month = copy.deepcopy(self._ref_tracked_month)
        # make sure that the copy and reference are equal before the adding process
        self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)
        # attempt to add, but reject the overlapping entry
        with patch('builtins.input', return_value='n'):
            test_tracked_month.add_entry(date(2020, 5, 4), Time.from_string('12:00'), Time.from_string('14:00'),
                                         'no desc')
        self._tracked_months_equal(self._ref_tracked_month, test_tracked_month)

    def test_get_month_summary_input_hpw(self):
        with patch('builtins.input', return_value='7'):
            created_month_summary = self._ref_tracked_month.get_month_summary()
            self._data_frames_equal(self._ref_month_summary, created_month_summary)

    def test_get_month_summary_with_hpw(self):
        created_month_summary = self._ref_tracked_month.get_month_summary(hours_per_week=7)
        self._data_frames_equal(self._ref_month_summary, created_month_summary)

    def test_month_accessor(self):
        self.assertEqual(Month(self._ref_month.month, self._ref_month.year), self._ref_tracked_month.month())


if __name__ == '__main__':
    unittest.main()
