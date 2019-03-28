"""Exceptions for topmodel.py
"""


class TopmodelpyException(Exception):
    """
    Base exception class.  All custom exceptions subclass this class.
    """


class ModelConfigFileErrorInvalidSection(TopmodelpyException):
    """
    Raised when a model config file does not contain required sections.
    """
    def __init__(self, valid_sections, invalid_sections):
        self.message = (
            "Error with model config file.\n"
            "Invalid section.\n"
            "Valid sections are:\n"
            "  {}\n"
            "Invalid sections specified are:\n"
            "  {}".format(valid_sections, invalid_sections)
        )

    def __str__(self):
        return self.message


class ModelConfigFileErrorInvalidFilePath(TopmodelpyException):
    """
    Raised when a model config file does not contain required sections.
    """
    def __init__(self, filepath):
        self.message = (
            "Error with model config file.\n"
            "Invalid file path: {}".format(filepath)
        )

    def __str__(self):
        return self.message


class ModelConfigFileErrorInvalidOption(TopmodelpyException):
    """
    Raised when a model config file does not contain valid options.
    """
    def __init__(self, valid_options, options):
        self.message = (
            "Error with model config file.\n"
            "Invalid option.\n"
            "Valid options are contained in each respective list:\n"
            "  option_pet = {pet}\n"
            "  option_snowmelt_with_precip = {snowmelt_with_precip}\n"
            "  option_snowmelt_with_no_precip = {snowmelt_with_no_precip}\n"
            "".format(**valid_options)
        )
        self.message = self.message + (
            "Options specified are:\n"
            "  option_pet = {pet}\n"
            "  option_snowmelt_with_precip = {snowmelt_with_precip}\n"
            "  option_snowmelt_with_no_precip = {snowmelt_with_no_precip}\n"
            "".format(**options)
        )

    def __str__(self):
        return self.message


class InvalidUsgsNwisTsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted USGS NWIS tsv file.
    """


class InvalidModelParametersCsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted model parameters csv file.
    """


class InvalidTimeseriesCsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """


class InvalidTwiCsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted twi disribution csv file.
    """

