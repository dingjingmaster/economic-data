import os
import pandas as pd


def read_fun_data(path: str):
    f = {}
    if os.path.exists(path):
        try:
            o = pd.read_csv(path, sep='|').values.tolist()
            for line in o:
                f[line[0]] = (line[1], line[2])
            return f
        except Exception as e:
            print(e)
            return None
    return None


def read_fun_data_as_df(path: str):
    if os.path.exists(path):
        try:
            return pd.read_csv(path, sep='|')
        except Exception as e:
            print(e)
            return None
    return None
