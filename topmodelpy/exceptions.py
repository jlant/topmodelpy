"""Exceptions for topmodel.py
"""


class TopmodelpyException(Exception):
    """
    Base exception class.  All custom exceptions subclass this class.
    """
    def __str__(self):
        return self.message


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


class TimeseriesFileErrorInvalidHeader(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """
    def __init__(self, invalid_header, valid_header):
        self.message = (
            "Error with timeseries file.\n"
            "Invalid header:\n"
            "  {}\n"
            "Valid header:\n"
            "  {}\n"
            "".format(invalid_header, valid_header)
        )


class TimeseriesFileErrorMissingValues(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """
    def __init__(self, missing_values):
        self.message = (
            "Error with timeseries file.\n"
            "Missing values:\n"
            "  {}\n"
            "".format(missing_values)
        )


class TimeseriesFileErrorMissingDates(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """
    def __init__(self, timestamps_near_missing):
        self.message = (
            "Error with timeseries file.\n"
            "Missing dates near:\n"
            "  {}\n"
            "".format(timestamps_near_missing)
        )


class TimeseriesFileErrorInvalidTimestep(TopmodelpyException):
    """
    Raised when a file is not a properly formatted timeseries csv file.
    """
    def __init__(self, invalid_timestep):
        self.message = (
            "Error with timeseries file.\n"
            "Invalid timestep:\n"
            "  {}\n"
            "Valid timestep:\n"
            "  timestep <= 1 (sub-daily or daily)\n"
            "".format(invalid_timestep)
        )


class TwiFileErrorInvalidHeader(TopmodelpyException):
    """
    Raised when a file is not a properly formatted twi csv file.
    """
    def __init__(self, invalid_header, valid_header):
        self.message = (
            "Error with twi file.\n"
            "Invalid header:\n"
            "  {}\n"
            "Valid header:\n"
            "  {}\n"
            "".format(invalid_header, valid_header)
        )


class TwiFileErrorMissingValues(TopmodelpyException):
    """
    Raised when a file is not a properly formatted twi csv file.
    """
    def __init__(self, missing_values):
        self.message = (
            "Error with twi file.\n"
            "Missing values:\n"
            "  {}\n"
            "".format(missing_values)
        )


class TwiFileErrorInvalidProportion(TopmodelpyException):
    """
    Raised when a file is not a properly formatted twi csv file.
    """
    def __init__(self, invalid_proportion):
        self.message = (
            "Error with twi file.\n"
            "Invalid sum of proportion column:\n"
            "  {}\n"
            "Valid sum of proportion column:\n"
            "  1.0\n"
            "".format(invalid_proportion)
        )
