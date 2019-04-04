"""Module that contains functions to read a timeseries file in csv format."""

import pandas as pd

from .exceptions import (TimeseriesFileErrorInvalidHeader)


def read(filepath):
    """Read data file
    Open file and create a file object to process with
    read_file_in(filestream).

    :param filepath: File path to data file.
    :type param: string
    :return data: A dict that contains all the data from the file.
    :rtype: dict
    """
    try:
        with open(filepath, "r") as f:
            data = read_in(f)
        return data
    except TimeseriesFileErrorInvalidHeader as err:
        print(err)
    except Exception as err:
        print(err)


def read_in(filestream):
    """Read and process a filestream.
    Read and process a filestream of a comma-delimited parameter file.
    This function takes a filestream of text as input which allows for
    cleaner unit testing.

    :param filestream: A filestream of text.
    :type filestream: _io.TextIOWrapper
    :return data: A dict that contains all the data from the file.
    :rtype: dict
    """
    column_short_names = {
        "temperature (celsius)": "temperature",
        "precipitation (mm/day)": "precipitation",
        "pet (mm/day)": "pet",
        "flow observed (mm/day)": "flow_observed",
    }

    data = pd.read_csv(filestream, index_col=0, parse_dates=True, dtype=float)
    check_header(data.columns.values.tolist(), list(column_short_names))
    data.rename(columns=column_short_names, inplace=True)

    return data


def check_header(header, valid_header):
    """Check that column names in header line match what is expected.

    :param header: Header found in file.
    :type header: list
    :param valid_header: Valid header that is expected.
    :type valid_header: list
    """
    for item in header:
        if item not in valid_header:
            raise TimeseriesFileErrorInvalidHeader(header, valid_header)


if __name__ == "__main__":
    data = read("timeseries.csv")
    print(data)
    print(data.dtypes)
