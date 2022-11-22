import json
import os
from datetime import datetime

import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, Response, render_template

app = Flask(__name__)


def barRessortJSON(df):

    df = (df['ressort'].value_counts()
          .rename_axis('ressort')
          .reset_index(name='amount'))

    fig = px.bar(df, x='ressort', y='amount',
                 barmode='group', width=800, height=400)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def barDayJSON(df):

    df = (pd.to_datetime(df['date'])
          .dt.floor('d')
          .value_counts()
          .rename_axis('date')
          .reset_index(name='count')
          .sort_values('date'))

    fig = px.bar(df, x='date', y='count',
                 barmode='group', width=800, height=400)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/', methods=['GET', 'POST'])
def index():

    tagesschauDatabase = os.path.abspath(
        'data/tagesschau-data-fetching/database.json')

    f = open(tagesschauDatabase)

    data = json.load(f)

    dates = [datetime.fromisoformat(
        article['date']) for article in data]

    minDate = min(dates)
    maxDate = max(dates)

    size = os.path.getsize(tagesschauDatabase)
    df = pd.read_json(tagesschauDatabase)

    df['date'] = pd.to_datetime(
        df.date, format='%Y-%m-%dT%H:%M:%S.%f', utc=True)

    return render_template("index.html", head=data[:10], last=data[-10:], barRessortJSON=barRessortJSON(df), barDayJSON=barDayJSON(df), minDate=minDate, size=size, maxDate=maxDate, length=len(data))


@app.route('/database.json', methods=['GET'])
def sendFile():
    tagesschauDatabase = os.path.abspath(
        'data/tagesschau-data-fetching/database.json')

    content = open(tagesschauDatabase)
    return Response(content,
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=database.json'})


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)
