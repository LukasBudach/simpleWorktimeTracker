from Summary import Summary
from TrackedMonth import TrackedMonth

from utils import binary_question_input, date_input, time_input

import argparse

from datetime import date
from pathlib import Path


class WorktimeTracker:
    @staticmethod
    def stay_at_date():
        return binary_question_input('Add another entry for the same date? (y/n) ')

    def __init__(self, multiple_dates=False, data_dir=Path('./data')):
        self._tracked_month = None
        self._current_date = None
        self._multiple_dates = multiple_dates
        self._data_dir = data_dir

    # can't test, as the self.add_entry_for_one_date() function requires multiple different inputs
    def add_entries(self):  # pragma: no cover
        while True:
            self.add_entries_for_one_date()
            next_date = False
            if self._multiple_dates:
                next_date = binary_question_input('Do you want to want to add entries for another date? (y/n) ')
            if not next_date:
                break

    # can't test, as the self.add_entry_for_date() function requires multiple different inputs
    def add_entries_for_one_date(self):  # pragma: no cover
        self.get_new_date()
        self.get_tracked_month()

        add_entry = True
        while add_entry:
            self.add_entry_for_date()
            add_entry = self.stay_at_date()

    def get_new_date(self):
        new_date = date_input('Date of work (dd.mm.yyyy), leave empty if today: ', empty_for_today=True)
        if (self._current_date is not None) \
                and ((new_date.month != self._current_date.month) or (new_date.year != self._current_date.year)):
            self._tracked_month.save()
            self._tracked_month = None
        self._current_date = new_date

    def get_tracked_month(self):
        if self._tracked_month is None:
            self._tracked_month = TrackedMonth.from_date(self._current_date, target_dir=self._data_dir)

    # can't cover in tests due to multiple different inputs being needed
    def add_entry_for_date(self):  # pragma: no cover
        start_in = time_input('Start time (hh:mm): ')
        end_in = time_input('End time (hh:mm): ')
        description = input('Work description: ')

        self._tracked_month.add_entry(self._current_date, start_in, end_in, description)

    def close(self):
        self._tracked_month.save()
        summ = Summary.from_file(self._data_dir / 'Summary.csv')
        summ.update(data_dir=self._data_dir)
        summ.save()


# can't cover in tests due to multiple different inputs being needed by the WorktimeTracker.add_entries() function
def main(arguments):  # pragma: no cover
    tracker = WorktimeTracker(multiple_dates=arguments.multiple_entries)
    tracker.add_entries()
    tracker.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--multiple-entries', action='store_true', help='Set flag to add multiple entries without'
                                                                              ' rerunning the script.')
    args = parser.parse_args()

    main(args)
