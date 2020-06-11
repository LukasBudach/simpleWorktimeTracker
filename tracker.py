from Summary import Summary
from TrackedMonth import TrackedMonth

import argparse

from datetime import date


def date_to_iso(date_str):
    return '{}-{}-{}'.format(date_str[-4:], date_str[-7:-5], date_str[:2])


def get_date(in_date):
    if in_date != '':
        return date.fromisoformat(date_to_iso(in_date))
    else:
        return date.today()


def add_entry_for_date(tm: TrackedMonth, d: date):
    start_in = input('Start time (hh:mm): ')
    end_in = input('End time (hh:mm): ')
    descrip = input('Work description: ')

    tm.add_entry(d, start_in, end_in, descrip)
    return input('Add another entry for the same date? (y/n) ') == 'y'


def main(arguments):
    while True:
        stay_at_date = True
        date_in = input('Date of work (dd.mm.yyyy), leave empty if today: ')
        d = get_date(date_in)
        tm = TrackedMonth.from_date(d)

        while stay_at_date:
            stay_at_date = add_entry_for_date(tm, d)

        tm.save()
        next_date = False
        if arguments.multiple_entries:
            next_date = input('Do you want to want to add entries for another date? (y/n) ') == 'y'
        if not next_date:
            break

    summ = Summary.from_file('data/Summary.csv')
    summ.update()
    summ.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--multiple-entries', action='store_true', help='Set flag to add multiple entries without'
                                                                              ' rerunning the script.')
    args = parser.parse_args()

    main(args)
