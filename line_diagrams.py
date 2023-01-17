

from flask import Blueprint


# data science imports
import pandas as pd
import plotly
import plotly.express as px
import json

# other scripts
from lib import *
from functions import *


line_diagram_api = Blueprint('line_diagram_api', __name__)


date_begin = getConfig("date_begin")
date_end = getConfig("date_end")
width = float(getConfig("width"))
height = float(getConfig("height"))


@line_diagram_api.route('/Verlauf-Ranking-Thema', methods=['GET'])
def chart97():

    df = getDataframe()

    # Ändere das Feature `date` zu einem einheitlichen Datum
    df['date'] = pd.to_datetime(df['date'], utc=True)

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Fülle alle NaN Werte aus `rankings` mit einem leeren Array
    df['rankings'] = df['rankings'].fillna("[]")

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Füge vier neue Features hinzu: Tag, Woche, Monat, Jahr
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Füge ein neues Feature hinzu: Ranking besser als 5. Platz
    def high_ranking(x):
        if (type(x) == list):
            return any(ranking['score'] <= 5 for ranking in x)
        return False

    df['high_ranking'] = df['rankings'].apply(high_ranking)

    # Filter die Artikel nach: Hohes Ranking vorhanden
    df = df.loc[df.high_ranking]

    target_names = list(map(lambda short: topics[short]['name'], topics))

    df = merge_data_week_year(df, from_column='topic', to_columns=target_names)

    # Gruppiere die Artikel eines Themengebiets nach: Woche (eindeutig)
    # Füge alle entstandenen Daten mit `merge` zusammen

    fig = px.line(df, x="timestamp", y=target_names, title="Anzahl der Artikel auf den ersten 5 Plätzen",
                  labels={"timestamp": "Datum",
                          "variable": "Themengebiete",
                          "value": ""
                          },
                  height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@line_diagram_api.route('/Verlauf-Länge-Thema', methods=['GET'])
def chart98():

    df = getDataframe()

    # Ändere das Feature `date` zu einem einheitlichen Datum
    df['date'] = pd.to_datetime(df['date'], utc=True)

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Füge vier neue Features hinzu: Tag, Woche, Monat, Jahr
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Füge zwei neue Features hinzu: Anzahl Wörter, Anzahl Zeichen
    df['content_length'] = df['content'].str.len()
    df['content_words'] = df['content'].str.split().map(len)

    target_names = list(map(lambda short: topics[short]['name'], topics))

    # Gruppiere die Artikel nach: Woche (eindeutig)
    def perform_group(df: pd.DataFrame, column: str):
        return df.groupby(["week", "year"])['content_words'].mean().reset_index(name=column)

    df = merge_data_week_year2(df, from_column='topic',
                               to_columns=target_names, perform_group=perform_group)

    # Fülle die leeren Felder mit der Anzahl 0
    df = df.fillna(0)

    df = df.sort_values('timestamp', ascending=True)

    fig = px.line(df, x="date", y=target_names, title="Anzahl der Wörter der Artikel pro Woche",
                  labels={"date": "Datum",
                          "variable": "Themengebiete",
                          "value": "Durchschnittliche Anzahl der Wörter"
                          },
                  height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@line_diagram_api.route('/Verlauf-Stichwörter', methods=['GET'])
def chart99():
    df = getDataframe()

    target = ["Corona", "Weihnachten", "Infektionszahlen"]

    # Ändere das Feature `date` zu einem einheitlichen Datum
    df['date'] = pd.to_datetime(df['date'], utc=True)

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Stichwort
    keywords = json.loads(open("data-keywords/keywords.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df.tags.to_list()]

    for keyword in keywords:
        df.loc[(df.title.str.contains(keyword) | df.content.str.contains(
            keyword) | df.tags_full.str.contains(keyword)), 'keyword'] = keyword

    # Füge vier neue Features hinzu: Tag, Woche, Monat, Jahr
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Gruppiere die Artikel nach: Woche (eindeutig)
    df = merge_data_week_year(df, from_column='keyword', to_columns=target)

    # Fülle die leeren Felder mit der Anzahl 0
    df = df.fillna(0)

    df = df.sort_values("timestamp")

    fig = px.line(df, x="date", y=target, title="Anzahl der Artikel pro Woche",
                  labels={"date": "Datum",
                          "variable": "Stichwörter",
                          "value": "Anzahl der Artikel"
                          },
                  height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@line_diagram_api.route('/Verlauf-Thema', methods=['GET'])
def chart100():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Füge vier neue Features hinzu: Tag, Woche, Monat, Jahr
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # 1. Gruppiere Artikel nach: Woche (eindeutig)
    target_names = list(map(lambda short: topics[short]['name'], topics))

    df = merge_data_week_year(df, from_column='topic', to_columns=target_names)

    # Fülle die leeren Felder mit der Anzahl 0
    df = df.fillna(0)

    fig = px.line(df, x="date", y=target_names, title="Anzahl der Artikel pro Woche",
                  labels={"date": "Datum",
                          "variable": "Themengebiete",
                          "value": "Anzahl der Artikel"
                          },
                  height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
