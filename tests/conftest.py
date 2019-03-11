"""Test configurations and fixtures."""

import os
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def wolock_timeseries_data():
    """Return a Pandas dataframe of timeseries test data
    from Dave Wolock's Topmodel version. Test data contains
    input values along with model output values in a single file.
    """

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/wolock_input_output_timeseries.csv")
    data = pd.read_csv(fname,
                       names=["date",
                              "precipitation",
                              "temperature",
                              "precip_minus_pet",
                              "pet",
                              "flow_observed",
                              "flow_predicted"],
                       header=0)  # skip header

    return data


@pytest.fixture(scope="module")
def wolock_twi_data():
    """Return a Pandas dataframe of twi test data
    from Dave Wolock's Topmodel version"""

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/wolock_twi.csv")
    data = pd.read_csv(fname,
                       names=["bin",
                              "twi",
                              "proportion",
                              "cells"],
                       header=0)  # skip header

    return data


@pytest.fixture(scope="module")
def wolock_twi_weighted_mean():
    """Return the weighted mean of the twi test data
    from Dave Wolock's Topmodel version"""

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/wolock_twi.csv")
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
def wolock_parameters_data():
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
