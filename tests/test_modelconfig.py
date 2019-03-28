"""Tests for modelconfig module.
"""

import pytest
from pathlib import Path, PurePath

from topmodelpy.exceptions import InvalidModelConfigFileInvalidSections
from topmodelpy import modelconfig


def test_modelconfig_obj(modelconfig_obj):
    expected_sections = ["Inputs", "Outputs", "Options"]
    expected_input_dir = Path.cwd()
    expected_parameters_file = PurePath(expected_input_dir).joinpath(
                                                    "parameters.csv")
    expected_timeseries_file = PurePath(expected_input_dir).joinpath(
                                                    "timeseries.csv")
    expected_twi_file = PurePath(expected_input_dir).joinpath(
                                                    "twi.csv")
    expected_output_dir = Path.cwd()
    expected_option_pet = "hamon"
    expected_option_snowmelt_with_precip = "heavily_forested"
    expected_option_snowmelt_with_no_precip = "temperature_index"

    actual_sections = modelconfig_obj.sections()
    actual_input_dir = modelconfig_obj["Inputs"]["input_dir"]
    actual_parameters_file = modelconfig_obj["Inputs"]["parameters_file"]
    actual_timeseries_file = modelconfig_obj["Inputs"]["timeseries_file"]
    actual_twi_file = modelconfig_obj["Inputs"]["twi_file"]
    actual_output_dir = modelconfig_obj["Outputs"]["output_dir"]
    actual_option_pet = modelconfig_obj["Options"]["option_pet"]
    actual_option_snowmelt_with_precip = modelconfig_obj["Options"][
        "option_snowmelt_with_precip"]
    actual_option_snowmelt_with_no_precip = modelconfig_obj["Options"][
        "option_snowmelt_with_no_precip"]

    assert actual_sections == expected_sections
    assert actual_input_dir == str(expected_input_dir)
    assert actual_parameters_file == str(expected_parameters_file)
    assert actual_timeseries_file == str(expected_timeseries_file)
    assert actual_twi_file == str(expected_twi_file)
    assert actual_output_dir == str(expected_output_dir)
    assert actual_option_pet == expected_option_pet
    assert actual_option_snowmelt_with_precip == expected_option_snowmelt_with_precip
    assert actual_option_snowmelt_with_no_precip == expected_option_snowmelt_with_no_precip


def test_modelconfig_obj_no_sections(modelconfig_obj_no_sections):
    with pytest.raises(InvalidModelConfigFileInvalidSections) as err:
        modelconfig.check_config_sections(modelconfig_obj_no_sections)

    #sections = modelconfig_obj_no_sections.sections()
    #assert str(err.value) == error_msg


def test_modelconfig_obj_bad_options(modelconfig_obj_bad_options):
    with pytest.raises(ValueError) as err:
        modelconfig.check_config_options(modelconfig_obj_bad_options)

    msg = (
        """
Error with model config file.
Valid options are:
  option_pet = hamon
  option_snowmelt_with_precip = heavily_forested or
                                partly_forested
  option_snowmelt_with_no_precip = temperature_index
Options specified are:
  option_pet = pet
  option_snowmelt_with_precip = snow
  option_snowmelt_with_no_precip = snow
        """
    )
    assert str(err.value) == msg


