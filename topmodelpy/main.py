"""Main module that runs topmodelpy.

This module contains functionality that:
    - Read model configurationo file
    - Read all input files
    - Preprocess input data
        - Calculate the timestep daily fraction
        - Calculate pet if not in timeseries
        - Calculates adjusted precipitation from snowmelt
        - Calculate the twi weighted mean
    - Run Topmodel
    - Post process results
        - Write output *.csv file of results
        - Plot output
"""
from topmodelpy import (hydrocalcs,
                        modelconfigfile,
                        parametersfile,
                        timeseriesfile,
                        twifile)
from topmodelpy.topmodel import Topmodel


def topmodelpy(configfile, options):
    """Reads inputs, preprocesses data, runs Topmodel, and postprocesses
    results.

    :param configfile: The file path to the model config file that
    contains model specifications
    :type param: string
    :param options: The options sent from the cli
    :type options: Click.obj
    """

    configdata = modelconfigfile.read(configfile)
    parameters, timeseries, twi = read_input_files(configdata)

    preprocessed_data = preprocess(parameters, timeseries, twi)
    topmodel_data = run_topmodel(parameters, twi, preprocessed_data)
    postprocess()


def read_input_files(configdata):
    """Read input files from model configuration file.

    Returns a tuple of:
        dictionary from parameters file
        pandas.DataFrame from timeseries file
        pandas.DataFrame from twi file

    :param config: A ConfigParser object that behaves much like a dictionary.
    :type config: ConfigParser
    :return: Tuple of parameters dict, timeseries dataframe, twi dataframe
    :rtype: tuple
    """
    parameters = parametersfile.read(configdata["Inputs"]["parameters_file"])
    timeseries = timeseriesfile.read(configdata["Inputs"]["timeseries_file"])
    twi = twifile.read(configdata["Inputs"]["twi_file"])

    return parameters, timeseries, twi


def preprocess(parameters, timeseries, twi):
    """Preprocess data for topmodel run.

    Calculate timestep daily fraction, usually 1 for daily timesteps
        - 1 day = 86400 seconds
    Calculate pet if pet is not in timeseries dataframe
    Calculate snowmelt and adjusted precipitation from snowmelt routine
        - Snowmelt routine requires temperatures in Fahrenheit.
        - The temperature cutoff from the parameters dict is in Fahrenheit.
        - snowprecip is the adjusted precipitation from snowmelt.
        - The snowmelt and snowpack variables are not used at this time.
    Calculate the difference between the adjusted precip and pet for Topmodel.
    Calculate the weighted twi mean for Topmodel.

    :param parameters: The parameters for the model.
    :type parameters: Dict
    :param timeseries: A dataframe of all the timeseries data.
    :type timeseries: Pandas.DataFrame
    :param twi: A dataframe of all the twi data.
    :type twi: Pandas.DataFrame
    :return preprocessed_data: A dict of the calculated variables from
                               preprocessing.
    :rtype: dict
    """
    # Calculate the daily timestep as a fraction
    timestep_daily_fraction = (
        (timeseries.index[1] - timeseries.index[0]).total_seconds() / 86400.0
    )

    # Get pet as a numpy array from the input timeseries if it exists,
    # otherwise calculate it.
    if "pet" in timeseries.columns:
        pet = timeseries["pet"].to_numpy() * timestep_daily_fraction
    else:
        pet = hydrocalcs.pet(
            dates=timeseries.index.to_pydatetime(),
            temperature=timeseries["temperature"].to_numpy(),
            latitude=parameters["latitude"]["value"],
            method="hamon"
        )
        pet = pet * timestep_daily_fraction

    # Calculate the adjusted precipitation based on snowmelt
    # Note: snowmelt function needs temperatures in Fahrenheit
    snowprecip, snowmelt, snowpack = hydrocalcs.snowmelt(
        timeseries["precipitation"].to_numpy(),
        timeseries["temperature"].to_numpy() * (9/5) + 32,
        parameters["snowmelt_temperature_cutoff"]["value"],
        parameters["snowmelt_rate_coeff_with_rain"]["value"],
        parameters["snowmelt_rate_coeff"]["value"],
        timestep_daily_fraction
    )

    # Calculate the difference between the adjusted precip (snowprecip)
    # and pet.
    precip_minus_pet = snowprecip - pet

    # Calculate the twi weighted mean
    twi_weighted_mean = (
        (twi["twi"] * twi["proportion"]).sum()
        / twi["proportion"].sum()
    )

    # Return a dict of calculated data
    preprocessed_data = {
        "timestep_daily_fraction": timestep_daily_fraction,
        "pet": pet,
        "precip_minus_pet": precip_minus_pet,
        "snowprecip": snowprecip,
        "snowmelt": snowmelt,
        "snowpack": snowpack,
        "twi_weighted_mean": twi_weighted_mean,
    }

    return preprocessed_data


def run_topmodel(parameters, twi, preprocessed_data):
    """Run Topmodel.

    :param parameters: The parameters for the model.
    :type parameters: Dict
    :param twi: A dataframe of all the twi data.
    :type twi: Pandas.DataFrame
    :param preprocessed_data: A dict of the calculated variables from
                              preprocessing.
    :type: dict
    :return topmodel_data: A dict of relevant data results from Topmodel
    :rtype: dict
    """
    # Initialize Topmodel
    topmodel = Topmodel(
        scaling_parameter=parameters["scaling_parameter"],
        saturated_hydraulic_conductivity=(
            parameters["saturated_hydraulic_conductivity"]
        ),
        macropore_fraction=parameters["macropore_fraction"],
        soil_depth_total=parameters["soil_depth_total"],
        soil_depth_ab_horizon=parameters["soil_depth_ab_horizon"],
        field_capacity_fraction=parameters["field_capacity_fraction"],
        latitude=parameters["latitude"],
        basin_area_total=parameters["basin_area_total"],
        impervious_area_fraction=parameters["impervious_area_fraction"],
        twi_values=twi["twi"].to_numpy(),
        twi_saturated_areas=twi["proportion"].to_numpy(),
        twi_mean=preprocessed_data["twi_weighted_mean"],
        precip_available=preprocessed_data["precip_minus_pet"],
        flow_initial=parameters["flow_initial"],
        timestep_daily_fraction=preprocessed_data["timestep_daily_fraction"]
    )

    import pdb
    pdb.set_trace()
    # Run Topmodel
    topmodel.run()
