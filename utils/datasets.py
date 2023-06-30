import os
import pandas as pd

from enviroment import settings


def getDatasets():
    return os.listdir(settings.data_path)


def getDataset(name):
    return pd.read_csv(
        settings.data_path + "//" + name
    )
