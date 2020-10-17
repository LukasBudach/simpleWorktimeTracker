from calendar import monthrange
from datetime import datetime, date
from pathlib import Path

from psycopg2.extras import execute_values
from psycopg2.sql import SQL
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

import json
import logging
import pandas as pd
import psycopg2

import re

from datastructures.Time import Time

# TODO: this is a utils function, when refactoring, do this!
def sanitize_string(string):
    # replace umlauts
    string = string.lower()
    string = string.encode()
    string = string.replace('ü'.encode(), b'ue')
    string = string.replace('ä'.encode(), b'ae')
    string = string.replace('ö'.encode(), b'oe')
    string = string.replace('ß'.encode(), b'ss')
    string = string.decode('utf-8')

    # remove all other special characters and return
    return re.sub('[^A-Za-z0-9]+', '', string)


class Database:
    def __init__(self, conf):
        conf_f = open(Path(conf), 'r')
        conf = json.load(conf_f)
        conf_f.close()

        self._host = conf['host']
        self._port = conf['port']
        self._database = conf['database']
        self._user = conf['user']
        self._password = conf['password']
        self._connection = None

    def is_connected(self):
        return self._connection is not None

    def _connect(self):
        if self.is_connected():
            return
        self._connection = psycopg2.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password
        )

    def _submit(self, silent=False):
        self._connection.commit()
        self._close()
        if not silent:
            logging.info('Submitted changes to the database.')

    def _close(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None

    def _get_cursor(self):
        return self._connection.cursor()

    def _execute_request(self, query, record, silent=False):
        self._connect()
        cursor = self._get_cursor()
        cursor.execute(query, record)
        cursor.close()
        self._submit(silent=silent)

    def insert(self, table, record, silent=False):
        if not silent:
            logging.info('Writing record to table {}...'.format(table))
        val_list_placeholder = '%s'
        for i in range(len(record) - 1):
            val_list_placeholder = val_list_placeholder + ', %s'
        query = SQL(u"INSERT INTO {} VALUES ({}) ON CONFLICT DO NOTHING".format(table, val_list_placeholder))

        self._execute_request(query, record, silent=silent)
        return True

    def insert_many(self, table, records, silent=False):
        if not silent:
            logging.info('Writing {} records to table {}...'.format(len(records), table))

        query = SQL("INSERT INTO {} VALUES %s ON CONFLICT DO NOTHING".format(table))

        self._connect()
        cursor = self._get_cursor()
        execute_values(cursor, query, records)
        cursor.close()
        self._submit(silent=silent)

    def _create_table(self, table_name, table_type):
        query = SQL('CREATE TABLE {} ( LIKE abstract{} INCLUDING ALL )'.format(table_name, table_type))

        self._connect()
        cursor = self._get_cursor()
        try:
            cursor.execute(query)
        except psycopg2.errors.DuplicateTable as e:
            print(e)
            return False
        finally:
            cursor.close()
            self._submit(silent=True)

        return True

    def insert_job(self, table, data):
        try:
            record = [
                str(data['title']),
                '{}{}'.format(sanitize_string(data['title']), 'summary'),
                '{}{}'.format(sanitize_string(data['title']), 'data')
            ]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a job with incomplete data, aborting.')
            return False

        print(record[0])

        if not self._create_table(record[1], 'summary') and self._create_table(record[2], 'data'):
            return False

        return self.insert(table, record, silent=True)

    def _get_job_data_table(self, job):
        query = SQL("SELECT data_table FROM jobs WHERE title=%s")

        self._connect()
        cursor = self._get_cursor()
        cursor.execute(query, (job,))
        data_table_name = cursor.fetchall()
        cursor.close()
        self._close()

        if not data_table_name:
            return False
        return data_table_name[0][0]

    def _get_job_summary_table(self, job):
        query = SQL("SELECT summary_table FROM jobs WHERE title=%s")

        self._connect()
        cursor = self._get_cursor()
        cursor.execute(query, (job,))
        summary_table_name = cursor.fetchall()
        cursor.close()
        self._close()

        if not summary_table_name:
            return False
        return summary_table_name[0][0]

    def get_running_total(self, job, job_data_table=None):
        if job_data_table is None:
            job_data_table = self._get_job_data_table(job)

        query = SQL("SELECT running_total FROM {} ORDER BY start_time DESC LIMIT 1".format(job_data_table))

        self._connect()
        cursor = self._get_cursor()
        cursor.execute(query)
        latest_running_total = cursor.fetchall()
        cursor.close()
        self._close()

        if not latest_running_total:
            return 0
        return latest_running_total[0][0]

    def get_summary_entry(self, job_summary_table, month):
        query = SQL("SELECT * FROM {} WHERE month=%s".format(job_summary_table))

        self._connect()
        cursor = self._get_cursor()
        cursor.execute(query, (month,))
        entry = cursor.fetchall()
        cursor.close()
        self._close()

        if not entry:
            return False
        return entry[0]

    def update_summary(self, job, data):
        # use the existing stuff, this makes me cry
        pass

    def insert_work_entry(self, job, data):
        # fetch the table to be written to
        data_table = self._get_job_data_table(job)

        if data_table is False:
            logging.warning('The job {} does not exist yet. Please create it and insert a work entry then.')
            return False

        # build the record
        try:
            # get the last running total and calculate the new
            running_total = self.get_running_total(job, data_table)
            running_total = running_total + (data['end_time'] - data['start_time']).value()

            record = [
                data['start_time'].as_datetime(data['date']),
                data['end_time'].as_datetime(data['date']),
                running_total,                      # calculate running total I guess
                data['description']
            ]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert incomplete worktime data, aborting.')
            return False

        # insert the record
        self.insert(data_table, record, silent=True)

        # recalculate and re-write the summary as needed
        self.update_summary(job, data)

        return True

    def insert_temperature(self, data):
        logging.info('Writing temperature information...')

        try:
            temp_data = [data['dashboard_data']['Temperature']]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a temperature reading with invalid data, aborting.')
            return False

        return self._insert_data_point('temperature', data, temp_data)

    def insert_humidity(self, data):
        logging.info('Writing humidity information...')

        try:
            humidity_data = [data['dashboard_data']['Humidity']]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a humidity reading with invalid data, aborting.')
            self._close()
            return False

        return self._insert_data_point('humidity', data, humidity_data)

    def insert_co2(self, data):
        logging.info('Writing carbon dioxide information...')

        try:
            co2_data = [data['dashboard_data']['CO2']]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a CO2 reading with invalid data, aborting.')
            return False

        return self._insert_data_point('carbioxide', data, co2_data)

    def insert_noise(self, data):
        logging.info('Writing noise information...')

        try:
            noise_data = [data['dashboard_data']['Noise']]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a noise reading with invalid data, aborting.')
            return False

        return self._insert_data_point('noise', data, noise_data)

    def insert_pressure(self, data):
        logging.info('Writing pressure information...')

        try:
            pressure_data = [
                data['dashboard_data']['Pressure'],
                data['dashboard_data']['AbsolutePressure']
            ]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a pressure reading with invalid data, aborting.')
            return False

        return self._insert_data_point('pressure', data, pressure_data)

    def insert_rain(self, data):
        logging.info('Writing rain information...')

        try:
            rain_data = [data['dashboard_data']['Rain']]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a noise reading with invalid data, aborting.')
            return False

        return self._insert_data_point('rain', data, rain_data)

    def insert_wind(self, data):
        logging.info('Writing wind information...')

        try:
            wind_data = [
                data['dashboard_data']['WindStrength'],
                data['dashboard_data']['WindAngle'],
                data['dashboard_data']['GustStrength'],
                data['dashboard_data']['GustAngle']
            ]
        except KeyError as e:
            logging.debug('Missing key: {}'.format(e))
            logging.warning('Attempted to insert a wind reading with invalid data, aborting.')
            return False

        return self._insert_data_point('wind', data, wind_data)

    def get_table_schema(self, table_name, silent=False):
        if not silent:
            logging.info('Reading schema for table {}.'.format(table_name))

        self._connect()
        query = """SELECT column_name FROM information_schema.columns WHERE table_name=%s"""

        cursor = self._get_cursor()
        cursor.execute(query, (table_name,))
        schema = cursor.fetchall()
        cursor.close()
        self._close()

        return [colname[0] for colname in schema]

    def read_table_full(self, table, order_by_col=None, silent=False):
        if not silent:
            logging.info('Attempting to fetch all records from the database table {}...'.format(table))

        schema = self.get_table_schema(table, silent=True)

        self._connect()
        if order_by_col is None:
            query = SQL("SELECT * FROM {}".format(table))
        else:
            query = SQL("SELECT * FROM {} ORDER BY {} ASC".format(table, order_by_col))

        cursor = self._get_cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        self._close()

        return pd.DataFrame(data=records, columns=schema)

    def read_data_table_full(self, table, silent=False):
        return self.read_table_full(table, order_by_col='requesttime', silent=silent)

    def read_data_table_uniques(self, table, silent=False):
        if not silent:
            logging.info('Attempting to fetch only unique records from the database table {}.'.format(table))

        return self.read_data_table_full(table, silent=True).drop_duplicates(subset='datatime', ignore_index=True)

    def get_device_information(self, device_ids, silent=False):
        if not silent:
            logging.info('Attempting to fetch information for the given device IDs.')

        records = self.read_table_full('device', silent=True)
        return records[records['address'].isin(device_ids)]


if __name__ == '__main__':
    from datastructures.Time import Time

    db = Database('auth/postgres.json')
    db.insert_job('jobs', {'title': 'TestJob'})

    data = {
        'date': date.today(),
        'start_time': Time(6, 00, False),
        'end_time': Time(7, 30, False),
        'description': 'My third test entry! This is a lot less interesting now'
    }
    print(db.get_running_total('TestJob'))
    print(db.insert_work_entry('TestJob', data))
