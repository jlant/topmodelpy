"""Test potential evapotranspiration calculation."""

from datetime import datetime
import numpy as np

from topmodelpy.pet import calc_pet


def test_calc_pet(parameters_wolock,
                  timeseries_wolock):

    dates = np.array(timeseries_wolock["date"].values,
                     dtype=np.datetime64).astype(datetime)
    actual = calc_pet(dates=dates,
                      temperatures=timeseries_wolock["temperature"].values,
                      latitude=parameters_wolock["latitude"],
                      method="hamon")

    # The absolute tolerance is set because the calculation done in topmodelpy
    # is a little different than the calculation done in Wolock's version.
    np.testing.assert_allclose(actual,
                               timeseries_wolock["pet"].values,
                               atol=1.5)
