import json
import os
from datetime import datetime

import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, Response, render_template

app = Flask(__name__)

DATABASE_PATH = os.path.abspath(
    'data/tagesschau-data-fetching/database.json')


def getDataframe():

    df = pd.read_json(DATABASE_PATH)

    df['date'] = pd.to_datetime(
        df.date, format='%Y-%m-%dT%H:%M:%S.%f', utc=True)

    return df


@app.route('/bar-ressort-json', methods=['GET'])
def barRessortJSON():

    df = getDataframe()

    df = (df['ressort'].value_counts()
          .rename_axis('ressort')
          .reset_index(name='amount'))

    fig = px.bar(df, x='ressort', y='amount',
                 barmode='group', width=800, height=400)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/bar-day-json', methods=['GET', 'POST'])
def barDayJSON():

    df = getDataframe()

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

    f = open(DATABASE_PATH)

    data = json.load(f)

    dates = [datetime.fromisoformat(
        article['date']) for article in data]

    minDate = min(dates)
    maxDate = max(dates)

    size = os.path.getsize(DATABASE_PATH)

    features = json.loads(
        open('static/files/features.json', 'r', encoding='utf8').read())

    more_features = json.loads(
        open('static/files/more_features.json', 'r', encoding='utf8').read())

    return render_template("index.html", head=data[:10], last=data[-10:], minDate=minDate, size=size, maxDate=maxDate, features=features, more_features=more_features, length=len(data))


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
