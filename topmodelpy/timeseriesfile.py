"""Module that contains functions to read a timeseries file in csv format."""

import numpy as np
import pandas as pd

from .exceptions import (TimeseriesFileErrorInvalidHeader,
                         TimeseriesFileErrorMissingDates,
                         TimeseriesFileErrorMissingValues,
                         TimeseriesFileErrorInvalidTimestep)


def read(filepath):
    """Read data file
    Open file and create a file object to process with
    read_file_in(filestream).

    :param filepath: File path to data file.
    :type param: string
    :return data: A dataframe of all the timeseries data.
    :rtype: Pandas.DataFrame
    """
    try:
        with open(filepath, "r") as f:
            data = read_in(f)
        return data
    except TimeseriesFileErrorInvalidHeader as err:
        print(err)
    except TimeseriesFileErrorMissingDates as err:
        print(err)
    except TimeseriesFileErrorMissingValues as err:
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
        "flow_observed (mm/day)": "flow_observed",
    }

    data = pd.read_csv(filestream, index_col=0, parse_dates=True, dtype=float)
    data.columns = data.columns.str.strip()
    check_header(data.columns.values.tolist(), list(column_short_names))
    check_missing_dates(data)
    check_missing_values(data)
    check_timestep(data)
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


def check_missing_dates(data):
    """Check for any missing dates."""
    if data.index.isna().any():
        missing_indices = np.where(data.index.isna())[0]
        timestamps_near_missing = data.index[missing_indices - 1]
        raise TimeseriesFileErrorMissingDates(timestamps_near_missing.values)


def check_missing_values(data):
    """Check for any missing data values."""
    if data.isna().values.any():
        missing_values = data[data.isna().any(axis=1)]
        raise TimeseriesFileErrorMissingValues(missing_values)


def check_timestep(data):
    """Check that the timestep is 1 day or less."""
    timestep = (data.index[1] - data.index[0]).days
    if not timestep <= 1:
        raise TimeseriesFileErrorInvalidTimestep(timestep)
