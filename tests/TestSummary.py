from datastructures import *
from Summary import Summary
from TrackedMonth import TrackedMonth

import copy
import numpy as np
from datetime import date
from pathlib import Path
import pandas as pd
import unittest
from unittest.mock import patch


class TestSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ref_data = pd.DataFrame(data={'month': [Month(2, 2020), Month(3, 2020), Month(4, 2020)],
                                           'time done': [Time.from_string('10:30'), Time.from_string('9:45'),
                                                         Time.from_string('12:40')],
                                           'running total': [Time.from_string('10:30'), Time.from_string('20:15'),
                                                             Time.from_string('32:55')],
                                           'time required': [Time.from_string('07:15'), Time.from_string('07:45'),
                                                             Time.from_string('30:00')],
                                           'overtime done': [Time.from_string('03:15'), Time.from_string('02:00'),
                                                             Time.from_string('-17:20')],
                                           'total overtime': [Time.from_string('03:15'), Time.from_string('05:15'),
                                                              Time.from_string('12:05')],
                                           'hours per week': [1.75, 1.75, 7.0]})
        cls._ref_summary = Summary(data=cls._ref_data, summary_file=Path('./tests/testdata/valid_reference_summary.csv'))
        cls._ref_summary.save()

    def _data_frames_equal(self, reference, other):
        # shapes of data frames are equal
        self.assertEqual(reference.shape, other.shape)
        # contents of data frames are equal
        for col in reference.columns:
            self.assertTrue((reference[col] == other[col]).all())

    def test_validate_valid_header(self):
        self.assertIsNone(Summary.validate_header(self._ref_data))

    def test_validate_invalid_header(self):
        invalid_data = self._ref_data.drop(columns=['overtime done'])
        with self.assertRaises(AssertionError):
            Summary.validate_header(invalid_data)

    def test_from_file(self):
        read_summary = Summary.from_file(Path('./tests/testdata/valid_reference_summary.csv'))
        self._data_frames_equal(self._ref_summary._data, read_summary._data)

    def test_sort(self):
        # get copy of the reference summary with some rows swapped
        swapped_summary = copy.deepcopy(self._ref_summary)
        copy_row_0 = swapped_summary._data.iloc[0].copy()
        swapped_summary._data.iloc[0] = swapped_summary._data.iloc[2].copy()
        swapped_summary._data.iloc[2] = copy_row_0
        # make sure that the swapped and reference summary objects are now indeed different
        with self.assertRaises(AssertionError):
            self._data_frames_equal(self._ref_summary._data, swapped_summary._data)
        # sort and test whether the two objects are now equal
        swapped_summary.sort()
        self._data_frames_equal(self._ref_summary._data, swapped_summary._data)

    def test_recalculate_totals(self):
        # get copy of tracked month with an invalid running total
        no_rt_summary = copy.deepcopy(self._ref_summary)
        no_rt_summary._data['running total'] = pd.Series([Time(i, i, False) for i in range(3)])
        no_rt_summary._data['total overtime'] = pd.Series([Time(i, i, False) for i in range(3)])
        # make sure that the tracked month object without running total and reference are now indeed different
        with self.assertRaises(AssertionError):
            self._data_frames_equal(self._ref_summary._data, no_rt_summary._data)
        # sort and test whether the two objects are now equal
        no_rt_summary.recalculate_totals()
        self._data_frames_equal(self._ref_summary._data, no_rt_summary._data)

    def test_save(self):
        out_path = Path('./tests/testdata/tmp/summary.csv')
        savable_summary = copy.deepcopy(self._ref_summary)
        savable_summary._file_path = out_path
        savable_summary.save()
        ref_file = open(Path('./tests/testdata/valid_reference_summary.csv'), 'rb')
        out_file = open(out_path, 'rb')
        try:
            self.assertEqual(ref_file.readlines(), out_file.readlines())
        finally:
            ref_file.close()
            out_file.close()
            out_path.unlink()

    def test_update_insert_month_append_new(self):
        month_to_insert = TrackedMonth.from_file(Path('./tests/testdata/valid_reference_month.csv'))
        summary_insert_copy = copy.deepcopy(self._ref_summary)
        with patch('builtins.input', return_value='7'):
            # test whether the month is actually inserted
            self.assertTrue(summary_insert_copy.update_insert_month(month_to_insert))
        # test whether the month is inserted as expected
        ref_summary_inserted = copy.deepcopy(self._ref_summary)
        month_summary = month_to_insert.get_month_summary(hours_per_week=7.0)
        ref_summary_inserted._data = ref_summary_inserted._data.append(month_summary)
        self._data_frames_equal(ref_summary_inserted._data, summary_insert_copy._data)

    def test_update_insert_month_skip_existing(self):
        month_to_insert = TrackedMonth.from_file(Path('./tests/testdata/months/2020_04_April.csv'))
        summary_insert_copy = copy.deepcopy(self._ref_summary)
        # test whether the month is actually not inserted
        self.assertFalse(summary_insert_copy.update_insert_month(month_to_insert))
        # test whether the month is not being inserted, as expected
        self._data_frames_equal(self._ref_summary._data, summary_insert_copy._data)

    def test_update_insert_month_update_existing(self):
        month_to_insert = TrackedMonth.from_file(Path('./tests/testdata/months/2020_04_April.csv'))
        month_to_insert.add_entry(date(2020, 4, 30), Time.from_string('19:00'), Time.from_string('21:00'), 'desc seven')
        summary_insert_copy = copy.deepcopy(self._ref_summary)
        # test whether the month is actually inserted
        self.assertTrue(summary_insert_copy.update_insert_month(month_to_insert))
        # test whether the month is inserted as expected
        ref_summary_inserted = copy.deepcopy(self._ref_summary)
        month_summary = month_to_insert.get_month_summary(hours_per_week=7.0)
        ref_summary_inserted._data.loc[2] = list(month_summary.loc[0])
        self._data_frames_equal(ref_summary_inserted._data, summary_insert_copy._data)

    def test_update_insert_month_update_existing_no_hpw(self):
        month_to_insert = TrackedMonth.from_file(Path('./tests/testdata/months/2020_04_April.csv'))
        month_to_insert.add_entry(date(2020, 4, 30), Time.from_string('19:00'), Time.from_string('21:00'), 'desc seven')
        summary_insert_copy = copy.deepcopy(self._ref_summary)
        # set the hours per week for the month to update to nan
        summary_insert_copy._data.at[2, 'hours per week'] = np.nan
        with patch('builtins.input', return_value='7'):
            # test whether the month is actually inserted
            self.assertTrue(summary_insert_copy.update_insert_month(month_to_insert))
        # test whether the month is inserted as expected
        ref_summary_inserted = copy.deepcopy(self._ref_summary)
        month_summary = month_to_insert.get_month_summary(hours_per_week=7.0)
        ref_summary_inserted._data.loc[2] = list(month_summary.loc[0])
        self._data_frames_equal(ref_summary_inserted._data, summary_insert_copy._data)

    def test_update(self):
        summary_update_copy = copy.deepcopy(self._ref_summary)
        with patch('builtins.input', return_value='7'):
            # update from testdata months directory
            summary_update_copy.update(data_dir=Path('./tests/testdata/months'))
        ref_summary_updated = copy.deepcopy(self._ref_summary)
        inserted_month = TrackedMonth.from_file(Path('./tests/testdata/months/2020_05_May.csv'))
        with patch('builtins.input', return_value='7'):
            # insert the month that should be inserted with the update function
            ref_summary_updated.update_insert_month(inserted_month)
            ref_summary_updated.sort()
            ref_summary_updated.recalculate_totals()
        self._data_frames_equal(ref_summary_updated._data, summary_update_copy._data)


if __name__ == '__main__':
    unittest.main()
