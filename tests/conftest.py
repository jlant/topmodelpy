"""Test configurations and fixtures."""

from configparser import ConfigParser, ExtendedInterpolation
import os
import numpy as np
import pandas as pd
import pytest
from pathlib import Path


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
        "snowmelt_rate_coeff_with_rain": 0.007,
        "channel_length_max": 1.98,
        "channel_velocity_avg": 10,
        "flow_initial": 1
    }

    return data


@pytest.fixture(scope="module")
def modelconfig_obj():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config["Inputs"] = {
        "input_dir": Path.cwd(),
        "parameters_file": "${Inputs:input_dir}/parameters.csv",
        "timeseries_file": "${Inputs:input_dir}/timeseries.csv",
        "twi_file": "${Inputs:input_dir}/twi.csv",
    }

    config["Outputs"] = {
        "output_dir": Path.cwd(),
    }

    config["Options"] = {
        "option_pet": "hamon",
        "option_snowmelt_with_precip": "heavily_forested",
        "option_snowmelt_with_no_precip": "temperature_index",
    }

    return config


@pytest.fixture(scope="module")
def modelconfig_obj_invalid_sections():
    return ConfigParser(interpolation=ExtendedInterpolation())


@pytest.fixture(scope="module")
def modelconfig_obj_invalid_filepath():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config["Inputs"] = {
        "input_dir": Path.cwd(),
        "parameters_file": "some/bad/filepath/",
        "timeseries_file": "${Inputs:input_dir}/timeseries.csv",
        "twi_file": "${Inputs:input_dir}/twi.csv",
    }

    config["Outputs"] = {
        "output_dir": "",
    }

    config["Options"] = {
        "option_pet": "hamon",
        "option_snowmelt_with_precip": "heavily_forested",
        "option_snowmelt_with_no_precip": "temperature_index",
    }

    return config


@pytest.fixture(scope="module")
def modelconfig_obj_invalid_options():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config["Inputs"] = {
        "input_dir": Path.cwd(),
        "parameters_file": "${Inputs:input_dir}/parameters.csv",
        "timeseries_file": "${Inputs:input_dir}/timeseries.csv",
        "twi_file": "${Inputs:input_dir}/twi.csv",
    }

    config["Outputs"] = {
        "output_dir": Path.cwd(),
    }

    config["Options"] = {
        "option_pet": "yes",
        "option_snowmelt_with_precip": "snow",
        "option_snowmelt_with_no_precip": "hello",
    }

    return config


@pytest.fixture(scope="module")
def parameters_file():
    return ("""name,value,units,description
scaling_parameter,10,millimeters,a description
saturated_hydraulic_conductivity,150,millimeters/day,a description
macropore_fraction,0.2,fraction,a description
soil_depth_total,1,meters,a description
soil_depth_ab_horizon,0.7,meters,a description
field_capacity_fraction,0.2,fraction,a description
latitude,40.5,degrees,a description
basin_area_total,3.5,square kilometers,a description
impervious_area_fraction,0.3,fraction,a description
snowmelt_temperature_cutoff,-32,degrees fahrenheit,a description
snowmelt_rate_coeff,0.06,1/degrees fahrenheit,a description
snowmelt_rate_coeff_with_rain,7E-3,inches per degree fahrenheit,a description
channel_length_max,5,kilometers,a description
channel_velocity_avg,19,kilometers/day,a description
flow_initial,1,millimeters/day,a description
""")


@pytest.fixture(scope="module")
def parameters_file_invalid_header():
    return ("""names,val,unit,descr
scaling_parameter,10,millimeters,a description
saturated_hydraulic_conductivity,150,millimeters/day,a description
macropore_fraction,0.2,fraction,a description
soil_depth_total,1,meters,a description
soil_depth_ab_horizon,0.7,meters,a description
field_capacity_fraction,0.2,fraction,a description
latitude,40.5,degrees,a description
basin_area_total,3.5,square kilometers,a description
impervious_area_fraction,0.3,fraction,a description
snowmelt_temperature_cutoff,-32,degrees fahrenheit,a description
snowmelt_rate_coeff,0.06,1/degrees fahrenheit,a description
snowmelt_rate_coeff_with_rain,7E-3,inches per degree fahrenheit,a description
channel_length_max,5,kilometers,a description
channel_velocity_avg,19,kilometers/day,a description
flow_initial,1,millimeters/day,a description
""")


@pytest.fixture(scope="module")
def timeseries_file():
    return ("""date,temperature (celsius),precipitation (mm/day),pet (mm/day),flow_observed (mm/day)
2019-01-01,1.0,2.0,3.0,4.0
2019-01-02,1.1,2.1,3.1,4.1
2019-01-03,1.2,2.2,3.2,4.2
2019-01-04,1.3,2.3,3.3,4.3
2019-01-05,1.4,2.4,3.4,4.4
""")


@pytest.fixture(scope="module")
def timeseries_file_invalid_header():
    return ("""date,temperature (fahrenheit),precipitation (mm/day),pet (mm/day),flow observed (mm/day)
2019-01-01,1.0,2.0,3.0,4.0
2019-01-02,1.1,2.1,3.1,4.1
2019-01-03,1.2,2.2,3.2,4.2
2019-01-04,1.3,2.3,3.3,4.3
2019-01-05,1.4,2.4,3.4,4.4
""")


@pytest.fixture(scope="module")
def timeseries_file_missing_dates():
    return ("""date,temperature (celsius),precipitation (mm/day),pet (mm/day),flow_observed (mm/day)
2019-01-01,1.0,2.0,3.0,4.0
,1.1,2.1,3.1,4.1
2019-01-03,1.2,2.2,3.2,4.2
2019-01-04,1.3,2.3,3.3,4.3
,1.4,2.4,3.4,4.4
""")


@pytest.fixture(scope="module")
def timeseries_file_missing_values():
    return ("""date,temperature (celsius),precipitation (mm/day),pet (mm/day),flow_observed (mm/day)
2019-01-01,1.0,2.0,3.0,
2019-01-02,1.1,2.1,3.1,4.1
2019-01-03,,2.2,3.2,4.2
2019-01-04,1.3,2.3,3.3,4.3
2019-01-05,1.4,2.4,3.4,4.4
""")


@pytest.fixture(scope="module")
def timeseries_file_invalid_timestep():
    return ("""date,temperature (celsius),precipitation (mm/day),pet (mm/day),flow_observed (mm/day)
2019-01-01,1.0,2.0,3.0,4.0
2019-02-01,1.1,2.1,3.1,4.1
2019-03-01,1,2.2,3.2,4.2
2019-04-01,1.3,2.3,3.3,4.3
2019-05-01,1.4,2.4,3.4,4.4
""")


@pytest.fixture(scope="module")
def twi_file():
    return ("""bin,twi,proportion,cells
1,0.02,0.10,10
2,0.03,0.15,15
3,0.04,0.25,25
4,0.05,0.30,30
5,0.06,0.20,20
""")


@pytest.fixture(scope="module")
def twi_file_invalid_header():
    return ("""bin,value,proportion,cells
1,0.02,0.10,10
2,0.03,0.15,15
3,0.04,0.25,25
4,0.05,0.30,30
5,0.06,0.20,20
""")


@pytest.fixture(scope="module")
def twi_file_missing_values():
    return ("""bin,twi,proportion,cells
1,0.02,0.10,
2,0.03,0.15,15
3,0.04,0.25,25
4,0.05,0.30,30
5,,0.20,20
""")


@pytest.fixture(scope="module")
def twi_file_invalid_proportion():
    return ("""bin,twi,proportion,cells
1,0.02,0.10,10
2,0.03,0.15,15
3,0.04,0.25,25
4,0.05,0.30,30
5,0.06,0.22,20
""")


@pytest.fixture(scope="module")
def observed_data():
    return np.array([55.7, 62.0, 65.5, 64.7, 61.1])


@pytest.fixture(scope="module")
def modeled_data():
    return np.array([55.5, 62.1, 65.3, 64.4, 61.2])
