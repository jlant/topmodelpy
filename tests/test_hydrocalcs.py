"""Tests for hydrocals module."""

from datetime import datetime
import numpy as np

from waterpy import hydrocalcs


def test_pet(parameters_wolock,
             timeseries_wolock):

    dates = np.array(timeseries_wolock["date"].values,
                     dtype=np.datetime64).astype(datetime)
    actual = hydrocalcs.pet(
        dates=dates,
        temperatures=timeseries_wolock["temperature"].values,
        latitude=parameters_wolock["latitude"],
        method="hamon"
    )

    # The absolute tolerance is set because the calculation done in waterpy
    # is a little different than the calculation done in Wolock's version.
    np.testing.assert_allclose(actual,
                               timeseries_wolock["pet"].values,
                               atol=1.5)


def test_absolute_error(observed_data, modeled_data):

    expected = np.array([0.2, -0.1, 0.2, 0.3, -0.1])
    actual = hydrocalcs.absolute_error(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected)


def test_mean_squared_error(observed_data, modeled_data):

    expected = 0.038
    actual = hydrocalcs.mean_squared_error(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected)


def test_relative_error(observed_data, modeled_data):

    expected = np.array([0.00359066, -0.0016129, 0.00305344, 0.00463679, -0.00163666])
    actual = hydrocalcs.relative_error(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected, atol=1e-8)


def test_percent_error(observed_data, modeled_data):

    expected = np.array([0.359066, -0.16129, 0.305344, 0.463679, -0.163666])
    actual = hydrocalcs.percent_error(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected, atol=1e-6)


def test_percent_difference(observed_data, modeled_data):

    expected = np.array([0.35971223, -0.16116035, 0.3058104, 0.464756, -0.1635323])
    actual = hydrocalcs.percent_difference(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected, atol=1e-6)


def test_r_squared(observed_data, modeled_data):

    expected = 0.99768587638100936
    actual = hydrocalcs.r_squared(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected)


def test_nash_sutcliffe(observed_data, modeled_data):

    expected = 0.99682486631016043
    actual = hydrocalcs.nash_sutcliffe(observed_data, modeled_data)

    np.testing.assert_allclose(actual, expected)
