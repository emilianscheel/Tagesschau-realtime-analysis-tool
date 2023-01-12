import json
import os
from datetime import datetime
from flask import Blueprint, Response, render_template


# other scripts
from lib import *


pages = Blueprint('pages', __name__)


@pages.route('/', methods=['GET', 'POST'])
def index():

    f = open(getConfig("database_file"))

    data = json.load(f)

    dates = [datetime.fromisoformat(
        article['date']) for article in data]

    minDate = min(dates)
    maxDate = max(dates)

    size = os.path.getsize(getConfig("database_file"))

    features = json.loads(
        open('static/files/features.json', 'r', encoding='utf8').read())

    more_features = json.loads(
        open('static/files/more_features.json', 'r', encoding='utf8').read())

    diagrams = {
        "chart-1": "Artikel-Ressort",
        "chart-2": "Artikel-Tag",
        "chart-3": "Artikel-Länge-Ressort",
        "chart-4": "Artikel-Länge-Thema",
        "chart-5": "Artikel-Thema",
        "chart-6": "Artikel-Thema-&-Ressort",
        "chart-7": "Artikel-Ranking-Ressort",
        "chart-8": "Artikel-Ranking-Thema",
        "chart-9": "Artikel-Ranking-Thema-&-Ressort"
    }

    line_diagrams = {
        "chart-100": "Verlauf-Thema",
        "chart-99": "Verlauf-Stichwörter",
        "chart-98": "Verlauf-Länge-Thema",
        "chart-97": "Verlauf-Ranking-Thema"
    }

    return render_template("index.html", head=data[:10], last=data[-10:], version=getConfig("version"), minDate=minDate, line_diagrams=line_diagrams, diagrams=diagrams, size=size, maxDate=maxDate, features=features, more_features=more_features, length=len(data))


@pages.route('/database.json', methods=['GET'])
def sendFile():
    tagesschauDatabase = os.path.abspath(
        'data/tagesschau-data-fetching/database.json')

    content = open(tagesschauDatabase)
    return Response(content,
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=database.json'})
