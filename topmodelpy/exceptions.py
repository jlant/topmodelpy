"""Exceptions for topmodel.py
"""


class TopmodelpyException(Exception):
    """
    Base exception class.  All custom exceptions subclass this class.
    """


class InvalidModelConfigFileInvalidSections(TopmodelpyException):
    """
    Raised when a file is not a properly formatted configuration ini file.
    """
    def __init__(self, valid_sections, invalid_sections):
        self.message = (
            "Error with model config file.\n"
            "Invalid sections.\n"
            "Valid sections are:\n"
            "  {}\n"
            "Invalid sections specified are:\n"
            "  {}".format(valid_sections, invalid_sections)
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

