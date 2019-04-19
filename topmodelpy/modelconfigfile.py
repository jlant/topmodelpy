"""Module for reading a model configuration file.

The configuration file is in the standard INI file format. The file contains
three sections:
1. Inputs - section for model input files
2. Outputs - section for model output files
3. Options - section for model options
"""

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

from .exceptions import (ModelConfigFileErrorInvalidSection,
                         ModelConfigFileErrorInvalidFilePath,
                         ModelConfigFileErrorInvalidOption)


def read(filepath):
    """Read model config file.

    Read and process the model configuration file that is in the standard INI
    data format.

    :param filepath: A valid file path
    :type filepath: string
    :return: A ConfigParser object that behaves much like a dictionary.
    :rtype: ConfigParser
    """
    filepath = Path(filepath)
    try:
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(filepath)
        check_config(config)
    except ModelConfigFileErrorInvalidSection as err:
        print(err)
    except ModelConfigFileErrorInvalidFilePath as err:
        print(err)
    except ModelConfigFileErrorInvalidOption as err:
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
        raise ModelConfigFileErrorInvalidSection(sections, valid_sections)


def check_config_filepaths(config):
    """Check that all the filepaths are valid."""
    for section in config.sections():
        for key in config[section]:
            value = config[section][key]
            if value and (key.endswith("dir") or key.endswith("file")):
                filepath = Path(value)
                if not filepath.exists() and not filepath.is_file():
                    raise ModelConfigFileErrorInvalidFilePath(value)


def check_config_options(config):
    """Check that all the options are valid."""
    valid_options = {
        "pet": ["hamon"],
        "snowmelt": ["yes", "no"],
    }

    options = {
        "pet": config["Options"]["option_pet"].lower().strip(),
        "snowmelt": (
            config["Options"]["option_snowmelt"].lower().strip()
        ),
    }

    for key in valid_options.keys() and options.keys():
        if options[key] not in valid_options[key]:
            raise ModelConfigFileErrorInvalidOption(options, valid_options)
