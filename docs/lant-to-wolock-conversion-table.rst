Table 1. Lookup table between variable names used in this code versus variable
names used in Wolock's Fortran code.

==========================================     =====================     ================================================================     ============================   =======================
Lant Python Code                               Wolock Fortran Code       Definition                                                           Units                          Notes
==========================================     =====================     ================================================================     ============================   =======================
timestep_daily_fraction                        DT                        Fraction of a daily timestep                                         fraction                                             
scaling_parameter                              SZM                       Scaling parameter based on soil properties                           millimeters                                             
saturated_hydraulic_conductivity               CONMEAN                   Saturated hydraulic conductivity of the C horizon of the soil        millimeters/day                                           
macropore_fraction                             PMAC                      Fraction of precipitation bypassing the soil zone                    fraction                                             
soil_depth_total                               ZTOT                      Total soil depth (zone AB + zone C)                                  meters                                                
soil_depth_ab_horizon                          ZAB                       Depth of AB horizon                                                  meters                                               
field_capacity_fraction                        THFC                      Field capacity of soil                                               fraction                                             
latitude                                       XLAT                      Latitude                                                             degrees                                                
basin_area_total                               ATOT                      Total watershed area                                                 square kilometers                                    
impervious_area_fraction                       PIMP                      Fraction of impervious area                                          fraction                                               
snowmelt_temperature_cutoff                    TCUT                      Temperature cutoff for snowpack accumulation and snowmelt            degrees Fahrenheit                                     
snowmelt_rate_coeff                            SNOPROP                   Snowmelt parameter                                                   inches/degree Fahrenheit                              
snowmelt_rate_with_rain_coeff                  RAINPRO                   Rain-induced snowmelt parameter                                      1/degree Fahrenheit                                    
channel_length_max                             DMAX                      Maximum channel length                                               kilometers                                           
channel_velocity_avg                           SUBV                      Channel velocity                                                     kilometers/day                                        
channel_travel_time                            NTW                       Channel travel time                                                  days
flow_initial                                   Q0                        Initial flow                                                         millimeters/day                                        
twi_values                                     ST                        ln(a/tanB) values                                                    ln(meters)                                             
twi_saturated_areas                            AC                        Saturated land-surface area in watershed                             fraction                                              
twi_mean                                       TL                        Mean of ln(a/tanB) distribution                                      ln(meters)                                             
num_twi_increments                             NAC                       Number of twi increments or bins                                     ---                                                     
precip                                         PP,P,PPT                  Precipitation rate                                                   millimeters/day                                       
pet                                            PET                       Potential evapotranspiration rate                                    millimeters/day                millimeters in Wolock     
precip_available                               PPTPET                    Precipiation - Potential evapotranspiration                          millimeters/day
num_timesteps                                  NSTEPS                    Number of timesteps; number of precipitation data values             ---
flow_predicted                                 QPRED                     Total predicted flow                                                 millimeters/day
soil_depth_roots                               ZROOT                     Root-zone depth                                                      meters
soil_depth_c_horizon                           ZAB                       Depth of AB horizon                                                  meters
vertical_drainage_flux_initial                 U0                        Initial vertical drainage flux                                       millimeters/day                CONMEAN*TSTEP in Wolock
transmissivity_saturated_max                   TRANS                     Maximum saturated transmissivity                                     square millimeters/day
flow_subsurface_max                            SZQ                       Maximum subsurface flow rate                                         millimeters/day
root_zone_storage_max                          SRMAX                     Maximum root-zone storage                                            millimeters
saturation_deficit_avg                         S                         Watershed average saturation deficit                                 millimeters 
vertical_drainage_flux                         UZ                        Vertical drainage flux; upper soil to saturated subsurface           millimeters/day
unsaturated_zone_storage                       SUZ                       Soil water available for drainage                                    millimeters
root_zone_storage                              SRZ                       Root zone storage                                                    millimeters
saturation_deficit_local                       SD                        Saturation deficit at location x                                     millimeters
precip_for_evaporation                         EPC                       The negative of precip minus pet                                     millimeters/day                -PPTPET in Wolock
precip_for_recharge                            PP                        The positive of precip minus pet                                     millimeters/day                PPTPET in Wolock
precip_excesses                                EX                        Precip in excess of pet and field capacity storage                   millimeters                    array
precip_excess                                  PPEX                      Precip in excess of pet and field capacity storage                   millimeters                    float
flow_predicted_overland                        QOF                       Predicted overland flow                                              millimeters/day
flow_predicted_vertical_drainage_flux          QUZ                       Predicted vertical drainage flux                                     millimeters/day                units? (UZ*AC(IA))
flow_predicted_subsurface                      QB                        Predicted subsurface flow                                            millimeters/day
flow_predicted_impervious_area                 --                        Predicted impervious area flow                                       millimeters/day                in Lant
flow_predicted_total                           QPRED                     Total predicted flow                                                 millimeters/day            
flow_predicted_stream                          QQ                        Flow delivered to stream channel                                     millimeters/day
==========================================     =====================     ================================================================     ============================   =======================
