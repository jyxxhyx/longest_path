import pandas as pd


def read(file_name):
    city_list = pd.read_csv(file_name)['city'].tolist()
    return city_list
