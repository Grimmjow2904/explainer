import os
import pandas as pd

from enviroment import settings


def getDatasets():
    data = [os.listdir(settings.data_path)]
    targets = []
    for i in data[0]:
        dataset = pd.read_csv(
            settings.data_path + "//" + i)
        targets.append(dataset.columns.values[-1])
    data.append(targets)
    return data


def getDataset(name):
    return pd.read_csv(
        settings.data_path + "//" + name
    )
