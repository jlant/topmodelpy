"""Module for reading a model configuration file.

The configuration file is in the standard INI file format. The file contains
three sections:
1. Inputs - section for model input files
2. Outputs - section for model output files
3. Options - section for model options
"""

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

from .exceptions import InvalidModelConfigFileInvalidSections


def read(filepath):
    """Read model config file.

    Read and process the model configuration file that is in the standard INI
    data format.

    :param filepath: A valid file path
    :type filepath: string
    :return: A ConfigParser object that behaves much like a dictionary.
    :rtype: ConfigParser

    Returns
    -------
    ConfigParser
        A ConfigParser object that behaves much like a dictionary.

    """
    filepath = Path(filepath)
    try:
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(filepath)
        check_config(config)
    except IOError as err:
        print(err)
    except ValueError as err:
        print(err)
    except InvalidModelConfigFileInvalidSections as err:
        print(err)
    except Exception as err:
        print(err)

    return config


def check_config(config):
    """ Check that the config file has data and that all file paths are valid.

    :param config: A ConfigParser object that behaves much like a dictionary.
    :type config: ConfigParser
    """
    check_config_sections(config)
    check_config_filepaths(config)
    check_config_options(config)


def check_config_sections(config):
    """Check that the config file has sections."""
    valid_sections = ["Inputs", "Outputs", "Options"]
    sections = config.sections()
    if not sections == valid_sections:
        raise InvalidModelConfigFileInvalidSections(valid_sections, sections)


def check_config_filepaths(config):
    """Check that all the filepaths are valid."""
    for section in config.sections():
        for key in config[section]:
            value = config[section][key]
            if value and (key.endswith("dir") or key.endswith("file")):
                filepath = Path(value)
                if not filepath.exists() and not filepath.is_file():
                    error_msg = ("Error with model config file.\n"
                                 "Invalid file path: {}".format(value))
                    raise IOError(error_msg)


def check_config_options(config):
    """Check that all the options are valid."""
    valid_options_pet = ["hamon"]
    valid_options_snowmelt_with_precip = ["heavily_forested",
                                          "partly_forested"]
    valid_options_snowmelt_with_no_precip = ["temperature_index"]

    option_pet = (
        config["Options"]["option_pet"].lower().strip())
    option_snowmelt_with_precip = (
        config["Options"]["option_snowmelt_with_precip"].lower().strip())
    option_snowmelt_with_no_precip = (
        config["Options"]["option_snowmelt_with_no_precip"].lower().strip())

    error_msg = (
        """
Error with model config file.
Valid options are:
  option_pet = hamon
  option_snowmelt_with_precip = heavily_forested or
                                partly_forested
  option_snowmelt_with_no_precip = temperature_index
Options specified are:
  option_pet = {}
  option_snowmelt_with_precip = {}
  option_snowmelt_with_no_precip = {}
        """.format(option_pet,
                   option_snowmelt_with_precip,
                   option_snowmelt_with_no_precip)
    )

    if option_pet not in valid_options_pet:
        raise ValueError(error_msg)
    if option_snowmelt_with_precip not in valid_options_snowmelt_with_precip:
        raise ValueError(error_msg)
    if option_snowmelt_with_no_precip not in valid_options_snowmelt_with_no_precip:
        raise ValueError(error_msg)
