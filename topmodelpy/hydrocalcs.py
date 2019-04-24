"""
Module of hydrologic calculations.

References:

Engineering and Design - Runoff from Snowmelt
U.S. Army Corps of Engineers
Engineering Manual 1110-2-1406
https://www.wcc.nrcs.usda.gov/ftpref/wntsc/H&H/snow/COEemSnowmeltRunoff.pdf
"""

import numpy as np


def pet(dates, temperatures, latitude, method="hamon"):
    """Calculate potential evapotranspiration for various methods.

    :param dates: An array of python datetimes
    :type dates: numpy.ndarray
    :param temperatures: An array of temperatures , in degrees Celsius
    :type temperatures: numpy.ndarray
    :param latitude: A latitude, in decimal degrees
    :type latitude: float
    :return pet: array of pet values, in millimeters per day
    :rtype pet: numpy.ndarray
    """
    if method.lower() == "hamon":
        return pet_hamon(dates, temperatures, latitude)


def pet_hamon(dates, temperatures, latitude):
    """Calculate the amount of potential evapotranspiration in millimeters
    per day using the Hamon equation.

    :param dates: An array of python datetimes
    :type dates: numpy.ndarray
    :param temps: An array of temps, in degrees Celsius
    :type temps: numpy.ndarray
    :param latitude: A latitude, in decimal degrees
    :type latitude: float
    :return pet: array of pet values, in millimeters per day
    :rtype pet: numpy.ndarray

    .. notes::
       Equation:

       (1) PET = 0.1651 * Ld * RHOSAT * KPEC

       where

           PET          daily potential evapotranspiration (mm/day)
           Ld           daytime length (daylight hours), time from sunrise
                        to sunset in multiples of 12 hours (hours)
           RHOSAT       saturated vapor density at the daily mean air
                        temperature (T), g/m**3
           KPEC         calibration coefficient, dimensionless
                        set to 1.2 for southeastern United States

       Sub-equations:

       (2) RHOSAT = 216.7 * ESAT / (T + 273.3)

       (3) ESAT = 6.108 * EXP(17.26939 * T / (T + 237.3))

       where

           T       daily mean air temperature, (celsius)
           ESAT    saturated vapor pressure at the given T, (mb)

       (4) Ld = (w / 15) * 2

       where

           w       the sunset hour angle (degrees); Earth moves 15° per hour

       (5) w = arccos(-1 * tan(declination) * tan(latitude))

       where

           latitude           angle distance of a place north  or south of the
                              earth's equator (radians)

           declination        angle between the Sun's rays and the equatorial
                              plane (radians); the declination of the Earth is
                              the angular distance at solar noon between the
                              Sun and the Equator, north-positive

       (6) declination = 23.45° * sin((360 * (284 + N) / 365))

       where

           N                  number of days after January 1 (the Julian Day)

       References:
           - Lu et al. (2005). A comparison of six potential evapotranspiration
             methods for reginal use in the southeastern United States.

           - Brock, Thomas. (1981). Calculating solar radiation for ecological
             studies. Ecological Modeling.

           - https://en.wikipedia.org/wiki/Position_of_the_Sun
    """
    if len(dates) != len(temperatures):
        raise IndexError(
            "Length of dates: {}\n",
            "Length of temperatures: {}\n",
            "Lengths of dates and temperatures must be equal"
            "".format(len(dates), len(temperatures))
        )

    DEG2RAD = np.pi/180
    RAD2DEG = 180/np.pi
    CALIBCOEFF = 1.2

    pet = []
    for date, temperature in zip(dates, temperatures):

        # Declination
        # Note: using python datetimes whih have .timetuple() method
        day_num = date.timetuple().tm_yday
        angle = 360 * ((284 + day_num) / 365) * DEG2RAD
        declination = (23.45 * DEG2RAD) * np.sin(angle)

        # calculate sunset hour angle in degrees (w)
        sunset_hour_angle = (
            np.arccos(-1 * np.tan(declination) * np.tan(latitude * DEG2RAD))
            * RAD2DEG
        )

        # calculate daytime length in 12 hour unit (Ld)
        daytime_length = abs((sunset_hour_angle / 15) * 2) / 12

        # calculate saturated vapor pressure (ESAT)
        saturated_vapor_pressure = (
            6.108 * np.exp((17.26939 * temperature) / (temperature + 237.3))
        )

        # calculate saturated vapor density (RHOSAT)
        saturated_vapor_density = (
            (216.7 * saturated_vapor_pressure) / (temperature + 273.3)
        )

        # calculate potential evapotranspiration
        potential_evapotranspiration = (
            0.1651 * daytime_length * saturated_vapor_density * CALIBCOEFF
        )

        # add to list
        pet.append(potential_evapotranspiration)

    # convert list to numpy array
    pet = np.array(pet)

    return pet


def snowmelt(precipitation,
             temperatures,
             temperature_cutoff,
             snowmelt_rate_coeff_with_rain,
             snowmelt_rate_coeff,
             timestep_daily_fraction):
    """Snow melt routine.

    :param precipitation: Precipitation rates, in millimeters per day
    :type precipitation: numpy.ndarray
    :param temperatures: Temperatures, in degrees Fahrenheit
    :type temperatures: numpy.ndarray
    :param temperature_cutoff: Temperature when melt begins,
                               in degrees Fahrenheit
    :type temperature_cutoff: float
    :param snowmelt_rate_coeff_with_rain: Snowmelt coefficient when raining,
                                          1/degrees Fahrenheit
    :type snowmelt_rate_coeff_with_rain: float
    :param snowmelt_rate_coeff: Snowmelt rate coefficient (often variable),
                                in inches per degree Fahrenheit
    :type snowmelt_rate_coeff: float
    :param timestep_daily_fraction: Model timestep as a fraction of a day
    :type timestep_daily_fraction: float
    :return: Tuple of arrays of adjusted precipitation, snowmelt,
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
                snowmelt = snowmelt_rain_on_snow_heavily_forested(
                    precip_inch,
                    temp,
                    temperature_cutoff,
                    snowmelt_rate_coeff_with_rain
                )

                # adjust daily snowmelt to same timestep as precip and temp
                snowmelt = snowmelt * timestep_daily_fraction

            else:
                snowmelt = snowmelt_temperature_index(
                    temp,
                    temperature_cutoff,
                    snowmelt_rate_coeff
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


def snowmelt_rain_on_snow_heavily_forested(precipitation,
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


def snowmelt_rain_on_snow_open_to_partly_forested(precipitation,
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


def snowmelt_temperature_index(temperatures,
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


def weighted_mean(values, weights):
    """Calculate the weighted mean.

    :param values: Array of values
    :type values: numpy.ndarray
    :param weights: Array of weights
    :type weights: numpy.ndarray
    :rtype: float
    """
    weighted_mean = (values * weights).sum() / weights.sum()

    return weighted_mean


def absolute_error(observed, modeled):
    """Calculate the absolute error between two arrays.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: numpy.ndarray
    """
    error = observed - modeled

    return error


def mean_squared_error(observed, modeled):
    """Calculate the mean square error between two arrays.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: float
    """
    error = absolute_error(observed, modeled)
    mse = np.mean(error**2)

    return mse


def relative_error(observed, modeled):
    """Calculate the relative change between two arrays.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: numpy.ndarray
    """
    error = absolute_error(observed, modeled) / observed

    return error


def percent_error(observed, modeled):
    """Calculate the percent error between two arrays.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: numpy.ndarray
    """
    error = relative_error(observed, modeled) * 100

    return error


def percent_difference(observed, modeled):
    """Calculate the percent difference between two arrays.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: numpy.ndarray
    """
    mean = np.mean((observed, modeled), axis=0)
    percent_diff = ((modeled - observed) / mean) * 100

    return percent_diff


def r_squared(observed, modeled):
    """Calculate the Coefficient of Determination. Used to indicate how well
    data points fit a line or curve. Use numpy.coeff for computation.

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: float
    """
    r = np.corrcoef(observed, modeled)[0, 1]
    coefficient = r**2

    return coefficient


def nash_sutcliffe(observed, modeled):
    """Calculate the Nash-Sutcliffe (model efficiency coefficient).
    Used to assess the predictive power of hydrological models.

    E = 1 - sum((observed - modeled) ** 2)) / (sum((observed - mean_observed)**2 )))

    :param observed: Array of observed data
    :type observed: numpy.ndarray
    :param modeled: Array of modeled data
    :type modeled: numpy.ndarray
    :rtype: float
    """
    mean_observed = np.mean(observed)
    numerator = np.sum((observed - modeled) ** 2)
    denominator = np.sum((observed - mean_observed)**2)
    coefficient = 1 - (numerator/denominator)

    return coefficient

