
import os
import pandas as pd
from configparser import ConfigParser


CONFIG = ConfigParser()
files = CONFIG.read('config.ini')


ENV = os.environ['ENV']


def getConfig(config_name: str) -> str:
    return CONFIG.get(ENV, config_name)


def getDataframe():
    df = pd.read_json(getConfig("database_file"))

    df['date'] = pd.to_datetime(
        df.date, format='%Y-%m-%dT%H:%M:%S.%f', utc=True)

    return df
