"""Tests for modelconfigfile module."""

import pytest
from pathlib import Path, PurePath

from waterpy.exceptions import (ModelConfigFileErrorInvalidSection,
                                   ModelConfigFileErrorInvalidFilePath,
                                   ModelConfigFileErrorInvalidOption)
from waterpy import modelconfigfile


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
    expected_option_snowmelt = True

    actual_sections = modelconfig_obj.sections()
    actual_input_dir = modelconfig_obj["Inputs"]["input_dir"]
    actual_parameters_file = modelconfig_obj["Inputs"]["parameters_file"]
    actual_timeseries_file = modelconfig_obj["Inputs"]["timeseries_file"]
    actual_twi_file = modelconfig_obj["Inputs"]["twi_file"]
    actual_output_dir = modelconfig_obj["Outputs"]["output_dir"]
    actual_option_pet = modelconfig_obj["Options"]["option_pet"]
    actual_option_snowmelt = modelconfig_obj["Options"].getboolean("option_snowmelt")

    assert actual_sections == expected_sections
    assert actual_input_dir == str(expected_input_dir)
    assert actual_parameters_file == str(expected_parameters_file)
    assert actual_timeseries_file == str(expected_timeseries_file)
    assert actual_twi_file == str(expected_twi_file)
    assert actual_output_dir == str(expected_output_dir)
    assert actual_option_pet == expected_option_pet
    assert actual_option_snowmelt == expected_option_snowmelt


def test_modelconfig_obj_no_sections(modelconfig_obj_invalid_sections):
    with pytest.raises(ModelConfigFileErrorInvalidSection) as err:
        modelconfigfile.check_config_sections(modelconfig_obj_invalid_sections)

    assert "Invalid section" in str(err.value)


def test_modelconfig_obj_invalid_filepath(modelconfig_obj_invalid_filepath):
    with pytest.raises(ModelConfigFileErrorInvalidFilePath) as err:
        modelconfigfile.check_config_filepaths(modelconfig_obj_invalid_filepath)

    assert "Invalid file path" in str(err.value)


def test_modelconfig_obj_invalid_options(modelconfig_obj_invalid_options):
    with pytest.raises(ModelConfigFileErrorInvalidOption) as err:
        modelconfigfile.check_config_options(modelconfig_obj_invalid_options)

    assert "Invalid option" in str(err.value)
