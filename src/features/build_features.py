import pandas as pd
import numpy as np
import re


def reduce_mem_usg_pd(df):
    """Reducing memory usage in pandas with smaller datatypes.

    Optimizing pandas memory usage by the effective use of datatypes.
    Args:
        df (DataFrame): large dataset

    Returns:
        DataFrame: optimize dataset

    Todo:
        Object -> categorical
    """
    dtypes = {
        "int": {
            "int8": [-128, 127],
            "int16": [-32768, 32767],
            "int32": [-2147483648, 2147483647],
            "int64": [-9223372036854775808, 9223372036854775807]
        },
        "float": {
            "float16": [-32768, 32767],
            "float32": [-2147483648, 2147483647],
            "float64": [-9223372036854775808, 9223372036854775807]}
        }

    numerical_cols = list(df.describe().transpose().index)
    print(f"Memory usage: {df.memory_usage(index=False, deep=True)}")
    for col in numerical_cols:
        max = df[col].max()
        min = df[col].min()

        col_dtype = re.sub(r'[0-9]+', '', df[col].dtype.name)
        # int, float
        for dtype in dtypes:
            if dtype == col_dtype:
                for d in dtypes[dtype]:
                    min_max = dtypes[dtype][d]
                    if min > min_max[0] and max < min_max[1]:
                        df[col] = df[col].astype(d)
                        break

                break

    print(f"Memory usage: {df.memory_usage(index=False, deep=True)}")

    return df


def remove_outliers(df, cols):
    i = 0
    for col in cols:
        print(col)
        print(f"Before filtering: {df.shape}")
        df = df[(df[col] > cols[col][0]) & (df[col] < cols[col][
            1])]
        print(f"After filtering: {df.shape}")

    return df


def split_datetime(df, col):
    col_name = df.columns[col]
    # Split datetime column
    datetime = pd.to_datetime(df[col_name])
    df['day_of_week'] = datetime.dt.dayofweek
    df['day_of_month'] = datetime.dt.day
    df['month'] = datetime.dt.month
    df['year'] = datetime.dt.year
    df['hour'] = datetime.dt.hour + datetime.dt.minute / 60

    return df


def compute_distance(lat1, lon1, lat2, lon2):
    R = 6372800  # Earth radius in meters

    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    total_distance = 6372800 * c

    # return np.rint(total_distance/1000)
    return total_distance / 1000