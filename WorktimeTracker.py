from Summary import Summary
from TrackedMonth import TrackedMonth

import argparse

from datetime import date


class WorktimeTracker:
    @staticmethod
    def stay_at_date():
        return input('Add another entry for the same date? (y/n) ') == 'y'

    @staticmethod
    def date_to_iso(date_str):
        return '{}-{}-{}'.format(date_str[-4:], date_str[-7:-5], date_str[:2])

    @staticmethod
    def get_date(in_date):
        if in_date != '':
            return date.fromisoformat(WorktimeTracker.date_to_iso(in_date))
        else:
            return date.today()

    def __init__(self, multiple_dates=False):
        self._tracked_month = None
        self._current_date = None
        self._multiple_dates = multiple_dates

    def add_entries(self):
        while True:
            self.add_entries_for_one_date()
            next_date = False
            if self._multiple_dates:
                next_date = input('Do you want to want to add entries for another date? (y/n) ') == 'y'
            if not next_date:
                break

    def add_entries_for_one_date(self):
        self.get_new_date()
        self.get_tracked_month()

        add_entry = True
        while add_entry:
            self.add_entry_for_date()
            add_entry = self.stay_at_date()

    def get_new_date(self):
        date_in = input('Date of work (dd.mm.yyyy), leave empty if today: ')
        new_date = WorktimeTracker.get_date(date_in)
        if (self._current_date is not None) \
                and ((new_date.month != self._current_date.month) or (new_date.year != self._current_date.year)):
            self._tracked_month.save()
            self._tracked_month = None
        self._current_date = WorktimeTracker.get_date(date_in)

    def get_tracked_month(self):
        if self._tracked_month is None:
            self._tracked_month = TrackedMonth.from_date(self._current_date)

    def add_entry_for_date(self):
        start_in = input('Start time (hh:mm): ')
        end_in = input('End time (hh:mm): ')
        description = input('Work description: ')

        self._tracked_month.add_entry(self._current_date, start_in, end_in, description)

    def close(self):
        self._tracked_month.save()
        summ = Summary.from_file('data/Summary.csv')
        summ.update()
        summ.save()


def main(arguments):
    tracker = WorktimeTracker(multiple_dates=arguments.multiple_entries)
    tracker.add_entries()
    tracker.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--multiple-entries', action='store_true', help='Set flag to add multiple entries without'
                                                                              ' rerunning the script.')
    args = parser.parse_args()

    main(args)
