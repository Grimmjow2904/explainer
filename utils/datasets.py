import base64
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


def save_dataset(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    if name.endswith(".csv"):
        try:
            data = content.encode("utf8").split(b";base64,")[1]
            with open(os.path.join(settings.data_path, name), "wb") as fp:
                fp.write(base64.decodebytes(data))
            return True
        except Exception as error:
            print(error)
            return False
    else:
        return False
