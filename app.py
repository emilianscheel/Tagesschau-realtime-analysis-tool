from datetime import datetime
from flask import Flask, render_template
import json
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    tagesschauDatabase = os.path.expanduser(
        '~/data/tagesschau-data-fetching/database.json')

    f = open(tagesschauDatabase)

    data = json.load(f)

    dates = [datetime.fromisoformat(
        article['date']) for article in data]

    minDate = min(dates)
    maxDate = max(dates)

    return render_template("index.html", head=data[:10], minDate=minDate, maxDate=maxDate, length=len(data))


app.run(debug=True)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)