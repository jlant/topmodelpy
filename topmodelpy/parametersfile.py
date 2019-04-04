"""Module that contains functions to read a parameters file in csv format."""

import csv

from .exceptions import (ParametersFileErrorInvalidHeader,
                         ParametersFileErrorInvalidScalingParameter,
                         ParametersFileErrorInvalidLatitude,
                         ParametersFileErrorInvalidSoilDepthTotal,
                         ParametersFileErrorInvalidSoilDepthAB,
                         ParametersFileErrorInvalidFieldCapacity,
                         ParametersFileErrorInvalidMacropore,
                         ParametersFileErrorInvalidImperviousArea,)


def read(filepath):
    """Read data file
    Open file and create a file object to process with
    read_file_in(filestream).

    :param filepath: File path of data file.
    :type param: string
    :return data: A dict that contains all the data from the file.
    :rtype: dict
    """
    try:
        with open(filepath) as f:
            data = read_in(f)
        check_data(data)
        return data
    except (ParametersFileErrorInvalidHeader,
            ParametersFileErrorInvalidScalingParameter,
            ParametersFileErrorInvalidLatitude,
            ParametersFileErrorInvalidSoilDepthTotal,
            ParametersFileErrorInvalidSoilDepthAB,
            ParametersFileErrorInvalidFieldCapacity,
            ParametersFileErrorInvalidMacropore,
            ParametersFileErrorInvalidImperviousArea,) as err:
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
    fnames = ["name", "value", "units", "description"]
    reader = csv.DictReader(filestream, fieldnames=fnames)
    header = next(reader)
    header_list = [val.lower().strip() for val in header.values()]
    check_header(header_list, fnames)

    data = {}
    for row in reader:
        name = row["name"].lower().strip()
        data[name] = {
            "value": float(row["value"].strip()),
            "units": row["units"].lower().strip(),
            "description": row["description"].strip(),
        }
    return data


def check_header(header, valid_header):
    """Check that column names in header line match what is expected.

    :param header: Header found in file.
    :type header: list
    :param valid_header: Valid header that is expected.
    :type valid_header: list
    """
    if not header == valid_header:
        raise ParametersFileErrorInvalidHeader(header, valid_header)


def check_data(data):
    """Check that all data values from the file are valid.

    :param data: A dict that contains all the data from the file.
    :type data: dict
    """
    check_scaling_parameter(data["scaling_parameter"]["value"])
    check_latitude(data["latitude"]["value"])
    check_soil_depth_total(data["soil_depth_total"]["value"])
    check_soil_depth_ab_horizon(data["soil_depth_ab_horizon"]["value"],
                                data["soil_depth_total"]["value"])
    check_field_capacity(data["field_capacity_fraction"]["value"])
    check_macropore(data["macropore_fraction"]["value"])
    check_impervious_area(data["impervious_area_fraction"]["value"])


def check_scaling_parameter(value):
    """Check that the scaling parameter value is valid.
    Valid scaling parameter value is:
        scaling_parameter > 0

    :param value: scaling parameter value.
    :type value: float
    """
    if not value > 0:
        raise ParametersFileErrorInvalidScalingParameter(value)


def check_latitude(value):
    """Check that the latitude value is valid.
    Valid latitude value are:
      90 >= latitude >= 0

    :param value: latitude value.
    :type value: float
    """
    if not value >= 0 or not value <= 90:
        raise ParametersFileErrorInvalidLatitude(value)


def check_soil_depth_total(value):
    """Check that the soil_depth_total value is valid.
    Valid soil depth value are:
      soil_depth_total > 0

    :param value: soil depth total value.
    :type value: float
    """
    if not value > 0:
        raise ParametersFileErrorInvalidSoilDepthTotal(value)


def check_soil_depth_ab_horizon(value, soil_depth_total):
    """Check that the soil_depth_ab_horizon value is valid.
    Valid soil depth of AB horizon value are:
      soil_depth_ab_horizon > 0
      soil_depth_ab_horizon < soil_depth_total

    :param value: soil depth ab horizon value.
    :type value: float
    """
    if not value > 0 or not value < soil_depth_total:
        raise ParametersFileErrorInvalidSoilDepthAB(value, soil_depth_total)


def check_field_capacity(value):
    """Check that the field capacity fraction value is valid.
    Valid field capacity fraction value are:
      0 <= field_capacity <= 1

    :param value: field capacity value.
    :type value: float
    """
    if not value > 0 or not value < 1:
        raise ParametersFileErrorInvalidFieldCapacity(value)


def check_macropore(value):
    """Check that the macropore value is valid.
    Valid macropore fraction value are:
      0 <= macropore <= 1

    :param value: macropore value.
    :type value: float
    """
    if not value > 0 or not value < 1:
        raise ParametersFileErrorInvalidMacropore(value)


def check_impervious_area(value):
    """Check that the impervious_area value is valid.
    Valid impervious_area fraction value are:
      0 <= impervious_area_fraction <= 1

    :param value: impervious area value.
    :type value: float
    """
    if not value > 0 or not value < 1:
        raise ParametersFileErrorInvalidImperviousArea(value)
