
import json
import os
from datetime import datetime
from flask import Flask, Response, render_template

# data science imports
import pandas as pd
import plotly
import plotly.express as px

# import diagram api
from diagrams import diagram_api
from line_diagrams import line_diagram_api
from pages import pages

# other scripts
from lib import *


app = Flask(__name__)
app.register_blueprint(pages)
app.register_blueprint(diagram_api)
app.register_blueprint(line_diagram_api)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)
