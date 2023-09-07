.. role:: underline
    :class: underline

WRF Output 
==========


WRF Output Fields
-----------------

By default, WRF outputs numerous variables that are included in the wrf history files (wrfout\*). However, there are options to remove some of the variables, to output additional variables, and to output certain variables to files other than the wrfout\* files. Valid fields depend on the model options used, and fields with zero values are not computed by the model options selected. To see a `full list of wrf output variables`_, issue the following command.

    ``ncdump -h wrfout_d<domain>_<date>``

.. _`full list of wrf output variables`: ./output_variables.html

|

Special WRF Output Variables
----------------------------

The WRF model outputs state variables (defined in the Registry/Registry.EM_COMMON file) that are used in the model's prognostic equations. Some of these variables are perturbation fields; therefore the following definitions for reconstructing meteorological variables are necessary:

|

.. csv-table::
   :width: 75%
   :widths: 50,40 

   "Total Geopotential", "PH + PHB"
   "Total Geopotential Height (in meters)", "(PH + PHB) / 9.81"
   "Total Potential Temperature (in K)", "T + 300"
   "Total Pressure (in mb)", "(P + PB) \* 0.01"
   "Wind Components (grid-relative)", "U, V"
   "Surface Pressure (in Pa)", "psfc"
   "Surface Winds (grid-relative)", "U10, V10 (valid at mass points)"
   "Surface Temperature", "T2"
   "Surface Mixing Ratio", "Q2"

|

**Definitions for map projection (map_proj) options**
        1 = Lambert Conformal |br|
        2 = Polar Stereographic |br|
        3 = Mercator |br|
        4 = Latitude and Longitude (including global)

|

Run-Time I/O Option
-------------------

Input/output (IO) decisions (such as which variables to output, and which variables are associated with which stream) can be updated via the Registry files (found in the Registry directory), but making any changes to the Registry constitutes a cycle of "clean -a," configure, and compile, which can sometimes be a lengthy process. The "run-time I/O" option allows these updates to be made at run-time, via the namelist.input file, by following these steps.

        .. note::
           Using the Run-time I/O option can cause a performance hit. Therefore, for production runs, it is recommended to make registry changes instead of using this option.

|

1. Create a text file (e.g., my_file_d0X.txt) for each domain in the directory where wrf.exe will be run. This/these file(s) define the output that will be modified. Contents of the file(s) associate a stream ID (for e.g., stream 0 is the default history and output) with a variable, and whether the field is added or removed. Following are a few examples.

   ``-:h:0:RAINC,RAINNC``
   removes the fields RAINC and RAINNC from the standard history file (stream 0).

   ``-:h:7:RAINC,RAINNC``
   adds the fields RAINC and RAINNC to an output stream 7, which creates a separate file from the wrfout\* files. 

|

   Available options are
        * **\+ or -** : add or remove a variable
        * **0-24** : which stream
        * **i** or **h** : input or history
        * **field name in the Registry file** (string displayed in column 9 in the registry file)

|

   Available auxiliary streams are
        * **Streams 0-24** are available
        * **0** : reserved for wrfout\* files
        * **23** : reserved for pressure level diagnostic output
        * **3** : reserved for extreme climate
        * **2** : reserved for AFWA diagnostic output
        * **6** : reserved for RASM diagnostic output
        * Generally, using any of the other streams (except 1) is okay

2. Add the following to the &time_control section of namelist.input

   ``iofields_filename="my-file_d01.txt","my-file_d01.txt"`` |br|
   ``ignore_iofields_warning=.true.``

|

        When outputting variables to a new stream (i.e., not history stream 0), the following namelist variables should be added to the &time_control section. The settings can be modified as needed.  For e.g., if you are adding to stream 7:

        ``auxhist7_outname="your-stream-name_d<domain>_<date>"`` |br|
        ``auxhist7_interval=360,360`` |br|
        ``frames_per_auxhist7=1, 1`` |br|
        ``io_form_auxhist4=2``

    .. note::
       Note: "your-stream-name" can be anything, but do not replace "_d<domain>_<date>." That is the syntax the model looks for.

|

**Other important notes regarding the Runtime I/O option**

        * Do not include any spaces in between fields in the .txt file.
        * Variable names in the .txt file must be identical to the quoted string name from the Registry file (column 9)
        * It is not necessary to remove fields from one stream to add them to another. The same field can be in multiple streams.
        * Any field requested in the .txt file must already be declared as a state variable in the Registry.
        * *ignore_iofields_warning* namelist setting tells the program what to do if it encounters an error in the .txt file(s). The default is .true., which prints a warning message, but continues the run. If set to .false., the simulation aborts if there are errors in the .txt file(s).

|

Output Diagnostics
------------------

|

Time Series Output
++++++++++++++++++

Outputting time series data at particular locations within your domain can be useful for tracking the progression of particular variables.

To activate this option, a file called **tslist** must present in the WRF running directory. The tslist file contains a list of locations defined by their latitude and longitude, or i,j coordinates, along with a short description and abbreviation for each location. Create the tslist file following this format. 


    .. note::
       The first three lines are regarded as header information, and are ignored by the model.
    
| 
    
     ``#-----------------------------------------------#`` |br|
     ``# 24 characters for name | pfx |  LAT  |   LON  |`` |br|
     ``#-----------------------------------------------#`` |br|
     ``Cape Hallett              hallt -72.330  170.250`` |br|
     ``McMurdo Station           mcm   -77.851  166.713``

|

If cell locations are to be used (e.g., for idealized cases), the i,j locations are to be specified as follows.

     ``#-----------------------------------------------#`` |br|
     ``# 24 characters for name | pfx |   I   |    J   |`` |br|
     ``#-----------------------------------------------#`` |br|
     ``tower0001                 t0001  10       10`` |br|
     ``tower0002                 t0002  20       20`` |br|
     ``tower0003                 t0003  30       30``

|

After wrf is run, for each location listed in tslist that exists inside the model domain (either coarse or nested), the following files are written.

        **pfx*.d0x.TS** containing the regular time series output of surface variables. |br|
        **pfx.d0x.UU** containing a vertical profile of u wind component for each time step |br|
        **pfx.d0x.VV** containing a vertical profile of v wind component for each time step |br|
        **pfx.d0x.WW** containing a vertical profile of w wind component for each time step |br|
        **pfx.d0x.TH** containing a vertical profile of potential temperature for time step |br|
        **pfx.d0x.PH** containing a vertical profile of geopotential height for each time step |br|
        **pfx.d0x.QV** containing a vertical profile of water vapor mixing ratio for each time step |br|
        **pfx.d0x.PR** containing a vertical profile of pressure for each time step

        where 

                **pfx** : the specified prefix for the location in the tslist file |br|
                **d0x** : the domain ID, as given in namelist.input
          
|

**namelist.input variables specific to time-series output** 
        * **max_ts_locs** : maximum number of locations in 'tslist' ( default is 5) |br|
        * **ts_buf_size** : buffer size for time series output (default is 200) |br|
        * **max_ts_level** : number of model levels for time series vertical profiles (default is 15). The maximum number of max_ts_level is e_vert-1 (the number of half layers in the model run) |br|
        * **tslist_unstagger_winds** : output the unstaggered u, v, and w component winds (default is false)

|

    .. note::
       Locations specified in the tslist file that do not exist in any domain are ignored by the time series capability.

|

    .. note::
       Additional information regarding this option can be found in the WRF/run/README.tslist file within the code.

|

Pressure Level Output
+++++++++++++++++++++

This option outputs the following extra fields to a number of pressure levels.
        * U and V wind speed
        * T (temperature)
        * Dewpoint temperature
        * Relative humididy (RH)
        * Geopotential Height

To activate this option, add the following to the **&diags** section of namelist.input. For e.g.,

        ``p_lev_diags=1`` |br|
        ``num_press_levels=4`` |br|
        ``press_levels= 85000, 70000, 50000, 20000``

The extra fields are output to auxiliary stream 23, and therefore the following should be set in **&time_control** in namelist.input. For e.g., 

        ``auxhist23_interval = 360, 360`` |br|
        ``frames_per_auxhist23 = 100, 100`` |br|
        ``io_form_auxhist23 = 2``

|

Convective Storm Diagnostics
++++++++++++++++++++++++++++

This option outputs the following extra fields in the history file (wrfout*).
        * maximum 10 m wind speed
        * maximum helicity in 2 - 5 km layer
        * maximum vertical velocity in updraft and downdraft below 400 mb
        * mean vertical velocity in 2 - 5 km layer
        * maximum column graupel in a time window between history output times

To activate this option, add the following namelist settings.

        ``nwp_diagnostics = 1`` (&time_control) |br|
        ``do_radar_ref = 1`` (&physics)

|

Climate Diagnostics
+++++++++++++++++++

This option outputs 48 surface diagnostic variables. For **T2, Q2, TSK, U10, V10, 10 m wind speed, RAINCV, RAINNCV,** the following are calculated:
        * maximum and minimum
        * times when max and min occur
        * mean value
        * standard deviation of the mean


Output goes to auxiliary stream 3. To activate this option, add the following settings in **&time_control** in namelist.input. For e.g., 

        ``output_diagnostics = 1`` |br|
        ``auxhist3_outname = "wrfxtrm_d<domain>_<date>"`` |br|
        ``auxhist3_interval = 1440, 1440`` |br|
        ``frames_per_auxhist3 = 100, 100`` |br|
        ``io_form_auxhist3 = 2``

|

     .. note::
        Because the daily max and min, etc. are computed, it is advised to do a restart only at a multiple of auxhist3_intervals.

|

Time-averaged Output
++++++++++++++++++++

This option outputs history time-averaged column-pressure coupled U, V and W for downstream transport models.

To activate this option, add the following to **&dynamics** in namelist.input.

        ``do_avgflx_em = 1``

Additionally, if a Grell cumulus scheme is used, set the following in **&dynamics** in namelist.input to output time-averaged convective mass-fluxes.

        ``do_avg_cugd = 1``

|

Weather Diagnostics
+++++++++++++++++++

*(contributed by AFWA)*

This option outputs diagnostic variables to auxiliary stream 2. See `full documentation_`.

|

    .. note::
       This option cannot be used with code compiled with OpenMP.

|

To activate this option, add the following to namelist.input.

        ``&afwa`` |br|
        ``afwa_diag_opt=1``

And then set any of the following options to **1** to output specific fields (set for each domain - default is 0=off).

        ``afwa_ptype_opt = 1,1`` (precipitation type) |br|
        ``afwa_vil_opt = 1, 1`` (vertical integrated liquid)  |br|
        ``afwa_radar_opt = 1, 1`` (radar) |br|
        ``afwa_severe_opt = 1, 1`` (severe weather) |br|
        ``afwa_icing_opt = 1, 1`` (icing) |br|
        ``afwa_vis_opt = 1, 1`` (visibility) |br|
        ``afwa_cloud_opt = 1, 1`` (cloud) |br|
        ``afwa_therm_opt = 1, 1`` (thermal indices) |br|
        ``afwa_turb_opt = 1, 1`` (turbulence) |br|
        ``afwa_buoy_opt = 1, 1`` (buoyancy)

The following may also be set in **&afwa** if **afwa_ptype_opt=1**

        ``afwa_ptype_ccn_temp = 264.15`` (CCN temperature for precipitation type calculation) |br|
        ``afwa_ptype_tot_melt = 50`` (total melting energy for precipitation type calculation)
 

.. _`full documentation` : https://www2.mmm.ucar.edu/wrf/users/docs/AFWA_Diagnostics_in_WRF.pdf

|

Solar Forecasting Diagnostics
+++++++++++++++++++++++++++++

This option outputs the following variables to the wrf output files (wrfout\*).
        * Solar zenith angle
        * Clearness index
        * 2D maximum cloud fraction
        * Paths for water vapor, liquid water, ice water, and snow water
        * Effective radius for liquid cloud, ice, and snow
        * Optical thickness for liquid cloud, ice, and snow
        * Cloud base height and top height
        * For liquid and ice variables, the "total" water path (liquid + ice + snow), effective radius, and optical thickness are calculated, where the "total" variables account for subgrid hydrometeors.
        * Accumulated GHI *(since V4.4)*

To activate this option, set the following in the **&diags** section of namelist.input.
       
        ``solar_diagnostics = 1``

|

    .. note::
       If tslist is also present, these same variables are written to the respective time series file(s)

|

Accumulated Physics Tendencies Output
+++++++++++++++++++++++++++++++++++++

This option outputs 16 accumulated physics tendencies for the following variables.
        * Potential temperature
        * Water vapor mixing ratio
        * u and v components of the wind. 
          
To activate this option, add the following to the **&physics** section of namelist.input.

        ``acc_phy_temd = 1``

|

Miscellaneous Output Options
++++++++++++++++++++++++++++

        **do_radar_ref = 1** : Add to **&physics** to compute radar reflectivity using microphysics-specific parameters in the model. |br|
          *This option works with mp_physics= 2, 4, 6, 7, 8, 10, 14, 16, 17, 18, 19, 21, 24, 26, 28* 
       
        **prec_acc_dt = 60** : Add to **&physics** to provide a time interval for outputting precipitation variables (rain from cumulus and microphysics schemes, and snow from microphysics), in minutes.

|

|

Using Multiple Lateral Boundary Condition Files
-----------------------------------------------

To speed up pre-processing of lateral boundary conditions in real-time scenarios, an option is available to create multiple lateral condition files. This allows a boundary condition file to be created as soon as the surrounding time periods become available, allowing the model to start the simulation sooner. 

To activate this option, add the following to namelist.input.

        ``bdy_inname = "wrfbdy_d<domain>_<date>"`` (in &time_control) |br|
        ``multi_bdy_files = .true.`` (in &bdy_control)

|

    .. note::
       Prior to V4.2, this must be done through a compile option (adding ``-D_MULTI_BDY_FILES_`` in ARCH_LOCAL in the configure.wrf file). 

|

Output files are in the following format (for e.g., using a 6-hourly data interval)
        wrfbdy_d01_2000-01-24_12:00:00 |br|
        wrfbdy_d01_2000-01-24_18:00:00 |br|
        wrfbdy_d01_2000-01-25_00:00:00 |br|
        wrfbdy_d01_2000-01-25_06:00:00

|

|

Checking Output
---------------

Once a model run completes, it is advised to quickly check a few things.

If WRF was built with distributed memory (dmpar), there should be an rsl.out.* and rsl.error.* file for each processor. If the simulation was successful, the message **SUCCESS COMPLETE WRF** should be printed at the end of these files. This can quickly be checked by typing

        ``tail rsl.out.0000``

All options in namelist.input are preserved to a filed named **namelist.output**.

To check the output times written to a netCDF file, the following netCDF command can be used (for example), 

        ``ncdump -v Times wrfout_d01_yyyy-mm-dd_hh:00:00``

To see the time computations take for each model time step, the time it takes to write a history file, or a restart file, open the rsl.out.0000 file (or other standard-out files), which logs these times. For example, 

**Model Time Steps**
        ``Timing for main: time 2006-01-21_23:55:00 on domain  2:    4.91110 elapsed seconds.`` |br|
        ``Timing for main: time 2006-01-21_23:56:00 on domain  2:    4.73350 elapsed seconds.`` |br|
        ``Timing for main: time 2006-01-21_23:57:00 on domain  2:    4.72360 elapsed seconds.`` |br|
        ``Timing for main: time 2006-01-21_23:57:00 on domain  1:   19.55880 elapsed seconds.``

**History File**
        ``Timing for Writing wrfout_d02_2006-01-22_00:00:00 for domain 2: 1.17970 elapsed seconds.`` |br|
        ``Timing for main: time 2006-01-22_00:00:00 on domain 1: 27.66230 elapsed seconds.`` |br|
        ``Timing for Writing wrfout_d01_2006-01-22_00:00:00 for domain 1: 0.60250 elapsed seconds.``

|

|

|

|
