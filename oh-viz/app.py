from flask import Flask, render_template, json,Response, jsonify, request, redirect
from helpers import extract_timeseries_data, extract_column, build_table, unix_time_millis
from datetime import datetime, timedelta
from collections import OrderedDict
from chart import Chart
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/')
def index():
    # df = pd.read_table('static/data/app_units.tsv', parse_dates=[0])
    # df1 = df.rename(columns={'iOS Downloads': 'iosw', 'Android Downloads': 'androidw'})
    # df1['total'] = df1['iosw'] + df1['androidw']
    # iosw, androidw, total = extract_timeseries_data(df1, ['iosw', 'androidw', 'total'])

    charts = [] # list of charts you want to appear on page

    chart3 = Chart("Important Chart")
    dates = pd.date_range(start="2016-01-01", end="2016-01-31").map(unix_time_millis)
    chart3.add_series('apples', [list(a) for a in zip(dates, np.random.randint(0, 10, 31))])
    chart3.add_series('oranges', [list(a) for a in zip(dates, np.random.randint(0, 10, 31))])
    chart3.add_series('grapes', [list(a) for a in zip(dates, np.random.randint(20, 50, 31))])
    chart3.add_notes("This very informative chart is an inventory of the fruit currently available in the kitchen. Also testing what happens when the notes are really long.")
    # Update the ylabel from the default instead of passing in when creating:
    chart3.ylabel = "Fruits"
    charts.append(chart3)

    # page level metadata
    page_name="Demo"
    exec_summary = '''
    We did a lot of analyses here. Here are some top level notes about them:</br>
    <ul><li>We have awesome user retention. We have lots of downloads and clicks.</li>
    <li>Analytics is super cool. I can use html tags if I want.</li></ul>
    Or just write a plain string if I prefer where I discuss all the insights or highlights from
    my charts and analysis below. Note how when it's just a plain string it's not formatted
    in any particular way.
    Look at how I can do line breaks.</br>
    </br>
    This note was passed in from render_template().
    '''

    return render_template("example.html", page_name=page_name, summary=exec_summary, charts=charts)

@app.route('/data-monitor')
def data_monitor():
    charts = []
    # df = pd.read_csv('static/data/iat.csv')

    return render_template("data-monitor.html")

@app.route('/test-json')
def test_json():
    json = [{
        "name": "Tiger Nixon",
        "position": "System Architect",
        "salary": "$320,800",
        "start_date": "2011/04/25",
        "office": "Edinburgh",
        "extn": "5421"
      }, {
        "name": "Garrett Winters",
        "position": "Accountant",
        "salary": "$170,750",
        "start_date": "2011/07/25",
        "office": "Tokyo",
        "extn": "8422"
      }]
    return jsonify(json)

if __name__ == '__main__':
    app.run(debug=True)
