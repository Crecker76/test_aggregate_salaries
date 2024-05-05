import bson
import pandas as pd
from datetime import datetime


def read_data_from_bson(file_path) -> list:
    """
    Read data from a BSON file

    Parameters:
    file_path (str): path to the BSON file

    Returns:
    list of dicts: data from the BSON file
    """

    with open(file_path, 'rb') as f:
        dt_data = bson.decode_all(f.read())
    return dt_data


def aggregate_salaries(data, dt_from, dt_upto, group_type) -> dict:
    """
    Aggregate salaries by specified group type (hour, day, month)

    Parameters:
    data (list of dicts): salary data
    dt_from (str): start date and time in ISO format
    dt_upto (str): end date and time in ISO format
    group_type (str): type of aggregation (hour, day, month)

    Returns:
    dict: aggregated dataset and labels
    """

    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)
    df = pd.DataFrame(data)
    df['dt'] = pd.to_datetime(df['dt'])
    df = df[(df['dt'] >= dt_from) & (df['dt'] <= dt_upto)]
    freq_data = {
        'hour': 'h',
        'day': 'D',
        'month': 'MS'
    }
    if group_type in freq_data:
        us_freq = freq_data[group_type]
    else:
        raise ValueError("Invalid group type")
    date_range = pd.date_range(dt_from, dt_upto, freq=us_freq)
    df_grouped = df.resample(us_freq, on='dt')['value'].sum().reindex(date_range, fill_value=0)

    labels = df_grouped.index.strftime('%Y-%m-%dT%H:%M:%S').tolist()
    dataset = df_grouped.values.tolist()
    return {'dataset': dataset, 'labels': labels}


DATA = read_data_from_bson(file_path='sample_collection.bson')
