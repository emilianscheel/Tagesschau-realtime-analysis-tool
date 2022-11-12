from datetime import datetime
from flask import Flask, Response, render_template
import json
import os

app = Flask(__name__)


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

    return render_template("index.html", head=data[:10], minDate=minDate, size=size, maxDate=maxDate, length=len(data))


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
