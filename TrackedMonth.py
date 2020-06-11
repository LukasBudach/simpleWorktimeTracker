from datastructures import *

from calendar import monthrange
import datetime
import numpy as np
import pandas as pd
from pathlib import Path


class TrackedMonth:
    @classmethod
    def from_file(cls, filepath):
        raw_data = pd.read_csv(filepath, sep=',', header=0)

        # ensure the given file has the expected columns
        TrackedMonth.validate_header(raw_data)

        raw_data['date'] = raw_data['date'].apply(lambda d: datetime.datetime.strptime(d, '%d.%m.%Y').date())
        raw_data['start'] = raw_data['start'].apply(Time.from_string)
        raw_data['end'] = raw_data['end'].apply(Time.from_string)
        raw_data['work time'] = raw_data['work time'].apply(Time.from_string)
        raw_data['running total'] = raw_data['running total'].apply(Time.from_string)

        month_tracked = datetime.date(raw_data['date'][0].year, raw_data['date'][0].month, 1)

        return cls(raw_data, month_tracked)

    @classmethod
    def from_date(cls, date: datetime.date):
        filepath = Path('data/{}_{}_{}.csv'.format(date.year,
                                                   date.strftime('%m'),
                                                   date.strftime('%B')))
        if not filepath.exists():
            return cls(data=pd.DataFrame(columns=['date', 'start', 'end', 'work time', 'running total', 'description']),
                       month=date)
        else:
            return cls.from_file(filepath)

    @staticmethod
    def validate_header(data: pd.DataFrame):
        expected_header = ['date', 'start', 'end', 'work time', 'running total', 'description']
        assert np.array_equal(expected_header, data.columns)

    def __init__(self, data: pd.DataFrame, month: datetime.date):
        TrackedMonth.validate_header(data)
        self._data = data
        self._month = month
        self.sort()
        self.recalculate_running_total()

    def save(self):
        filepath = Path('data/{}_{}_{}.csv'.format(self._month.year,
                                                   self._month.strftime('%m'),
                                                   self._month.strftime('%B')))
        filepath.parent.mkdir(parents=True, exist_ok=True)

        self.sort()
        self.recalculate_running_total()

        output_df = self._data
        output_df['date'] = output_df['date'].apply(lambda d: d.strftime('%d.%m.%Y'))
        output_df.to_csv(filepath, sep=',', index=False)

    def add_entry(self, date: datetime.date, start: str, end: str, description: str):
        start_time = Time.from_string(start)
        end_time = Time.from_string(end)
        found_overlap, overlapping_entries = self.overlapping_entry_exists(date, start_time, end_time)
        if found_overlap:
            print('The work time entry {} starting {} and ending {} overlaps with the following entries:'
                  .format(date.strftime('%d.%m.%Y'), start, end))
            overlap = self._data[overlapping_entries]
            for el in overlap.iterrows():
                print('{} start {} end {}'.format(el[1]['date'].strftime('%d.%m.%Y'), el[1]['start'], el[1]['end']))
            overwrite_entry = input('Do you want to overwrite all of these entries? (y/n) ')
            if overwrite_entry == 'y':
                self._data = self._data[overlapping_entries.apply(lambda b: not b)]
            else:
                return

        new_entry = pd.DataFrame(columns=['date', 'start', 'end', 'work time', 'running total', 'description'])
        new_entry.loc[0] = [date, start_time, end_time, end_time - start_time, Time(0, 0, False), description]
        self._data = self._data.append(new_entry)
        self.sort()
        self.recalculate_running_total()

    def overlapping_entry_exists(self, date: datetime.date, start: Time, end: Time):
        same_date_entries = self._data['date'] == date
        df = self._data[same_date_entries]
        overlapping_entries = same_date_entries
        for el in df.iterrows():
            idx = el[0]
            dat = el[1]
            overlapping_entries[idx] = overlapping_entries[idx] \
                                       and (((start <= dat['start']) and (end > dat['start']))
                                            or ((dat['start'] < start) and dat['end'] > start))

        return overlapping_entries.any(), overlapping_entries

    def sort(self):
        self._data.sort_values(by=['date', 'start'], axis=0, inplace=True, ignore_index=True, kind='heapsort')

    def recalculate_running_total(self):
        running_total = Time(0, 0, False)
        for el in self._data.iterrows():
            running_total = running_total + el[1]['work time']
            self._data['running total'][el[0]] = running_total

    def get_month_summary(self, hours_per_week=None):
        df = pd.DataFrame(columns=['month', 'time done', 'running total', 'time required', 'overtime done',
                                   'total overtime', 'hours per week'])
        if hours_per_week is None:
            hpw = input('How many hours per week do you have to work in {} (as float)? '
                        .format(self._month.strftime('%B %Y')))
            hours_per_week = float(hpw)

        req_t = Time.required_time_calculation(monthrange(self._month.year, self._month.month)[1], hours_per_week)
        total_t = self._data['running total'].max()
        df.loc[0] = [Month(self._month.month, self._month.year), total_t, Time(0, 0, False), req_t, total_t - req_t,
                     Time(0, 0, False), hours_per_week]
        return df

    def month(self):
        return Month(self._month.month, self._month.year)
