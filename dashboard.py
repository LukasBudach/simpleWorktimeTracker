from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from flask_socketio import SocketIO, emit

from Summary import Summary
from datastructures.Dates import Month

from pathlib import Path

import os

app = Flask(__name__)
app.secret_key = os.urandom(16)
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def setup():
    session['year'] = None

    return redirect(url_for('overview'))


@app.route('/overview', methods=['GET', 'POST'])
def overview():
    if 'year' in request.args.keys():
        session['year'] = request.args['year']

    return render_template('index.html')


@app.route('/assets/<path:path>')
def provide_assets(path):
    return send_from_directory('static/assets', path)


@socketio.on('connected')
def create_page():
    summary = Summary.from_file(Path('data/Summary.csv'))

    if session['year'] is not None:
        create_cards_for_year(session['year'])

    latest_data = summary.get_latest_month()
    emit('updateHeader', (latest_data['running total'].as_string(),
                          (latest_data['running total'] - latest_data['total overtime']).as_string(),
                          latest_data['total overtime'].as_string(), latest_data['total overtime'].is_negative()
                          ))

    emit('updateYearDropdown', list(range(summary.get_min_year(), summary.get_max_year()+1)))


def create_cards_for_year(year):
    summary = Summary.from_file(Path('data/Summary.csv'))

    if year == 'all':
        years = list(range(summary.get_min_year(), summary.get_max_year() + 1))
    else:
        years = [int(year)]

    for year in years:
        for month in range(1, 13):
            target_month = Month(month, year)
            recorded_data = summary.get_month(target_month)
            if recorded_data is not None:
                emit('createCard', (target_month.as_string()[:-5], year, recorded_data['time required'].as_string(),
                                    recorded_data['time done'].as_string()))


if __name__ == '__main__':
    socketio.run(app, debug=False, port=8000, host='192.168.178.22')
