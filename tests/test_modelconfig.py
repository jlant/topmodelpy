
"""Tests for read_modelconfig module.
"""

import pytest
import os

from topmodelpy import modelconfig


def test_raises_exception_bad_file(modelconfig_obj_empty):

    filepath = "some/filepath/bad_file.txt"
    msg = ("Error with modelconfig file.")
    with pytest.raises(ValueError) as err:
        modelconfig.read(filepath)


def test_modelconfig_obj(modelconfig_obj):

    # Testing a sample of the file that have different value types, i.e. paths,
    # None values, Boolean, etc.
    expected_sections = ["Inputs", "Outputs", "Options"]

    expected_model_type = "topmodel_wolock"

    expected_input_dir = "/home/jlantl/jeremiah/projects/waterpy/data/inputs"
    expected_model_parameters_csv_file = os.path.join(expected_input_dir,
                                                      "model_parameters.csv")
    expected_pet_file = ""
    expected_option_pet_hamon = "yes"
    expected_option_pet_hamon_bool = True

    actual_sections = modelconfig_obj.sections()
    actual_model_type = model_config_obj["Inputs"]["model_type"]
    actual_input_dir = model_config_obj["Inputs"]["input_dir"]
    actual_model_parameters_csv_file = model_config_obj["Inputs"]["model_parameters_csv_file"]
    actual_pet_file = model_config_obj["Inputs"]["pet_csv_file"]
    actual_option_pet_hamon = model_config_obj["Options"]["option_pet_hamon"]
    actual_option_pet_hamon_bool = model_config_obj["Options"].getboolean("option_pet_hamon")

    assert actual_sections == expected_sections
    assert actual_model_type == expected_model_type
    assert actual_input_dir == expected_input_dir
    assert actual_model_parameters_csv_file == expected_model_parameters_csv_file
    assert actual_pet_file == expected_pet_file
    assert actual_option_pet_hamon == expected_option_pet_hamon
    assert actual_option_pet_hamon_bool== expected_option_pet_hamon_bool
