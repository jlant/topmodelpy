"""Tests for timeseriesfile module."""

from datetime import datetime
from io import StringIO
import numpy as np
import pandas as pd
import pytest

from topmodelpy.exceptions import (TimeseriesFileErrorInvalidHeader,
                                   TimeseriesFileErrorMissingValues,
                                   TimeseriesFileErrorMissingDates,
                                   TimeseriesFileErrorInvalidTimestep)
from topmodelpy import timeseriesfile


def test_timeseries_file_read_in(timeseries_file):
    expected = pd.DataFrame({
        "date": np.array([
                    datetime(2017, 1, 1, 0, 0),
                    datetime(2017, 1, 2, 0, 0),
                    datetime(2017, 1, 3, 0, 0),
                    datetime(2017, 1, 4, 0, 0),
                    datetime(2017, 1, 5, 0, 0)]),
        "temperature": np.array([1.0, 1.1, 1.2, 1.3, 1.4]),
        "precipitation": np.array([2.0, 2.1, 2.2, 2.3, 2.4]),
        "pet": np.array([3.0, 3.1, 3.2, 3.3, 3.4]),
        "flow_observed": np.array([4.0, 4.1, 4.2, 4.3, 4.4]),
    })
    filestream = StringIO(timeseries_file)
    actual = timeseriesfile.read_in(filestream)

    np.testing.assert_allclose(actual["precipitation"],
                               expected["precipitation"])
    np.testing.assert_allclose(actual["temperature"],
                               expected["temperature"])
    np.testing.assert_allclose(actual["pet"],
                               expected["pet"])
    np.testing.assert_allclose(actual["flow_observed"],
                               expected["flow_observed"])
    assert actual.dtypes.all() == "float64"
    assert isinstance(actual.index, pd.DatetimeIndex)
    assert (actual.index[1] - actual.index[0]).days == 1


def test_timeseries_file_invalid_header(timeseries_file_invalid_header):
    filestream = StringIO(timeseries_file_invalid_header)

    with pytest.raises(TimeseriesFileErrorInvalidHeader) as err:
        timeseriesfile.read_in(filestream)

    assert "Invalid header" in str(err.value)


def test_timeseries_file_missing_dates(timeseries_file_missing_dates):
    filestream = StringIO(timeseries_file_missing_dates)

    with pytest.raises(TimeseriesFileErrorMissingDates) as err:
        timeseriesfile.read_in(filestream)

    assert "Missing dates" in str(err.value)


def test_timeseries_file_missing_values(timeseries_file_missing_values):
    filestream = StringIO(timeseries_file_missing_values)

    with pytest.raises(TimeseriesFileErrorMissingValues) as err:
        timeseriesfile.read_in(filestream)

    assert "Missing values" in str(err.value)


def test_timeseries_file_invalid_timestep(timeseries_file_invalid_timestep):
    filestream = StringIO(timeseries_file_invalid_timestep)

    with pytest.raises(TimeseriesFileErrorInvalidTimestep) as err:
        timeseriesfile.read_in(filestream)

    print(err.value)
    assert "Invalid timestep" in str(err.value)
