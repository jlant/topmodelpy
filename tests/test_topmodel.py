"""Test Topmodel class."""

import numpy as np

from topmodelpy.topmodel import Topmodel
from topmodelpy import utils


def test_topmodel_init(wolock_parameters_data,
                       wolock_timeseries_data,
                       wolock_twi_data,
                       wolock_twi_weighted_mean):
    """Test Topmodel class initialization"""

    # Initialize Topmodel
    topmodel = Topmodel(
        scaling_parameter=wolock_parameters_data["scaling_parameter"],
        saturated_hydraulic_conductivity=wolock_parameters_data["saturated_hydraulic_conductivity"],
        macropore_fraction=wolock_parameters_data["macropore_fraction"],
        soil_depth_total=wolock_parameters_data["soil_depth_total"],
        soil_depth_ab_horizon=wolock_parameters_data["soil_depth_ab_horizon"],
        field_capacity_fraction=wolock_parameters_data["field_capacity_fraction"],
        latitude=wolock_parameters_data["latitude"],
        basin_area_total=wolock_parameters_data["basin_area_total"],
        impervious_area_fraction=wolock_parameters_data["impervious_area_fraction"],
        twi_values=wolock_twi_data["twi"].values,
        twi_saturated_areas=wolock_twi_data["proportion"].values,
        twi_mean=wolock_twi_weighted_mean,
        precip=wolock_timeseries_data["precipitation"].values,
        pet=wolock_timeseries_data["pet"].values,
        flow_initial=1,
        soil_depth_roots=1,
        timestep_daily_fraction=1
    )

    assert(topmodel.scaling_parameter ==
           wolock_parameters_data["scaling_parameter"])
    assert(topmodel.saturated_hydraulic_conductivity ==
           wolock_parameters_data["saturated_hydraulic_conductivity"])
    assert(topmodel.macropore_fraction ==
           wolock_parameters_data["macropore_fraction"])
    assert(topmodel.soil_depth_total ==
           wolock_parameters_data["soil_depth_total"])
    assert(topmodel.soil_depth_ab_horizon ==
           wolock_parameters_data["soil_depth_ab_horizon"])
    assert(topmodel.field_capacity_fraction ==
           wolock_parameters_data["field_capacity_fraction"])
    assert(topmodel.latitude ==
           wolock_parameters_data["latitude"])
    assert(topmodel.basin_area_total ==
           wolock_parameters_data["basin_area_total"])
    assert(topmodel.impervious_area_fraction ==
           wolock_parameters_data["impervious_area_fraction"])
    np.testing.assert_allclose(topmodel.twi_values,
                               wolock_twi_data["twi"].values)
    np.testing.assert_allclose(topmodel.twi_saturated_areas,
                               wolock_twi_data["proportion"].values)
    assert(topmodel.twi_mean ==
           wolock_twi_weighted_mean)
    np.testing.assert_allclose(topmodel.precip,
                               wolock_timeseries_data["precipitation"].values)
    np.testing.assert_allclose(topmodel.pet,
                               wolock_timeseries_data["pet"].values)
    assert(topmodel.flow_initial == 1)
    assert(topmodel.soil_depth_roots == 1)
    assert(topmodel.timestep_daily_fraction == 1)


def test_topmodel_run(wolock_parameters_data,
                      wolock_timeseries_data,
                      wolock_twi_data,
                      wolock_twi_weighted_mean):
    """Test Topmodel run with input data from Dave Wolock's Topmodel version"""

    # Initialize Topmodel
    topmodel = Topmodel(
        scaling_parameter=wolock_parameters_data["scaling_parameter"],
        saturated_hydraulic_conductivity=wolock_parameters_data["saturated_hydraulic_conductivity"],
        macropore_fraction=wolock_parameters_data["macropore_fraction"],
        soil_depth_total=wolock_parameters_data["soil_depth_total"],
        soil_depth_ab_horizon=wolock_parameters_data["soil_depth_ab_horizon"],
        field_capacity_fraction=wolock_parameters_data["field_capacity_fraction"],
        latitude=wolock_parameters_data["latitude"],
        basin_area_total=wolock_parameters_data["basin_area_total"],
        impervious_area_fraction=wolock_parameters_data["impervious_area_fraction"],
        twi_values=wolock_twi_data["twi"].values,
        twi_saturated_areas=wolock_twi_data["proportion"].values,
        twi_mean=wolock_twi_weighted_mean,
        precip=wolock_timeseries_data["precipitation"].values,
        pet=wolock_timeseries_data["pet"].values,
        flow_initial=1,
        soil_depth_roots=1,
        timestep_daily_fraction=1
    )

    topmodel.run()

    diff = (topmodel.flow_predicted
            - wolock_timeseries_data["flow_predicted"].values)
    print(np.where(diff == max(diff)))
    print(topmodel.flow_predicted[181])
    print(wolock_timeseries_data["flow_predicted"].values[181])
    print(topmodel.flow_predicted[:10])
    print(wolock_timeseries_data["flow_predicted"].values[:10])
    # np.testing.assert_allclose(topmodel.flow_predicted,
    #                           wolock_timeseries_data["flow_predicted"].values,
    #                           rtol=1)
