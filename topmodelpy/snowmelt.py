"""Snowmelt calculations


References:

Engineering and Design - Runoff from Snowmelt
U.S. Army Corps of Engineers
Engineering Manual 1110-2-1406
https://www.wcc.nrcs.usda.gov/ftpref/wntsc/H&H/snow/COEemSnowmeltRunoff.pdf
"""

import numpy as np


def calc_snowmelt(precipitation,
                  temperatures,
                  temperature_cutoff,
                  rain_melt_coeff,
                  melt_rate_coeff,
                  timestep_daily_fraction):
    """Snow melt routine.

    :param precipitation: Precipitation rates, in millimeters per day
    :type precipitation: numpy.ndarray
    :param temperatures: Temperatures, in degrees Fahrenheit
    :type temperatures: numpy.ndarray
    :param temperature_cutoff: Temperature when melt begins,
                               in degrees Fahrenheit
    :type temperature_cutoff: float
    :param rain_melt_coeff: Snowmelt coefficient when raining,
                             1/degrees Fahrenheit
    :type rain_melt_coeff: float
    :param melt_rate_coeff: Snowmelt rate coefficient (often variable),
                            in inches per degree Fahrenheit
    :type melt_rate_coeff: float
    :param timestep_daily_fraction: Model timestep as a fraction of a day
    :type timestep_daily_fraction: float
    :return: Tuple of arrays of updated precipitation, snowmelt,
             and snowpack values, each array is in millimeters per day
    :rtype: Tuple

    """
    precip_inches = precipitation / 25.4  # mm to inches

    snowprecip = []
    snowmelts = []
    snowpacks = []

    snowmelt = 0
    snowpack = 0
    for temp, precip_inch in zip(temperatures, precip_inches):

        # If temp is high enough then there is snowmelt,
        # calculate amount of snowmelt, else no snowmelt,
        # snowpack accumulates by full precip amount
        if temp >= temperature_cutoff:
            # If it is raining, calculate snowmelt with rain,
            # else calculate snowmelt without rain
            if precip_inch > 0:
                snowmelt = calc_snowmelt_rain_on_snow_heavily_forested(
                    precip_inch,
                    temp,
                    temperature_cutoff,
                    rain_melt_coeff
                )

                # adjust daily snowmelt to same timestep as precip and temp
                snowmelt = snowmelt * timestep_daily_fraction

            else:
                snowmelt = calc_snowmelt_temperature_index(
                    temp,
                    temperature_cutoff,
                    rain_melt_coeff
                )

                # adjust daily snowmelt to same timestep as precip and temp
                snowmelt = snowmelt * timestep_daily_fraction

            # If there is more snowmelt than snowpack available to melt, then
            # add the amount of snowpack available to the snowmelt
            if snowmelt >= snowpack:
                snowmelt = snowpack

            # Remove the amount of snowmelt from the snowpack,
            # and add the amount of snowmelt to the current precip amount
            snowpack = snowpack - snowmelt
            precip_inch = precip_inch + snowmelt

        # If temp is too cold for melting, then add the precip (snow) amount
        # to the snow pack and assume no water infiltrates on cold days by
        # setting precip to zero
        else:
            snowpack = snowpack + precip_inch
            precip_inch = 0

        snowprecip.append(precip_inch)
        snowmelts.append(snowmelt)
        snowpacks.append(snowpack)

    snowprecip = np.array(snowprecip) * 25.4  # inches to mm
    snowmelts = np.array(snowmelts) * 25.4  # inches to mm
    snowpacks = np.array(snowpacks) * 25.4  # inches to mm

    return snowprecip, snowmelts, snowpacks


def calc_snowmelt_rain_on_snow_heavily_forested(precipitation,
                                                temperatures,
                                                temperature_cutoff=32.0,
                                                rain_melt_coeff=0.007):
    """Calculate the amount of snowmelt rain-on-snow situations in
    heavily forested areas using a generalized equation for rain-on-snow
    situations in heavily forested areas (the mean canopy cover is greater
    than 80%). This snowmelt calculation is from the family of energy budget
    solutions.

    :param precipitation: Precipitation rates, in inches/day
    :type precipitation: numpy.ndarray
    :param temperatures: Temperatures, in degrees Fahrenheit
    :type temperatures: numpy.ndarray
    :param temperature_cutoff: Temperature when melt begins,
                               in degrees Fahrenheit
    :type temperature_cutoff: float
    :param rain_melt_coeff: Snowmelt coefficient when raining,
                             1/degrees Fahrenheit
    :type rain_melt_coeff: float
    :return snowmelt: Snowmelt values, in inches per day
    :rtype snowmelt: numpy.ndarray

    .. note::

    Equation:

    M = (0.074 + 0.007 * P_r) * (T_a - 32) + 0.05

    where

    M           snowmelt, inches/day
    P_r         rate of precipitation, inches/day
    T_a         temperature of saturated air, at 3 meters (10 ft) level,
                degrees Fahrenheit

    Reference:

    Engineering and Design - Runoff from Snowmelt
    U.S. Army Corps of Engineers
    Engineering Manual 1110-2-1406
    Chapter 5-3. Generalized Equations, Rain-on-Snow Situations, Equation 5-20
    https://www.wcc.nrcs.usda.gov/ftpref/wntsc/H&H/snow/COEemSnowmeltRunoff.pdf
    """
    return (
        (0.074 + rain_melt_coeff * precipitation)
        * (temperatures - temperature_cutoff) + 0.05
    )


def calc_snowmelt_rain_on_snow_open_to_partly_forested(precipitation,
                                                       temperatures,
                                                       winds,
                                                       temperature_cutoff=32.0,
                                                       rain_melt_coeff=0.007,
                                                       basin_wind_coeff=0.5):
    """Calculate the amount of snowmelt rain-on-snow situations in
    partially forested areas using a generalized equation for
    rain-on-snow situations in partially forested areas (the mean canopy
    cover is greater than 10%-80%). Snowmelt calculation is from the family
    of energy budget solutions.

    :param precipitation: Precipitation rates, in inches/day
    :type precipitation: numpy.ndarray
    :param temperatures: Temperatures of saturated air,
                         in degrees Fahrenheit
    :type temperatures: numpy.ndarray
    :param winds: Winds, in miles per hour
    :type winds: numpy.ndarray
    :param temperature_cutoff: Temperature when melt begins,
                               in degrees Fahrenheit
    :type temperature_cutoff: float
    :param rain_melt_coeff: Snowmelt coefficient when raining,
                             1/degrees Fahrenheit
    :type rain_melt_coeff: float
    :param basin_wind_coeff: Basin wind exposure coefficient, fraction
    :type basin_wind_coeff: float
    :return snowmelt: Snowmelt values, in inches per day
    :rtype snowmelt: numpy.ndarray

    .. note::

    Equation:

    M = (0.029 + 0.0084 * k * v + 0.007 * P_r) * (T_a - 32) + 0.09

    where

    M           snowmelt, inches/day
    k           basin wind exposure coefficient, unitless
    v           wind velocity, miles/hour
    P_r         rate of precipitation, inches/day
    T_a         temperature of saturated air, at 3 meters (10 ft) level,
                degrees Fahrenheit

    Reference:

    Engineering and Design - Runoff from Snowmelt
    U.S. Army Corps of Engineers
    Engineering Manual 1110-2-1406
    Chapter 5-3. Generalized Equations, Rain-on-Snow Situations, Equation 5-19
    https://www.wcc.nrcs.usda.gov/ftpref/wntsc/H&H/snow/COEemSnowmeltRunoff.pdf
    """
    return (
        (0.029
         + (0.0084 * basin_wind_coeff * winds)
         + (rain_melt_coeff * precipitation))
        * (temperatures - temperature_cutoff) + 0.09
    )


def calc_snowmelt_temperature_index(temperatures,
                                    temperature_cutoff=32.0,
                                    melt_rate_coeff=0.06):
    """Calculate the amount of snowmelt using a temperature index method,
    also called degree-day method. This method has its limitations as noted
    in the reference.

    :param temperatures: Temperatures, in degrees Fahrenheit
    :type temperatures: numpy.ndarray
    :param temperature_cutoff: Temperature when melt begins,
                               in degrees Fahrenheit
    :type temperature_cutoff: float
    :param melt_rate_coeff: Snowmelt rate coefficient (often variable),
                            in inches per degree Fahrenheit
    :type melt_rate_coeff: float
    :return snowmelt: Snowmelt values, in inches per day
    :rtype snowmelt: numpy.ndarray

    .. note::

    Equation:

    M = C_m * (T_a - T_b)

    where

    M           snowmelt, inches per period
    C_m         melt-rate coefficient, inches/(degree Fahrenheit/period)
    T_a         air temperature, degrees Fahrenheit
    T_b         base temperature, degrees Fahrenheit

    Reference:

    Engineering and Design - Runoff from Snowmelt
    U.S. Army Corps of Engineers
    Engineering Manual 1110-2-1406
    Chapter 6-1. Generalized Equations, Rain-on-Snow Situations, Equation 6-1
    https://www.wcc.nrcs.usda.gov/ftpref/wntsc/H&H/snow/COEemSnowmeltRunoff.pdf
    """
    return melt_rate_coeff * (temperatures - temperature_cutoff)


