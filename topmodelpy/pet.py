"""
Module of potental evapotranspiration calculations.
"""

import numpy as np


def calc_pet(dates, temperatures, latitude, method="hamon"):
    """Calculate potential evapotranspiration for various methods.

    :param dates: An array of dates
    :type dates: numpy.ndarray
    :param temperatures: An array of temperatures , in degrees Celsius
    :type temperatures: numpy.ndarray
    :param latitude: A latitude, in decimal degrees
    :type latitude: float
    :return pet: array of pet values, in millimeters per day
    :rtype pet: numpy.ndarray
    """
    if method.lower() == "hamon":
        return calc_pet_hamon(dates, temperatures, latitude)


def calc_pet_hamon(dates, temperatures, latitude):
    """Calculate the amount of potential evapotranspiration in millimeters
    per day using the Hamon equation.

    :param dates: An array of dates
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

        # calculate declination
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
