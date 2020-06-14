from TrackedMonth import TrackedMonth
from WorktimeTracker import WorktimeTracker

from datetime import date
from pathlib import Path
import pandas as pd
import unittest
from unittest.mock import patch


class TestWorktimeTracker(unittest.TestCase):
    def setUp(self):
        self._tracker = WorktimeTracker(data_dir=Path('./tests/testdata/months'))

    def _data_frames_equal(self, reference, other):
        # shapes of data frames are equal
        self.assertEqual(reference.shape, other.shape)
        # contents of data frames are equal
        for col in reference.columns:
            self.assertTrue((reference[col] == other[col]).all())

    def test_stay_at_date_yes(self):
        with patch('builtins.input', return_value='y'):
            self.assertTrue(WorktimeTracker.stay_at_date())

    def test_stay_at_date_no(self):
        with patch('builtins.input', return_value='n'):
            self.assertFalse(WorktimeTracker.stay_at_date())

    def test_get_new_date_from_empty(self):
        with patch('builtins.input', return_value='03.05.2020'):
            self._tracker.get_new_date()
        self.assertEqual(date(2020, 5, 3), self._tracker._current_date)

    def test_get_tracked_month_new_month(self):
        # set a date that does not yet have a month tracking file in `tests/testdata/months`
        with patch('builtins.input', return_value='03.05.2019'):
            self._tracker.get_new_date()
        self._tracker.get_tracked_month()
        ref_tracked_month = TrackedMonth(data=pd.DataFrame(columns=['date', 'start', 'end', 'work time',
                                                                    'running total', 'description']),
                                         month=date(2019, 5, 1))
        self._data_frames_equal(ref_tracked_month._data, self._tracker._tracked_month._data)
        self.assertEqual(ref_tracked_month.month(), self._tracker._tracked_month.month())

    def test_get_tracked_month_exsiting_month(self):
        # set the date based on which a tracked month will be loaded
        with patch('builtins.input', return_value='03.05.2020'):
            self._tracker.get_new_date()
        self._tracker.get_tracked_month()
        ref_tracked_month = TrackedMonth.from_file(Path('./tests/testdata/months/2020_05_May.csv'))
        self._data_frames_equal(ref_tracked_month._data, self._tracker._tracked_month._data)


if __name__ == '__main__':
    unittest.main()
