# -*- coding: utf-8 -*-
"""
topmodelpy.main
~~~~~~~~~~~~~~~

Module that contains functionality that:
    1. Reads model configuration file and input files
    3. Preprocesses data for a Topmodel model run
        a. Calculates pet
        b. Calculates snowmelt
    4. Runs Topmodel
    5. Post processes data
        a. Writes output results as a csv file
        b. Plots output results as png files
"""

from . import (modelconfigfile,
               parametersfile,
               timeseriesfile,
               twifile,
               hydrocalcs)


def topmodelpy(configfile):
    configdata = modelconfigfile.read(configfile)
    parameters, timeseries, twi = read_input_files(configdata)

    preprocess()
    run_topodel()
    postprocess()


def read_input_files(configdata):
    parameters = parametersfile.read(configdata["Inputs"]["parameters_file"])
    timeseries = timeseriesfile.read(configdata["Inputs"]["timeseries_file"])
    twi = twifile.read(configdata["Inputs"]["twi_file"])

    return parameters, timeseries, twi


def preprocess(timeseries):
    timstep_daily_fraction = (
        (timeseries.index[1] - timeseries.index[0]).total_seconds() / 86000.0
    )
