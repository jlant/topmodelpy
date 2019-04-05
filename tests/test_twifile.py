"""Tests for twi module."""

from datetime import datetime
from io import StringIO
import numpy as np
import pandas as pd
import pytest

from topmodelpy.exceptions import (TwiFileErrorInvalidHeader,
                                   TwiFileErrorMissingValues,
                                   TwiFileErrorInvalidProportion)
from topmodelpy import twifile


def test_twi_file_read_in(twi_file):
    expected = pd.DataFrame({
        "bin": np.array([1, 2, 3, 4, 5]),
        "twi": np.array([0.02, 0.03, 0.04, 0.05, 0.06]),
        "proportion": np.array([0.10, 0.15, 0.25, 0.30, 0.20]),
        "cells": np.array([10, 15, 25, 30, 20]),
    })
    filestream = StringIO(twi_file)
    actual = twifile.read_in(filestream)

    np.testing.assert_allclose(actual["bin"],
                               expected["bin"])
    np.testing.assert_allclose(actual["twi"],
                               expected["twi"])
    np.testing.assert_allclose(actual["proportion"],
                               expected["proportion"])
    np.testing.assert_allclose(actual["cells"],
                               expected["cells"])
    assert actual.dtypes.all() == "float64"


def test_twi_file_invalid_header(twi_file_invalid_header):
    filestream = StringIO(twi_file_invalid_header)

    with pytest.raises(TwiFileErrorInvalidHeader) as err:
        twifile.read_in(filestream)

    assert "Invalid header" in str(err.value)


def test_twi_file_missing_values(twi_file_missing_values):
    filestream = StringIO(twi_file_missing_values)

    with pytest.raises(TwiFileErrorMissingValues) as err:
        twifile.read_in(filestream)

    assert "Missing values" in str(err.value)


def test_twi_file_invalid_proportion(twi_file_invalid_proportion):
    filestream = StringIO(twi_file_invalid_proportion)

    with pytest.raises(TwiFileErrorInvalidProportion) as err:
        twifile.read_in(filestream)

    assert "Invalid sum of proportion" in str(err.value)
