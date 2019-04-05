"""Module that contains functions to read a twi file in csv format."""

import numpy as np
import pandas as pd

from .exceptions import (TwiFileErrorInvalidHeader,
                         TwiFileErrorMissingValues,
                         TwiFileErrorInvalidProportion)


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
    except TwiFileErrorInvalidHeader as err:
        print(err)
    except TwiFileErrorMissingValues as err:
        print(err)
    except TwiFileErrorInvalidProportion as err:
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
    column_names = {
        "bin": "bin",
        "twi": "twi",
        "proportion": "proportion",
        "cells": "cells",
    }

    data = pd.read_csv(filestream, dtype=float)
    data.columns = data.columns.str.strip()
    check_header(data.columns.values.tolist(), list(column_names))
    check_missing_values(data)
    check_proportion(data)
    data.rename(columns=column_names, inplace=True)

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
            raise TwiFileErrorInvalidHeader(header, valid_header)


def check_missing_values(data):
    """Check if any data is missing.

    :param data: Pandas DataFrame containing data.
    :type data: pandas.DataFrame
    """
    if data.isnull().values.any():
        missing_values = data[data.isna().any(axis=1)]
        raise TwiFileErrorMissingValues(missing_values)


def check_proportion(data):
    """Check that the sum of proportion column is close to 1.0.
    rtol=1e-02 means that computed sum should be within 1% of 1.0

    :param data: Pandas DataFrame containing data.
    :type data: pandas.DataFrame
    """
    if not np.isclose(data["proportion"].sum(), 1.0, rtol=1e-02):
        raise TwiFileErrorInvalidProportion(data["proportion"].sum())
