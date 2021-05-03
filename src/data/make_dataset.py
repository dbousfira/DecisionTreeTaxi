import os
import re
import requests
import zipfile

DATA_PATH = "../data/"


def dl(output_file, url):
    zip = f"{DATA_PATH}{output_file}"
    open(zip, 'wb').write(requests.get(url).content)


def extract(zip):
    """Let’s extract it."""
    with zipfile.ZipFile(f"{DATA_PATH}raw/{zip}", 'r') as zip_ref:
        zip_ref.extractall(f"{DATA_PATH}interim")
        extracted = zip_ref.namelist()

    return os.path.join(f"{DATA_PATH}interim", extracted[0])


def reduce_mem_usg_pd(df, dates=[]):
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

    cols = list(df.describe().transpose().index)
    for col in cols:
        col_dtype = re.sub(r'[0-9]+', '', df[col].dtype.name)

        max = df[col].max()
        min = df[col].min()

        # int, float
        for dtype in dtypes:
            if dtype == col_dtype:
                for d in dtypes[dtype]:
                    min_max = dtypes[dtype][d]
                    if min > min_max[0] and max < min_max[1]:
                        df[col] = df[col].astype(d)
                        break

                break

    return df
