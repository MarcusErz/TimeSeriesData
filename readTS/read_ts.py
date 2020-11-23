import pandas as pd


def split_up_ts(path):
    ts_pd_data = pd.read_csv(path)
    ts_data = ts_pd_data.to_numpy()
    ts_data_dates = ts_data[:, 0].astype('datetime64', copy=False)
    ts_data_values = ts_data[:, 1]
    ts_data_outliers = ts_data[:, -1]
    return ts_data_dates, ts_data_values, ts_data_outliers
