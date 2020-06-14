from datastructures import *
from TrackedMonth import TrackedMonth

import glob
import numpy as np
import pandas as pd
from pathlib import Path


class Summary:
    @classmethod
    def from_file(cls, filepath: Path):
        raw_data = pd.read_csv(filepath, sep=',', header=0)

        # ensure the given file has the expected columns
        Summary.validate_header(raw_data)

        raw_data['month'] = raw_data['month'].apply(Month.from_summary_string)
        raw_data['time done'] = raw_data['time done'].apply(Time.from_string)
        raw_data['running total'] = raw_data['running total'].apply(Time.from_string)
        raw_data['time required'] = raw_data['time required'].apply(Time.from_string)
        raw_data['overtime done'] = raw_data['overtime done'].apply(Time.from_string)
        raw_data['total overtime'] = raw_data['total overtime'].apply(Time.from_string)

        return cls(raw_data, filepath)

    @staticmethod
    def validate_header(data: pd.DataFrame):
        expected_header = ['month', 'time done', 'running total', 'time required', 'overtime done', 'total overtime',
                           'hours per week']
        assert np.array_equal(expected_header, data.columns)

    def __init__(self, data, summary_file: Path):
        self._data = data
        self._file_path = summary_file
        self.sort()
        self.recalculate_totals()

    def sort(self):
        self._data.sort_values(by='month', axis=0, inplace=True, ignore_index=True, kind='heapsort')

    def recalculate_totals(self):
        running_total = Time(0, 0, False)
        total_overtime = Time(0, 0, False)
        for el in self._data.iterrows():
            running_total = running_total + el[1]['time done']
            self._data.at[el[0], 'running total'] = running_total
            total_overtime = total_overtime + el[1]['overtime done']
            self._data.at[el[0], 'total overtime'] = total_overtime

    def update(self, data_dir=Path('./data'), file_pattern='*_*_*.csv'):
        month_files = glob.glob(str(data_dir / file_pattern))
        performed_an_update = False
        for filepath in month_files:
            month_data = TrackedMonth.from_file(Path(filepath))
            month_updated = self.update_insert_month(month_data)
            performed_an_update = performed_an_update or month_updated
        if performed_an_update:
            self.sort()
            self.recalculate_totals()

    def update_insert_month(self, month_data: TrackedMonth):
        month_updated = month_data.month()
        month_entry = self._data['month'] == month_updated
        if month_entry.any():
            existing_entry = self._data[month_entry]
            if not np.isnan(existing_entry['hours per week']).all():
                month_summary = month_data.get_month_summary(hours_per_week=existing_entry['hours per week'])
            else:
                month_summary = month_data.get_month_summary()
            update_entry = (existing_entry['time done'].iat[0] != month_summary['time done'].iat[0]) \
                           or (existing_entry['time required'].iat[0] != month_summary['time required'].iat[0]) \
                           or (existing_entry['hours per week'].iat[0] != month_summary['hours per week'].iat[0])
            if not type(update_entry) is bool:
                update_entry = update_entry.all()
            if update_entry:
                # get index of True value, replace that row, sort, recalculate totals
                idx = existing_entry.index[0]
                self._data.loc[idx] = month_summary.values.tolist()[0]
                return True
            return False
        else:
            month_summary = month_data.get_month_summary()
            self._data = self._data.append(month_summary)
            return True

    def save(self):
        self._data.to_csv(self._file_path, sep=',', index=False)
