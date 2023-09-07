.. role:: underline
    :class: underline

Namelist Variables
==================

.. role:: nlnote
    :class: nlnote

.. role:: nlheader
    :class: nlheader

The following tables provide namelist.input variable options and descriptions. Not all namelist parameters require an entry for each domain, and doing so can cause an error during processing. In the tables provided, note whether variables are a "single entry" or "max_dom" entry, where "max_dom" indicates a value is expected for each domain. Additional resources for namelist descriptions and recommendations can be found in 

* Registry/* files
* run/README.namelist (or test/em_real/README.namelist)
* test/em_real/examples.namelist

|

&time_control
-------------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/time_control_run.csv
   :widths: 20,30,35,15 

.. csv-table::
   :width: 100%
   :class: nlnote

   "start\_ times name the first wrfout file and control the start time for restarts. |br|
   start\_ and end\_ times control the start and end time for all domains. |br|
   start\_ and end\_ times are used by real.exe."

.. csv-table::
   :file: ./csv_files/time_control_start_end.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "\ |br|
   \"

.. csv-table::
   :file: ./csv_files/time_control_other.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following 5 rows are specific to the 3DVAR application"

.. csv-table::
   :file: ./csv_files/time_control_wrfda.csv
   :widths: 20,30,35,15
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the automatic moving nest application |br|
   WRF must have been compiled with nesting option 3"

.. csv-table::
   :file: ./csv_files/time_control_moving_nest.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the runtime I/O option"

.. csv-table::
   :file: ./csv_files/time_control_io.csv
   :widths: 20,30,35,15
   :width: 100%


|

|

&domains
--------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/domains_other.csv
   :widths: 20,30,35,15 

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to running real.exe"

.. csv-table::
   :file: ./csv_files/domains_real.csv
   :widths: 20,30,35,15 

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to vertical interpolation"

.. csv-table::
   :file: ./csv_files/domains_vert_interp.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Preset Moving Nest option |br|
   To use these options, the model must be compiled with nesting option 2 (preset-moves)"

.. csv-table::
   :file: ./csv_files/domains_preset_moves.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Automatic Moving Nest option |br|
   To use these options, the model must be compiled with nesting option 3 (vortex-following)"

.. csv-table::
   :file: ./csv_files/domains_auto_move.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Adaptive Time Step option"

.. csv-table::
   :file: ./csv_files/domains_adapts.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to controlling parallel computing"

.. csv-table::
   :file: ./csv_files/domains_parallel.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to using the 3D Ocean Model |br|
   sf_ocean_physics must be turned on in the &physics namelist to apply these options" 

.. csv-table::
   :file: ./csv_files/domains_ocean.csv
   :widths: 20,30,35,15

|

|

&physics
--------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :width: 100%
   :class: nlnote

   "For specifics and detailed descriptions of the following Microphysics options, see the Physics/Microphysics section of this Users' Guide."

.. csv-table::
   :file: ./csv_files/physics_mp_physics.csv
   :widths: 20,30,35,15 

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following settings are for the NSSL 1-moment microphysics scheme. |br|
   For the 1- and 2-moment schemes, the shape parameters for graupel and hail can also be set."

.. csv-table::
   :file: ./csv_files/physics_nssl_mp.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "For specifics and detailed descriptions of the following Radiation options, see the Physics/Radiation section of this Users' Guide."

.. csv-table::
   :file: ./csv_files/physics_radiation.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following aerosol options allow RRTMG and new Goddard radiation to recognize the aerosol option setting, but the aerosols are constant during model integration."

.. csv-table::
   :file: ./csv_files/physics_aer_rad.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following variables for CAM radiation are automatically set."

.. csv-table::
   :file: ./csv_files/physics_cam_rad.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "For specifics and detailed descriptions of the following Surface options, see the Physics/Surface section of this Users' Guide."

.. csv-table::
   :file: ./csv_files/physics_surface.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "For specifics and detailed descriptions of the following Planetary Boundary Layer (PBL) options, see the Physics/Planetary Boundary Layer section of this Users' Guide."

.. csv-table::
   :file: ./csv_files/physics_pbl.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "For specifics and detailed descriptions of the following Cumulus Parameterization options, see the Physics/Cumulus Parameterization section of this Users' Guide."

.. csv-table::
   :file: ./csv_files/physics_cumulus.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options show recommended values. If you would like to use any other value, consult the code to understand what you are doing."

.. csv-table::
   :file: ./csv_files/physics_cu_maxens.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the KF-CuP cumulus parameterization scheme (cu_physics=10)" 

.. csv-table::
   :file: ./csv_files/physics_cu_kfcup.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Morrison+CESM microphysics scheme (mp_physics=40)"

.. csv-table::
   :file: ./csv_files/physics_morr_cesm.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to Ocean model physics."

.. csv-table::
   :file: ./csv_files/physics_ocean.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to seaice."

.. csv-table::
   :file: ./csv_files/physics_seaice.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the lake model."

.. csv-table::
   :file: ./csv_files/physics_lake_model.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the lightning parameterization."

.. csv-table::
   :file: ./csv_files/physics_lightning.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the wind turbine drag parameterization."

.. csv-table::
   :file: ./csv_files/physics_wind_turbine.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the hailcasting."

.. csv-table::
   :file: ./csv_files/physics_hailcast.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the surface irrigation parameteriation and are only applicable when sf_surf_irr_scheme>0; new since V4.2."

.. csv-table::
   :file: ./csv_files/physics_surf_irr.csv
   :widths: 20,30,35,15 
   :width: 100%

.. csv-table::
   :width: 100%
   :class: nlnote

   "\ |br|
   \"

.. csv-table::
   :file: ./csv_files/physics_other.csv
   :widths: 20,30,35,15 
   :width: 100%

|

|

&stoch
------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/stoch_other.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Stochastic Kinetic-Energy Backscatter Scheme (SKEB); |br|
   used to perturb a forecast; |br|
   assumes rand_perturb=1"

.. csv-table::
   :file: ./csv_files/stoch_skebs_rand_pert1.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Stochastically-perturbed Physical Tendencies (SPPT), and assumes sppt=1"

.. csv-table::
   :file: ./csv_files/stoch_sppt1.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Stochastic Kinetic-energy Backscatter Scheme (SKEBS), and assumes skebs=1"

.. csv-table::
   :file: ./csv_files/stoch_skebs1.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the Stochastically-perturbed Parameter Scheme (SPP), and assumes spp=1"

.. csv-table::
   :file: ./csv_files/stoch_spp1.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to the WRF-Solar Stochastic Ensemble Prediction System (WRF-Solar EPS), and assumes multi_perturb=1; |br|
   new since V4.4"

.. csv-table::
   :file: ./csv_files/stoch_eps.csv
   :widths: 20,30,35,15

|

|

&dynamics
---------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/dynamics.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to deactivating 2nd and 6th order horizontal filters for specific scalar variable classes" 

.. csv-table::
   :file: ./csv_files/dynamics_2nd_6th_order.csv
   :widths: 20,30,35,15

|

|

&bdy_control
------------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/bdy_control.csv
   :widths: 20,30,35,15

|

|

&fdda
-----

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to Grid Nudging and assume grid_fdda=1 for each domain." 

.. csv-table::
   :file: ./csv_files/fdda_grid_nudge.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to Spectral Nudging and assume grid_fdda=2 for each domain." 

.. csv-table::
   :file: ./csv_files/fdda_spectral_nudge.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to Observational Nudging and assume obs_nudge_opt=1 for each domain." 

.. csv-table::
   :file: ./csv_files/fdda_obs_nudge.csv
   :widths: 20,30,35,15

|

|

&dfi_control
------------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to Digital Filter Initialization (DFI) and assume dfi_opt>0" 

.. csv-table::
   :file: ./csv_files/dfi.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following settings show an example for 1 hour backward integration for a model simulation that starts at 2004-03-13_12:00:00"

.. csv-table::
   :file: ./csv_files/dfi_backward.csv
   :widths: 20,30,35,15

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following settings specify 30 minutes of forward integration for a model simulation that starts at 2004-03-13_12:00:00" 

.. csv-table::
   :file: ./csv_files/dfi_forward.csv
   :widths: 20,30,35,15

|

|

&grib2
------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/grib2.csv
   :widths: 20,30,35,15

|

|

&scm
----

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35
   :width: 100%

   "Namelist Parameter","Default Setting","Description"

.. csv-table::
   :width: 100%
   :class: nlnote

   "The Single Column Model (SCM) can only be run for a single domain. All options require only a single entry in the namelist." 

.. csv-table::
   :file: ./csv_files/scm.csv
   :widths: 20,30,35


|

|

&tc
---

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/tc.csv
   :widths: 20,30,35,15

|

|

&diags
------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Pressure Level (max_plevs or max_zlevs)"

.. csv-table::
   :width: 100%
   :class: nlnote

   "To output fields on pressure levels, the following variables must also be set. For example, |br|
   auxhist23_outname=\'wrfpress_d<domain>_<date>\' (modify output stream and file name accordingly) |br|
   io_form_auxhist23=2 (2=netCDF file format) |br|
   auxhist23_interval=180,180 (interval in minutes for each domain) |br|
   frames_per_auxhist23=1,1 (number of files output per interval period)"

.. csv-table::
   :file: ./csv_files/diags.csv
   :widths: 20,30,35,15

|

|

&afwa
-----

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :width: 100%
   :class: nlnote

   "The following options are specific to AFWA diagnostics, and assumes afwa_daig_opt=1. |br|
   Note: These options cannot be used with an OpenMP configuration."

.. csv-table::
   :file: ./csv_files/afwa.csv
   :widths: 20,30,35,15

|

|

&ideal
------

|

.. csv-table::
   :class: nlheader
   :widths: 20,30,35,15
   :width: 100%

   "Namelist Parameter","Default Setting","Description","Single Entry or Entry for Each Domain (max_dom)"

.. csv-table::
   :file: ./csv_files/ideal.csv
   :widths: 20,30,35,15

|

|

