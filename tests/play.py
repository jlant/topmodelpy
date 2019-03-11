import os
import pandas as pd


def wolock_twi_data():
    """Test timeseries data"""

    fname = os.path.join(os.path.dirname(__file__),
                         "testdata/wolock_twi.csv")
    data = pd.read_csv(fname,
                       names=["bin",
                              "twi",
                              "proportion",
                              "cells"],
                       )

    return data


data = wolock_twi_data()
twi = data["twi"].values
print(type(twi))
print(twi[0:2])
