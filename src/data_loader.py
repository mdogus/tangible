import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def load_data_with_delimiter(file_path, delimiter):
    df = pd.read_csv(file_path, delimiter=delimiter)
    return df
