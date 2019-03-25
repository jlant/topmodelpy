"""Test configurations and fixtures."""

from configparser import ConfigParser, ExtendedInterpolation
import os
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def timeseries_wolock():
    """Return a Pandas dataframe of timeseries test data
    from Dave Wolock's Topmodel version. Test data contains
    input values along with model output values in a single file.
    """

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/timeseries_wolock.csv")
    data = pd.read_csv(fname,
                       names=["date",
                              "temperature",
                              "precipitation",
                              "pet",
                              "precip_minus_pet",
                              "flow_observed",
                              "flow_predicted"],
                       header=0)  # skip header

    return data


@pytest.fixture(scope="module")
def twi_wolock():
    """Return a Pandas dataframe of twi test data
    from Dave Wolock's Topmodel version"""

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/twi_wolock.csv")
    data = pd.read_csv(fname,
                       names=["bin",
                              "twi",
                              "proportion",
                              "cells"],
                       header=0)  # skip header

    return data


@pytest.fixture(scope="module")
def twi_weighted_mean_wolock():
    """Return the weighted mean of the twi test data
    from Dave Wolock's Topmodel version"""

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/twi_wolock.csv")
    data = pd.read_csv(fname,
                       names=["bin",
                              "twi",
                              "proportion",
                              "cells"],
                       header=0)  # skip header

    twi_weighted_mean = (
        np.sum(data["twi"].values * data["proportion"].values)
        / np.sum(data["proportion"].values)
    )

    return twi_weighted_mean


@pytest.fixture(scope="module")
def parameters_wolock():
    """Return a dictionary of parameter test data
    from Dave Wolock's Topmodel version"""

    data = {
        "scaling_parameter": 10,
        "saturated_hydraulic_conductivity": 150,
        "macropore_fraction": 0.2,
        "soil_depth_total": 1,
        "soil_depth_ab_horizon": 0.5,
        "field_capacity_fraction": 0.2,
        "latitude": 40.5,
        "basin_area_total": 3.07,
        "impervious_area_fraction": 0.3,
        "snowmelt_temperature_cutoff": 32,
        "snowmelt_rate_coeff": 0.06,
        "snowmelt_rate_with_rain_coeff": 0.007,
        "channel_length_max": 1.98,
        "channel_velocity_avg": 10,
        "flow_initial": 1
    }

    return data


@pytest.fixture(scope="module")
def model_config_obj():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config["Inputs"] = {
        "input_dir": "./inputs",
        "parameters_file": "${Inputs:input_dir}/parameters.csv",
        "climate_file": "${Inputs:input_dir}/climate.csv",
        "twi_file": "${Inputs:input_dir}/twi.csv",
    }

    config["Outputs"] = {
        "output_dir": "./outputs",
    }

    config["Options"] = {
        "option_pet": "hamon",
        "option_snowmelt_with_precip": "heavily_forested",
        "option_snowmelt_with_no_precip": "temperature_index",
    }

    return config


@pytest.fixture(scope="module")
def modelconfig_obj_bad_paths():

    from configparser import ConfigParser, ExtendedInterpolation

    config = ConfigParser(interpolation=ExtendedInterpolation())

    config["Inputs"] = {
        "basin_chars_csv_file": __file__,
        "input_dir": "/some/path/that/does/not/exist",
        "pet_csv_file": "",
    }

    config["Outputs"] = {
        "output_dir": "/home/jlantl/jeremiah/projects/waterpy/data/outputs",
    }

    config["Options"] = {
        "pet_hamon": "yes",
    }

    return config
