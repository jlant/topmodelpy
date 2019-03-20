"""Test Topmodel class."""

import numpy as np

from topmodelpy.topmodel import Topmodel


def test_topmodel_init(parameters_wolock,
                       timeseries_wolock,
                       twi_wolock,
                       twi_weighted_mean_wolock):
    """Test Topmodel class initialization"""

    # Initialize Topmodel
    topmodel = Topmodel(
        scaling_parameter=parameters_wolock["scaling_parameter"],
        saturated_hydraulic_conductivity=(
            parameters_wolock["saturated_hydraulic_conductivity"]
        ),
        macropore_fraction=parameters_wolock["macropore_fraction"],
        soil_depth_total=parameters_wolock["soil_depth_total"],
        soil_depth_ab_horizon=parameters_wolock["soil_depth_ab_horizon"],
        field_capacity_fraction=parameters_wolock["field_capacity_fraction"],
        latitude=parameters_wolock["latitude"],
        basin_area_total=parameters_wolock["basin_area_total"],
        impervious_area_fraction=parameters_wolock["impervious_area_fraction"],
        twi_values=twi_wolock["twi"].values,
        twi_saturated_areas=twi_wolock["proportion"].values,
        twi_mean=twi_weighted_mean_wolock,
        precip_available=timeseries_wolock["precip_minus_pet"].values,
        flow_initial=1,
        soil_depth_roots=1,
        timestep_daily_fraction=1
    )

    assert(topmodel.scaling_parameter ==
           parameters_wolock["scaling_parameter"])
    assert(topmodel.saturated_hydraulic_conductivity ==
           parameters_wolock["saturated_hydraulic_conductivity"])
    assert(topmodel.macropore_fraction ==
           parameters_wolock["macropore_fraction"])
    assert(topmodel.soil_depth_total ==
           parameters_wolock["soil_depth_total"])
    assert(topmodel.soil_depth_ab_horizon ==
           parameters_wolock["soil_depth_ab_horizon"])
    assert(topmodel.field_capacity_fraction ==
           parameters_wolock["field_capacity_fraction"])
    assert(topmodel.latitude ==
           parameters_wolock["latitude"])
    assert(topmodel.basin_area_total ==
           parameters_wolock["basin_area_total"])
    assert(topmodel.impervious_area_fraction ==
           parameters_wolock["impervious_area_fraction"])
    np.testing.assert_allclose(topmodel.twi_values,
                               twi_wolock["twi"].values)
    np.testing.assert_allclose(topmodel.twi_saturated_areas,
                               twi_wolock["proportion"].values)
    assert(topmodel.twi_mean ==
           twi_weighted_mean_wolock)
    np.testing.assert_allclose(topmodel.precip_available,
                               timeseries_wolock["precip_minus_pet"].values)
    assert(topmodel.flow_initial == 1)
    assert(topmodel.soil_depth_roots == 1)
    assert(topmodel.timestep_daily_fraction == 1)


def test_topmodel_run(parameters_wolock,
                      timeseries_wolock,
                      twi_wolock,
                      twi_weighted_mean_wolock):
    """Test Topmodel run with input data from Dave Wolock's Topmodel version.
    Note:
        This version and Wolock's version produce predicted flow values are
        are close (max difference is 0.047 or 4.7%). However, there are small
        differences likely due to a slightly different twi mean values and
        floating point differences from rounding.  This test allows for a 
        small relative tolerance (rtol) of 0.05 for assertions.

    Reference:
        Python Relative tolerance (rtol) vs Absolute tolerance (atol)
        https://www.python.org/dev/peps/pep-0485/#defaults
    """

    # Initialize Topmodel
    topmodel = Topmodel(
        scaling_parameter=parameters_wolock["scaling_parameter"],
        saturated_hydraulic_conductivity=(
            parameters_wolock["saturated_hydraulic_conductivity"]
        ),
        macropore_fraction=parameters_wolock["macropore_fraction"],
        soil_depth_total=parameters_wolock["soil_depth_total"],
        soil_depth_ab_horizon=parameters_wolock["soil_depth_ab_horizon"],
        field_capacity_fraction=parameters_wolock["field_capacity_fraction"],
        latitude=parameters_wolock["latitude"],
        basin_area_total=parameters_wolock["basin_area_total"],
        impervious_area_fraction=parameters_wolock["impervious_area_fraction"],
        twi_values=twi_wolock["twi"].values,
        twi_saturated_areas=twi_wolock["proportion"].values,
        twi_mean=twi_weighted_mean_wolock,
        precip_available=timeseries_wolock["precip_minus_pet"].values,
        flow_initial=1,
        soil_depth_roots=1,
        timestep_daily_fraction=1
    )

    topmodel.run()

    diff = (topmodel.flow_predicted
            - timeseries_wolock["flow_predicted"].values)
    print("Difference between Lant and Wolock: {}".format(diff))
    print("Max difference: {}".format(max(diff)))
    print("The difference occurred at index: {}".format(np.where(diff ==
                                                                 max(diff))))
    np.testing.assert_allclose(topmodel.flow_predicted,
                               timeseries_wolock["flow_predicted"].values,
                               rtol=0.05)
