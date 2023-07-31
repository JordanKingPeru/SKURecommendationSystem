import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi


def read_kaggle_data(competition, filename):
    """Descarga y lee un archivo de datos de una competencia de Kaggle."""
    api = KaggleApi()
    api.authenticate()

    api.competition_download_file(competition, filename)

    # Descomprime el archivo si es necesario
    if filename.endswith('.zip'):
        os.system(f'unzip {filename}')
        filename = filename[:-4]  # remove .zip from the filename

    return pd.read_csv(filename)


def make_submission_kaggle(competition, filename, message):
    """Hace un envío a una competencia de Kaggle."""
    api = KaggleApi()
    api.authenticate()

    api.competition_submit(filename, message, competition)