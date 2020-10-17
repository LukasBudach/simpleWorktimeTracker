from bokeh.embed import components
from copy import deepcopy
from flask import Flask, redirect, render_template, request, session, url_for
from src.graph_factory import GraphFactory

import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/', methods=['GET', 'POST'])
def initial():
    session['plot_selection'] = {
        'optionTemperature': True,
        'optionHumidity': True,
        'optionNoise': False,
        'optionRain': False
    }
    session['first_plot_options'] = {
        'optionFirstLine': True,
        'optionFirstScatter': False,
        'optionFirstBar': False
    }
    session['second_plot_options'] = {
        'optionSecondLine': True,
        'optionSecondScatter': False,
        'optionSecondBar': False
    }

    return redirect(url_for('chart'))


@app.route('/updatePlotSelection', methods=['POST'])
def updatePlotSelection():
    session['plot_selection'] = {
        'optionTemperature': False,
        'optionHumidity': False,
        'optionNoise': False,
        'optionRain': False
    }
    for name_set in request.form.getlist('plotSelection'):
        session['plot_selection'][name_set] = True

    return redirect(url_for('chart'))


@app.route('/updateFirstPlotOptions', methods=['POST'])
def updateFirstPlotOptions():
    session['first_plot_options'] = {
        'optionFirstLine': False,
        'optionFirstScatter': False,
        'optionFirstBar': False
    }
    for name_set in request.form.getlist('plotOneOptions'):
        session['first_plot_options'][name_set] = True

    return redirect(url_for('chart'))


@app.route('/updateSecondPlotOptions', methods=['POST'])
def updateSecondPlotOptions():
    session['second_plot_options'] = {
        'optionSecondLine': False,
        'optionSecondScatter': False,
        'optionSecondBar': False
    }
    for name_set in request.form.getlist('plotTwoOptions'):
        session['second_plot_options'][name_set] = True

    return redirect(url_for('chart'))


@app.route('/chart')
def chart():
    plot_selection = session['plot_selection']
    plot_one_options = session['first_plot_options']
    plot_two_options = session['second_plot_options']

    print(plot_selection)

    factory = GraphFactory(db_conf='auth/local_postgres.json')
    used_first = False
    if plot_selection['optionTemperature']:
        if not used_first:
            factory.attach('temperature', ['temperature'],
                           line=plot_one_options['optionFirstLine'],
                           scatter=plot_one_options['optionFirstScatter'],
                           bar=plot_one_options['optionFirstBar'])
            used_first = True
        else:
            factory.attach('temperature', ['temperature'],
                           line=plot_two_options['optionSecondLine'],
                           scatter=plot_two_options['optionSecondScatter'],
                           bar=plot_two_options['optionSecondBar'])
    if plot_selection['optionHumidity']:
        if not used_first:
            factory.attach('humidity', ['humidity'],
                           line=plot_one_options['optionFirstLine'],
                           scatter=plot_one_options['optionFirstScatter'],
                           bar=plot_one_options['optionFirstBar'])
            used_first = True
        else:
            factory.attach('humidity', ['humidity'],
                           line=plot_two_options['optionSecondLine'],
                           scatter=plot_two_options['optionSecondScatter'],
                           bar=plot_two_options['optionSecondBar'])
    if plot_selection['optionNoise']:
        if not used_first:
            factory.attach('noise', ['noise'],
                           line=plot_one_options['optionFirstLine'],
                           scatter=plot_one_options['optionFirstScatter'],
                           bar=plot_one_options['optionFirstBar'])
            used_first = True
        else:
            factory.attach('noise', ['noise'],
                           line=plot_two_options['optionSecondLine'],
                           scatter=plot_two_options['optionSecondScatter'],
                           bar=plot_two_options['optionSecondBar'])
    if plot_selection['optionRain']:
        if not used_first:
            factory.attach('rain', ['currrain'],
                           line=plot_one_options['optionFirstLine'],
                           scatter=plot_one_options['optionFirstScatter'],
                           bar=plot_one_options['optionFirstBar'])
            used_first = True
        else:
            factory.attach('rain', ['currrain'],
                           line=plot_two_options['optionSecondLine'],
                           scatter=plot_two_options['optionSecondScatter'],
                           bar=plot_two_options['optionSecondBar'])

    script_plot, div_plot = components(factory.get_plot())

    inlines = {
        'div_plot': div_plot,
        'script_plot': script_plot
    }

    inlines.update(plot_selection)
    inlines.update(plot_one_options)
    inlines.update(plot_two_options)

    return render_template('index.html', **inlines)
