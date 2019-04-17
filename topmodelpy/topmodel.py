"""Topmodel class
Class that represents an implementation of a rainfall-runoff model,
called Topmodel, based on a `U.S. Geological Survey`_ version by
David Wolock (please see `[1]`_).

Please see table in docs directory called "lant-to-wolock-conversion-table.rst"
which contains variable descriptions and units

.. [1] Wolock, D.M., "Simulating the variable-source-area concept of
streamflow generation with the watershed model Topmodel", U.S. Geological
Survey, Water-Resources Investigations Report 93-4124, 1993.

.. _U.S. Geological Survey: https://www.usgs.gov

:authors: 2019 by Jeremiah Lant, see AUTHORS
:license: CC0 1.0, see LICENSE file for details
"""

import math
import numpy as np

from . import utils


class Topmodel:
    """Class that represents a Topmodel based rainfall-runoff model
    implementation by David Wolock.
    """
    def __init__(self,
                 scaling_parameter,
                 saturated_hydraulic_conductivity,
                 macropore_fraction,
                 soil_depth_total,
                 soil_depth_ab_horizon,
                 field_capacity_fraction,
                 latitude,
                 basin_area_total,
                 impervious_area_fraction,
                 twi_values,
                 twi_saturated_areas,
                 twi_mean,
                 precip_available,
                 flow_initial=1,
                 timestep_daily_fraction=1,
                 soil_depth_roots=1):

        # Check and assign timestep daily fraction
        if timestep_daily_fraction > 1:
            raise ValueError(
                "Incorrect timestep: {} \n",
                "Timestep daily fraction must be less than or equal to 1.",
                "".format(timestep_daily_fraction)
            )
        self.timestep_daily_fraction = timestep_daily_fraction

        # Assign parameters
        self.scaling_parameter = scaling_parameter
        self.saturated_hydraulic_conductivity = saturated_hydraulic_conductivity
        self.macropore_fraction = macropore_fraction
        self.soil_depth_total = soil_depth_total
        self.soil_depth_ab_horizon = soil_depth_ab_horizon
        self.field_capacity_fraction = field_capacity_fraction
        self.latitude = latitude
        self.basin_area_total = basin_area_total
        self.impervious_area_fraction = impervious_area_fraction

        # Assign twi
        self.twi_values = twi_values
        self.twi_saturated_areas = twi_saturated_areas
        self.twi_mean = twi_mean
        self.num_twi_increments = len(self.twi_values)

        # Check and assign precip and potential evapotranspiration (pet)
        self.precip_available = precip_available
        self.num_timesteps = len(self.precip_available)

        # Initialize total predicted flow array with nan
        self.flow_predicted = utils.nans(self.num_timesteps)

        # Soil hydraulic variables
        # Note: soil depth of root zone has default value of 1 meter
        self.soil_depth_roots = soil_depth_roots
        self.soil_depth_c_horizon = None
        self.vertical_drainage_flux_initial = None
        self.vertical_drainage_flux = None
        self.transmissivity_saturated_max = None
        self.flow_subsurface_max = None
        self.root_zone_storage_max = None

        # Channel routing parameters
        self.channel_velocity_avg = None
        self.channel_length_max = None
        self.channel_travel_time = None

        # Initial flow
        # Note: initial flow has default value of 1 mm/day
        self.flow_initial = flow_initial * self.timestep_daily_fraction

        # Watershed average storage deficit
        self.saturation_deficit_avgs = utils.nans(self.num_timesteps)
        self.saturation_deficit_avg = None

        # Soil zone storages
        self.unsaturated_zone_storages = utils.nans((self.num_timesteps,
                                                     self.num_twi_increments))
        self.root_zone_storages = utils.nans((self.num_timesteps,
                                              self.num_twi_increments))
        self.unsaturated_zone_storage = None
        self.root_zone_storage = None

        # Variables used in self.run() method
        self.saturation_deficit_locals = utils.nans((self.num_timesteps,
                                                     self.num_twi_increments))

        self.saturation_deficit_local = None
        self.precip_for_evaporation = None
        self.precip_for_recharge = None
        self.precip_excesses = None
        self.precip_excess = None
        self.evaporation = None
        self.flow_predicted_overland = None
        self.flow_predicted_vertical_drainage_flux = None
        self.flow_predicted_subsurface = None
        self.flow_predicted_impervious_area = None
        self.flow_predicted_total = None
        self.flow_predicted_stream = None

        # Initialize model
        self._initialize()

    def _initialize(self):
        """Initialize model soil parameters, storage deficit, and
        unsaturated zone and root zone storages.
        """
        # Initialize soil parameters, channel routing parameters
        self._initialize_soil_hydraulic_parameters()
        self._initialize_channel_routing_parameters()

        # Initialize the watershed average storage deficit
        self._initialize_watershed_average_storage_deficit()

        # Initialize unsaturated zone storage and root zone storage
        self._initialize_soil_zone_storages()

    def _initialize_soil_hydraulic_parameters(self):
        """Initialize the soil hydraulic parameters."""

        if self.soil_depth_roots > self.soil_depth_total:
            self.soil_depth_roots = self.soil_depth_total

        self.soil_depth_c_horizon = (
            self.soil_depth_total - self.soil_depth_ab_horizon
        )

        # Initial vertical drainage flux as saturated hydraulic conductivity
        self.vertical_drainage_flux_initial = (
            self.saturated_hydraulic_conductivity
            * self.timestep_daily_fraction
        )

        # Maximum saturated hydraulic transmissivity
        # Equation 41 in Wolock, 1993
        # Note: it is assumed that the hydraulic conductivity of the AB
        # horizon is two orders of magnitude greater than the hydraulic
        # conductivity of the Z horizon
        self.transmissivity_saturated_max = (
            self.soil_depth_ab_horizon * 100
            * self.saturated_hydraulic_conductivity
            + self.soil_depth_c_horizon * self.saturated_hydraulic_conductivity
        )

        # Maximum subsurface flow rate - equation 32 in Wolock, 1993
        self.flow_subsurface_max = (
            self.transmissivity_saturated_max * math.exp(-1 * self.twi_mean)
            * self.timestep_daily_fraction
        )

        # Maximum root zone water storage - equation 36 in Wolock, 1993
        # Note: conversion from meters to millimeters,
        # root zone storage (millimeters)
        # soil depth (meters)
        self.root_zone_storage_max = (
            self.soil_depth_roots * 1000 * self.field_capacity_fraction
        )

    def _initialize_channel_routing_parameters(self):
        """Initialize the channel routing parameters."""

        # Channel velocity
        self.channel_velocity_avg = 10 * self.timestep_daily_fraction

        # Channel length maximum approximation as 2 * radius of circle
        self.channel_length_max = 2 * np.sqrt(self.basin_area_total / np.pi)

        # Equation 38 in Wolock, 1993
        self.channel_travel_time = (
            self.channel_length_max / self.channel_velocity_avg
        )

        # Wolock's topmodel code includes the following; is this to
        # prevent water from being routed before the end of the timestep?
        self.channel_travel_time = max(self.channel_travel_time, 1)

    def _initialize_watershed_average_storage_deficit(self):
        """Calculate the watershed average storage deficit."""

        # Watershed average storage deficit
        self.saturation_deficit_avg = (
            -1 * math.log(self.flow_initial / self.flow_subsurface_max)
            * self.scaling_parameter
        )

    def _initialize_soil_zone_storages(self):
        """Initialize the unsaturated zone and root zone storages."""

        # self.unsaturated_zone_storage: the amount of soil water available
        # for drainage
        # self.root_zone_storage: the amount of water stored in root zone
        self.unsaturated_zone_storage = np.zeros(self.num_twi_increments)
        self.root_zone_storage = (
            np.ones(self.num_twi_increments) * self.root_zone_storage_max
        )

    def run(self):
        """Calculate water fluxes and flow prediction."""

        # Start of timestep loop
        for i in range(self.num_timesteps):
            # Initialize predicted flows, precipitation in excess
            # of evapotranspiration and field-capacity storage, and
            # local saturation deficit
            self.flow_predicted_overland = 0
            self.flow_predicted_vertical_drainage_flux = 0
            self.precip_excesses = np.zeros(self.num_twi_increments)
            self.saturation_deficit_local = utils.nans(self.num_twi_increments)

            # Assign water available for evapotranspiration and
            # water available for recharge based on how precipitation
            # compares to potential evapotranspiration
            # If precip_available < 0 => moisture has to be taken out of soil
            # to meet the pet demand
            # If precip_available > 0 => then surplus precip soaks into the
            # ground to recharge soil moisture and any left over after that
            # runs off as streamflow
            # If precip_available = 0 => no surplus precip
            self.precip_for_evaporation = 0
            self.precip_for_recharge = 0
            if self.precip_available[i] < 0:
                self.precip_for_evaporation = (
                    -1 * self.precip_available[i]
                )
            elif self.precip_available[i] > 0:
                self.precip_for_recharge = self.precip_available[i]

            # Start of twi increments loop
            for j in range(self.num_twi_increments):

                # Local saturation/storage/drainage deficit
                # =========================================
                # Calculate the local saturation deficit
                self.saturation_deficit_local[j] = (
                    self.saturation_deficit_avg
                    + self.scaling_parameter * (self.twi_mean
                                                - self.twi_values[j])
                )

                # If local saturation deficit is less than zero, meaning soil
                # is overly saturated, then set the local saturation deficit
                # to zero meaning soil is saturated and water table is at the
                # land surface
                if self.saturation_deficit_local[j] < 0:
                    self.saturation_deficit_local[j] = 0

                # If the unsaturated zone storage is greater than the local
                # saturation deficit, update the root zone storage with the
                # difference and assign the local saturation deficit to the
                # unsaturated zone storage
                if self.unsaturated_zone_storage[j] > self.saturation_deficit_local[j]:
                    self.root_zone_storage[j] = (
                        self.root_zone_storage[j]
                        + (self.unsaturated_zone_storage[j]
                           - self.saturation_deficit_local[j])
                    )
                    self.unsaturated_zone_storage[j] = self.saturation_deficit_local[j]

                    # If root zone storage is greater than the maximum
                    # soil root zone storage, then assign the difference to
                    # excess precipitation and assign the root zone storage
                    # to the maximum root zone storage
                    if self.root_zone_storage[j] > self.root_zone_storage_max:
                        self.precip_excesses[j] = (
                            self.root_zone_storage[j] - self.root_zone_storage_max
                        )
                        self.root_zone_storage[j] = self.root_zone_storage_max

                # Precipitation
                # =============
                # If there is precipitation available, then process the
                # precipitation by calculating the excess precipitation and
                # adding it to an array of precipitation excesses over all twi
                # increments
                if self.precip_for_recharge > 0:
                    self.precip_excess = (
                        self.precip_for_recharge
                        - (self.saturation_deficit_local[j]
                           - self.unsaturated_zone_storage[j])
                        - (self.root_zone_storage_max
                           - self.root_zone_storage[j])
                    )
                    self.precip_excesses[j] = (
                        self.precip_excesses[j] + self.precip_excess
                    )

                    # If the excess precipitation calculated is less than 0.0,
                    # then reset the excess precipitation to 0.0
                    if self.precip_excess < 0:
                        self.precip_excess = 0

                    self.precip_excess_diff = (
                        abs(self.precip_excess
                            - self.precip_for_recharge)
                    )

                    if not self.precip_excess_diff <= 1E-20:
                        # Calculate the root zone storage amount from the
                        # differences between
                        # 1. (1 - self.macropore_fraction): the amount that is
                        # not bypassing the soil root zone
                        # 2. (self.precip_for_recharge
                        #     - self.precip_excess): the amount that is
                        # available without any excess
                        self.root_zone_storage[j] = (
                            self.root_zone_storage[j]
                            + (1.0 - self.macropore_fraction)
                            * (self.precip_for_recharge - self.precip_excess)
                        )

                        # Calculate the unsaturated zone storage amount from
                        # the amount bypassing the soil root zone and the
                        # amount that is available without any excess

                        self.unsaturated_zone_storage[j] = (
                            self.unsaturated_zone_storage[j]
                            + self.macropore_fraction
                            * (self.precip_for_recharge
                               - self.precip_excess)
                        )

                        # If the root zone storage is greater than the maximum
                        # soil root zone storage, then added the difference
                        # to the unsaturated zone storage and assign the root
                        # zone storage to the maximum root zone storage
                        if self.root_zone_storage[j] > self.root_zone_storage_max:
                            self.unsaturated_zone_storage[j] = (
                                self.unsaturated_zone_storage[j]
                                + (self.root_zone_storage[j]
                                   - self.root_zone_storage_max)
                            )
                            self.root_zone_storage[j] = self.root_zone_storage_max
                        else:
                            # If the unsaturated zone storage is greater than
                            # the local saturation deficit, update the root
                            # zone storage with the difference and assign the
                            # local saturation deficit to the unsaturated zone
                            # storage (same step preformed in calculation of
                            # the local saturation deficit above)
                            if self.unsaturated_zone_storage[j] > self.saturation_deficit_local[j]:
                                self.root_zone_storage[j] = (
                                    self.root_zone_storage[j]
                                    + (self.unsaturated_zone_storage[j]
                                       - self.saturation_deficit_local[j])
                                )
                                self.unsaturated_zone_storage[j] = self.saturation_deficit_local[j]

                # Drainage from unsaturated zone storage
                # ======================================
                # If there is water availble for vertical drainage, then
                # calculate the vertical drainage flux (millimeters/day)
                # equation 23 in Wolock, 1993
                # Note: self.vertical_drainage_flux_initial =
                # self.saturated_hydraulic_conductivity
                # * self.timestep_daily_fraction
                if self.saturation_deficit_local[j] > 0:
                    self.vertical_drainage_flux = (
                        self.vertical_drainage_flux_initial
                        * (self.unsaturated_zone_storage[j]
                           / self.saturation_deficit_local[j])
                    )

                    # If the vertical drainage flux is greater than the soil
                    # water available for drainage (unsaturated_zone_storage),
                    # then assign the vertical drainage flux to the
                    # unsaturated_zone_storage
                    if self.vertical_drainage_flux > self.unsaturated_zone_storage[j]:
                        self.vertical_drainage_flux = self.unsaturated_zone_storage[j]

                    # Update the unsaturated zone storage by removing the
                    # vertical drainage flux amount from the amount of soil
                    # water available to drain
                    self.unsaturated_zone_storage[j] = self.unsaturated_zone_storage[j] - self.vertical_drainage_flux

                    # Calculate the predicted vertical drainage flux from the
                    # vertical drainage amount and the current saturated
                    # land-surface area in the watershed
                    self.flow_predicted_vertical_drainage_flux = (
                        self.flow_predicted_vertical_drainage_flux
                        + (self.vertical_drainage_flux
                           * self.twi_saturated_areas[j])
                    )

                # Evaporation from soil root zone storage
                # =======================================
                # If there is precipitation available for evaporation,
                # then compute evaporation.
                if self.precip_for_evaporation > 0:
                    self.evaporation = self.precip_for_evaporation

                    # If the precipitation available for evapotranspiration is
                    # greater than the soil root zone storage amount, then
                    # assign all the water in the soil root zone storage to the
                    # precipitation available for evapotranspiration
                    if self.evaporation > self.root_zone_storage[j]:
                        self.evaporation = self.root_zone_storage[j]

                    # Calculate the amount of water in the soil root zone
                    # storage by removing the amount available for
                    # evapotranspiration
                    # note: soil root zone storage will be depleted (equal 0.0)
                    # if the condition above is true where the precipitation
                    # available for evapotranspiration is greater than the soil
                    # root zone storage amount
                    self.root_zone_storage[j] = (
                        self.root_zone_storage[j] - self.evaporation
                    )

                # Overland flow
                # =============
                # If the excess precipitation is greater than zero, then
                # calculate the predicted overland flow from the amount of
                # excess precipitation and the saturated area for the current
                # twi increment
                if self.precip_excesses[j] > 0:
                    self.flow_predicted_overland = (
                        self.flow_predicted_overland
                        + (self.precip_excesses[j]
                           * self.twi_saturated_areas[j])
                    )

                # Saving variables of interest
                # ============================
                self.unsaturated_zone_storages[i][j] = self.unsaturated_zone_storage[j]
                self.root_zone_storages[i][j] = self.root_zone_storage[j]
                self.saturation_deficit_locals[i][j] = self.saturation_deficit_local[j]

                # END OF TWI INCREMENTS LOOP

            # CONTINUE TIMESTEP LOOP

            # Subsurface flow (base flow)
            # ===========================

            # Calculate the subsurface flow rate - equation 30 in Wolock, 1993
            self.subsurface_flow_rate_ratio = (
                self.saturation_deficit_avg / self.scaling_parameter
            )

            if self.subsurface_flow_rate_ratio > 100:
                self.flow_predicted_subsurface = 0
            else:
                self.flow_predicted_subsurface = (
                    self.flow_subsurface_max
                    * math.exp(-1 * self.subsurface_flow_rate_ratio)
                )

            # Update the average watershed saturation deficit with the
            # subsurface flow and the vertical drainage flux
            self.saturation_deficit_avg = (
                self.saturation_deficit_avg
                - self.flow_predicted_vertical_drainage_flux
                + self.flow_predicted_subsurface
            )

            if self.saturation_deficit_avg < 0:
                self.saturation_deficit_avg = 0

            # Impervious area flow
            # ====================
            # Calculate the contribution of impervious areas to streamflow -
            # equation 37 in Wolock, 1993
            self.flow_predicted_impervious_area = (
                self.impervious_area_fraction * self.precip_for_recharge
            )

            # Total flow
            # ==========
            # Calculate the total flow in a given timestep
            # Equation 1 in Wolock, 1993
            self.flow_predicted_total = (
                self.flow_predicted_subsurface
                + self.flow_predicted_overland
            )

            # Channel routing
            # ===============
            # Calculate the flow delivered to the stream
            self.flow_predicted_stream = (
                self.flow_predicted_total
                * (1 - self.impervious_area_fraction)
                + self.flow_predicted_impervious_area
            )

            if self.flow_predicted_stream < 0:
                self.flow_predicted_stream = 0

            # Adjust the flow delivered to the stream by the
            # channel travel time
            self.flow_predicted_stream = (
                self.flow_predicted_stream / self.channel_travel_time
            )

            # Final predicted flow
            # ====================
            # Append the flow delivered to the stream to the final flow
            # predicted array
            self.flow_predicted[i] = self.flow_predicted_stream

            # Saving variables of interest
            # ============================
            self.saturation_deficit_avgs[i] = self.saturation_deficit_avg
