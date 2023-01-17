

from flask import Blueprint


# data science imports
import pandas as pd
import plotly
import plotly.express as px
import json

# other scripts
from lib import *


diagram_api = Blueprint('diagram_api', __name__)


date_begin = getConfig("date_begin")
date_end = getConfig("date_end")
width = float(getConfig("width"))
height = float(getConfig("height"))


@diagram_api.route('/Artikel-Ranking-Thema-&-Ressort', methods=['GET'])
def chart9():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    df['date'] = pd.to_datetime(df['date'], utc=True)

    # Ändere die Spalte `ressort` zu einem Anfangsgroßbuchstaben
    df.ressort = df.ressort.str.title()

    # Ändere das Ressort der Artikel ohne Zuordnung zu `(Kein Ressort)`
    df.ressort = df.ressort.replace(r'\s+|^$', "(Kein Ressort)", regex=True)

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Fülle alle NaN Werte aus `rankings` mit einem leeren Array
    df['rankings'] = df['rankings'].fillna("[]")

    # Füge ein neues Feature hinzu: Ranking besser als 5. Platz
    def high_ranking(x):
        if (type(x) == list):
            return any(ranking['score'] <= 5 for ranking in x)
        return False

    df['high_ranking'] = df['rankings'].apply(high_ranking)

    # Filter die Artikel nach: Hohes Ranking vorhanden
    df = df.loc[df.high_ranking]

    # Gruppiere die Artikel nach: Themengebiet
    df_ressort = df.groupby(["ressort"]).size().reset_index(name='amount')
    df_ressort = df_ressort.rename(columns={'ressort': 'group'})

    df_ressort['color'] = "#8ecae6"  # blue
    df_ressort['edgecolor'] = "#219ebc"  # blue

    # Gruppiere die Artikel nach: Ressort
    df_topic = df.groupby(["topic"]).size().reset_index(name='amount')
    df_topic = df_topic.rename(columns={'topic': 'group'})

    df_topic['color'] = "#f2cc8f"  # orange
    df_topic['edgecolor'] = "#e07a5f"  # orange

    # Füge die beiden enstandenen Daten in einen `DataFrame`
    df = pd.concat([df_ressort, df_topic])

    # Sortiere die Artikel nach: Anzahl Top-Rankings (absteigend)
    df = df.sort_values(by='amount', ascending=False)

    fig = px.bar(df, x='group', y='amount', color="color", title="Anzahl der Artikel mit Ranking auf den ersten 5 Plätzen",
                 labels={"group": "Themengebiet und Ressorts",
                         "amount": "Anzahl der Artikel",
                         "color": "Art",
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Ranking-Thema', methods=['GET'])
def chart8():
    df = getDataframe()

    # Fülle alle NaN Werte aus `rankings` mit einem leeren Array
    df['rankings'] = df['rankings'].fillna("[]")

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Füge ein neues Feature hinzu: Ranking besser als 5. Platz
    def high_ranking(x):
        if (type(x) == list):
            return any(ranking['score'] <= 5 for ranking in x)
        return False

    df['high_ranking'] = df['rankings'].apply(high_ranking)

    # Filter die Artikel nach: Hohes Ranking vorhanden
    df = df.loc[df.high_ranking]

    # Gruppiere die Artikel nach: Themengebiet
    df_topics = df.groupby(["topic"]).size().reset_index(name='amount')

    # Sortiere die Artikel nach: Anzahl Top-Rankings (absteigend)
    df_topics = df_topics.sort_values(by='amount', ascending=False)

    fig = px.bar(df_topics, x='topic', y='amount', title="Anzahl der Artikel mit Ranking auf den ersten 5 Plätzen",
                 labels={"topic": "Themengebiet",
                         "amount": "Anzahl der Artikel"
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Ranking-Ressort', methods=['GET'])
def chart7():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Fülle alle NaN Werte aus `rankings` mit einem leeren Array
    df['rankings'] = df['rankings'].fillna("[]")

    # Ändere die Spalte `ressort` zu einem Anfangsgroßbuchstaben
    df['ressort'] = df['ressort'].str.title()

    # Ändere das Ressort der Artikel ohne Zuordnung zu `(Kein Ressort)`
    df.ressort = df.ressort.replace(r'\s+|^$', "(Kein Ressort)", regex=True)

    # Füge ein neues Feature hinzu: Ranking besser als 5. Platz
    def high_ranking(x):
        if (type(x) == list):
            return any(ranking['score'] <= 5 for ranking in x)
        return False

    df['high_ranking'] = df['rankings'].apply(high_ranking)

    # Filter die Artikel nach: Hohes Ranking vorhanden
    df = df.loc[df.high_ranking]

    # Gruppiere die Artikel nach: Themengebiet
    df_ressort = df.groupby(["ressort"]).size().reset_index(name='amount')

    # Sortiere die Artikel nach: Anzahl Top-Rankings (absteigend)
    df_ressort = df_ressort.sort_values(by='amount', ascending=False)

    fig = px.bar(df_ressort, x='ressort', y='amount', title="Anzahl der Artikel mit Ranking auf den ersten 5 Plätzen",
                 labels={"ressort": "Ressort",
                         "amount": "Anzahl der Artikel"
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Thema-&-Ressort', methods=['GET'])
def chart6():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Ändere die Spalte `ressort` zu einem Anfangsgroßbuchstaben
    df.ressort = df.ressort.str.title()

    # Ändere das Ressort der Artikel ohne Zuordnung zu `(Kein Ressort)`
    df.ressort = df.ressort.replace(r'\s+|^$', "(Kein Ressort)", regex=True)

    # Zähle die Artikel pro Themengebiet
    df_topic = df.topic.value_counts().reset_index(name="amount")
    df_topic['color'] = "#f2cc8f"  # ORANGE
    df_topic['edgecolor'] = "#e07a5f"  # ORANGE
    df_topic['type'] = "topic"

    # Zähle die Artikel pro Ressort
    df_ressort = df.ressort.value_counts().reset_index(name="amount")
    df_ressort['color'] = "#8ecae6"  # BLUE
    df_ressort['edgecolor'] = "#219ebc"  # BLUE
    df_ressort['type'] = "Ressort"

    # Füge die beiden enstandenen Daten in einen `DataFrame`
    df = pd.concat([df_ressort, df_topic])

    # Sortiere die Anzahl der Artikel pro Themengebiet/Ressort (absteigend)
    df = df.sort_values("amount", ascending=False)

    # Benenne das Feature `index` zu `group`
    df['group'] = df['index']

    fig = px.bar(df, x='group', y='amount', color="color", title="Anzahl der Artikel nach Thema",
                 labels={"index": "Thema",
                         "color": "Art",
                         "amount": "Anzahl der Artikel",
                         "group": "Themengebiete und Ressorts"
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Thema', methods=['GET'])
def chart5():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Zähle die Artikel pro Themengebiet
    df_topic = df.topic.value_counts().reset_index(name="amount")

    fig = px.bar(df_topic, x='index', y='amount', title="Anzahl der Artikel nach Thema",
                 labels={"index": "Thema",
                         "amount": "Anzahl der Artikel"
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Länge-Thema', methods=['GET'])
def chart4():
    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge zwei neue Features hinzu: Anzahl Wörter, Anzahl Zeichen
    df['content_length'] = df['content'].str.len()
    df['content_words'] = df['content'].str.split().map(len)

    # Füge ein neues Feature hinzu: Themengebiet
    topics = json.loads(open("data-topics/topics.json", "r").read())

    df['tags_full'] = ['; '.join(tags) for tags in df['tags'].to_list()]

    for topic in topics:
        df.loc[(df.title.str.contains('|'.join(topics[topic]['keywords'])) | df.tags_full.str.contains(
            '|'.join(topics[topic]['keywords']))), 'topic'] = topics[topic]['name']

    # Gruppiere die Artikel nach: Themengebiet
    # Aggregiere pro Themengebiet die Durchschnittsanzahl Wörter/Zeichen
    df = df.groupby(['topic']).agg(
        {"content_length": "mean", "content_words": "mean"})

    # Sortiere die Artikel nach: Anzahl Zeichen (absteigend)
    df = df.sort_values("content_length", ascending=False)

    fig = px.bar(df, y=['content_length', 'content_words'], labels={
        "content_length": "Anzahl der Zeichen",
        "content_words": "Anzahl der Wörter",
        "topic": "Thema",
        "value": "Textlänge"
    }, title="Durchschnittliche Textlänge nach Thema",
        barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Ressort', methods=['GET'])
def chart1():

    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Ändere die Spalte `ressort` zu einem Anfangsgroßbuchstaben
    df.ressort = df.ressort.str.title()

    # Ändere das Ressort der Artikel ohne Zuordnung zu `(Kein Ressort)`
    df.ressort = df.ressort.replace(r'\s+|^$', "(Kein Ressort)", regex=True)

    df = df.ressort.value_counts().reset_index(name="amount")

    df['color'] = "#8ecae6"  # BLUE
    df['edgecolor'] = "#219ebc"  # BLUE

    fig = px.bar(df, x='index', y='amount', color="color", title="Anzahl der Artikel nach Ressort",
                 labels={"index": "Ressort",
                         "amount": "Anzahl der Artikel"
                         },
                 barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Tag', methods=['GET'])
def chart2():

    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    df = (pd.to_datetime(df['date'])
          .dt.floor('d')
          .value_counts()
          .rename_axis('date')
          .reset_index(name='count')
          .sort_values('date'))

    fig = px.bar(df, x='date', y='count', labels={
        "date": "Datum",
        "count": "Anzahl der Artikel"
    }, title="Anzahl der Artikel pro Tag",
        barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@diagram_api.route('/Artikel-Länge-Ressort', methods=['GET'])
def chart3():

    df = getDataframe()

    # Filter die Artikel nach: Sind zwischen dem und dem Datum veröffentlich worden.
    df = df.loc[(df['date'] >= date_begin)]

    # Füge ein neues Feature hinzu: Anzahl Wörter, Anzahl Zeichen
    df['content_length'] = df['content'].str.len()
    df['content_words'] = df['content'].str.split().map(len)

    # Ändere die Spalte `ressort` zu einem Anfangsgroßbuchstaben
    df.ressort = df.ressort.str.title()

    # Ändere das Ressort der Artikel ohne Zuordnung zu `(Kein Ressort)`
    df.ressort = df.ressort.replace(r'\s+|^$', "(Kein Ressort)", regex=True)

    # Gruppiere die Artikel nach: Ressort
    # Aggregiere pro Ressort die Durchschnittsanzahl Zeichen/Wörter
    df = df.groupby(['ressort']).agg(
        {"content_length": "mean", "content_words": "mean"})

    # Sortiere die Artikel nach: Anzahl Zeichen (absteigend)
    df = df.sort_values("content_length", ascending=False)

    fig = px.bar(df, y=['content_length', 'content_words'], labels={
        "content_length": "Anzahl der Zeichen",
        "content_words": "Anzahl der Wörter",
        "ressort": "Ressort",
        "value": "Textlänge"
    }, title="Durchschnittliche Textlänge nach Ressort",
        barmode='group', height=height)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
