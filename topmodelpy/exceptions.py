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
    def __init__(self, invalid_sections, valid_sections):
        self.message = (
            "Error with model config file.\n"
            "Invalid section(s):\n"
            "  {}\n"
            "Valid sections are:\n"
            "  {}\n".format(invalid_sections, valid_sections)
        )

    def __str__(self):
        return self.message


class ModelConfigFileErrorInvalidFilePath(TopmodelpyException):
    """
    Raised when a model config file does not contain vaild file paths.
    """
    def __init__(self, filepath):
        self.message = (
            "Error with model config file.\n"
            "Invalid file path:\n"
            "  {}".format(filepath)
        )

    def __str__(self):
        return self.message


class ModelConfigFileErrorInvalidOption(TopmodelpyException):
    """
    Raised when a model config file does not contain valid options.
    """
    def __init__(self, invalid_options, valid_options):
        self.message = (
            "Error with model config file.\n"
            "Invalid option(s):\n"
            "  option_pet = {pet}\n"
            "  option_snowmelt_with_precip = {snowmelt_with_precip}\n"
            "  option_snowmelt_with_no_precip = {snowmelt_with_no_precip}\n"
            "".format(**invalid_options)
        )
        self.message = self.message + (
            "Valid options (contained in each respective list):\n"
            "  option_pet = {pet}\n"
            "  option_snowmelt_with_precip = {snowmelt_with_precip}\n"
            "  option_snowmelt_with_no_precip = {snowmelt_with_no_precip}\n"
            "".format(**valid_options)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidHeader(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_header, valid_header):
        self.message = (
            "Error with parameters file.\n"
            "Invalid header:\n"
            "  {}\n"
            "Valid header:\n"
            "  {}\n"
            "".format(invalid_header, valid_header)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidScalingParameter(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid scaling parameter:\n"
            "  {}\n"
            "Valid scaling parameter:\n"
            "  scaling_parameter > 0\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidLatitude(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid latitude:\n"
            "  {}\n"
            "Valid latitude:\n"
            "  0 <= latitude <= 90\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidSoilDepthTotal(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid soil depth total:\n"
            "  {}\n"
            "Valid soil depth total:\n"
            "  soil_depth_total > 0\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidSoilDepthAB(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value, soil_depth_total):
        self.message = (
            "Error with parameters file.\n"
            "Invalid soil depth ab horizon:\n"
            "  {}\n"
            "Valid soil depth ab horizon:\n"
            "  soil_depth_ab_horizon > 0\n"
            "  soil_depth_ab_horizon < {} (soil_depth_total)\n"
            "".format(invalid_value, soil_depth_total)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidFieldCapacity(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid field capacity:\n"
            "  {}\n"
            "Valid field capacity:\n"
            "  0 <= field_capacity_fraction <=1\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidMacropore(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid macropore:\n"
            "  {}\n"
            "Valid macropore:\n"
            "  0 <= macropore_fraction <=1\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class ParametersFileErrorInvalidImperviousArea(TopmodelpyException):
    """
    Raised when a file is not a properly formatted parameters csv file.
    """
    def __init__(self, invalid_value):
        self.message = (
            "Error with parameters file.\n"
            "Invalid impervious area:\n"
            "  {}\n"
            "Valid impervious area:\n"
            "  0 <= imprevious_area_fraction <=1\n"
            "".format(invalid_value)
        )

    def __str__(self):
        return self.message


class InvalidUsgsNwisTsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted USGS NWIS tsv file.
    """


class InvalidTimeseriesCsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """


class InvalidTwiCsvFile(TopmodelpyException):
    """
    Raised when a file is not a properly formatted twi disribution csv file.
    """

