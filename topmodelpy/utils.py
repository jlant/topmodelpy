"""Utility functions

"""

import numpy as np


def nans(shape, dtype=float):
    """Return an array filled with nan values.

    :param shape: A tuple for the shape of the array
    :type shape: tuple
    :returns: numpy.ndarray
    """
    array = np.empty(shape, dtype)
    array[:] = np.nan

    return array
