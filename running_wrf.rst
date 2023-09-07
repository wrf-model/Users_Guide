.. role:: underline
    :class: underline

Running WRF
===========

|

By default, the WRF model is a fully compressible, nonhydrostatic model with a hybrid vertical hydrostatic pressure coordinate (HVC), and Arakawa C-grid staggering. The model uses the Runge-Kutta 2nd and 3rd order time integration schemes, and 2nd to 6th order advection schemes in both the horizontal and vertical. It uses a time-split small step for acoustic and gravity-wave modes. The dynamics conserves scalar variables.

WRF model code contains an initialization program for either real-data (real.exe) or idealized data (ideal.exe), a numerical integration program (wrf.exe), a program allowing one-way nesting for domains run separately (ndown.exe), and a program for tropical storm bogussing (tc.exe). Version 4 of the WRF model supports a variety of capabilities, including

* Real-data and idealized simulations
* Various lateral boundary condition options 
* Full physics options, with various filters
* Positive-definite advection scheme
* Hydrostatic runtime option
* Terrain-following vertical coordinate option
* One-way, two-way, and moving nest options
* Three-dimensional analysis nudging
* Observation nudging
* Regional and global applications
* Digital filter initialization
* Vertical refinement for a nested domain

|

Running Idealized Cases
-----------------------
To run an idealized simulation, the model must have been compiled for the idealized test case of choice, with either a serial compiling option (mandatory for the 1-D and 2-D test cases, or with a parallel computing option (e.g., dmpar, allowed for 3-D test cases). See the following instructions for either a 2-D idealized case, or a 3-D idealized case.

**3-D Baroclinic Wave Case**

#. Move to the case running directory.

.. code-block::
        
        > cd WRF/test/em_b_wave

#. Edit the namelist.input file to set integration length, output frequency, domain size, timestep, physics options, and other parameters (see 'README.namelist' in the WRF/run directory, or `namelist options`_), and then save the file. 

#. Run the ideal initialization program. 
    * For a serial build: 
      
    .. code-block::

            > ./ideal.exe >& ideal.log

    * For a parallel build: 

    .. code-block::  
    
            > mpirun -np 1 ./ideal.exe 

|br|
    
    .. note::    
       ideal.exe must be run with only a single processor (denoted by "-np 1"), even if the code is built for parallel computing.

This program typically reads an input sounding file provided in the case directory, and generates an initial condition file ‘wrfinput_d01.’ Idealized cases do not require a lateral boundary file because boundary conditions are handled in the code via namelist options. If the job is successful, the bottom of the “ideal.log” file (or rsl.out.0000 file for parallel execution) should read **SUCCESS COMPLETE IDEAL INIT**.

#. Then to run the WRF model, type
    * For a serial build: 

    .. code-block::  
    
            > ./wrf.exe >& wrf.log

|br|
    * For a parallel build (*where here we are asking for 8 processors*): 
    
    .. code-block::

            > mpirun -np 8 ./wrf.exe

|br|

Pairs of *rsl.out.\** and *rsl.error.\** files will appear with MPI runs. These are standard out and error files. There will be one pair for each processor used. If the simulation was  successful, the wrf output is written to a file named "wrfout_d01_0001-01-01_00:00:00," and the end of the "wrf.log" file (or rsl.out.0000) should read **wrf: SUCCESS COMPLETE WRF**.

Output files *wrfout_d01_0001-01-01\** and restart files *wrfrst\** should be present in the run directory, depending on how namelist variables are specified for output. The time stamp on these files originates from the start times in the namelist file.

|

|
   
Running Real-data Cases
-----------------------

#.  To run the model for a real-data case, move to the working directory by issuing the command

    .. code-block::

	    > cd WRF/test/em_real
            or 
            > cd WRF/run

#.  Prior to running a real-data case, the WRF Preprocessing System (WPS) must have been successfully run, producing "met_em.*" files. Link the met_em* files to the WRF running directory.

    .. code-block::

	    > ln -sf ../../../WPS/met_em* .

#.  Start with the default *namelist.input* file in the directory and edit it for your case. 
	* Make sure the parameters in the *time_control* and *&domains* sections are set specific to your case 
	* Make sure dates and dimensions of the domain match those set in WPS. If only one domain is used, only entries in the first column are read and other columns are ignored. No need to remove additional columns.

#. Run the real-data initialization program. 

        * For WRF built for serial computing, or OpenMP - smpar
          
        .. code-block::

                > ./real.exe >& real.log
       
        * For WRF built for parallel computing - dmpar - an example requesting to run with four processors        
           
        .. code-block::

                > mpiexec -np 4 ./real.exe

|br|

The real.exe program uses the 2-D output (met_em* files) created by the WPS program to perform vertical interpolation for 3-D meteorological fields and sub-surface soil data, and creates boundary and initial condition files to feed into the wrf.exe program.

If successful, the end of the real.log (or rsl.out.0000 file) should read "**real_em: SUCCESS EM_REAL INIT**." There should also now be "wrfinput_d0* files (one file per domain) and a "wrfbdy_d01" file, which are used as input to the wrf.exe program. 

* Run the WRF model
	* For WRF built for serial computing, or OpenMP - smpar

        .. code-block::

	        > ./wrf.exe >& real.log

        * For WRF built for parallel computing - dmpar - an example requesting to run with four processors

        .. code-block::

                > mpiexec -np 4 ./wrf.exe

|br|

Pairs of rsl.out.* and rsl.error.* files will appear with MPI runs (one pair for each processor). These are standard out and error files. If the simulation is successful, wrf output is written to a file named *wrfout_d<domain>_<date>_<time>*, (where *<domain>* represents domain ID, and *<date>* represents a date string with the format *yyyy-mm-dd_hh:mm:ss*. The time given in the file name is the first time the output file is written, but depending on the setting for "frames_per_outfile" in the namelist, there can be multiple times available in each file. Check the times written to the output file by typing

.. code-block::

        > ncdump -v Times wrfout_d01_2000-01-24_12:00:00

|br|

Restart files can also be created by setting "restart_interval" in namelist.input to a time interval within the total integration time. Restart file(s) have the following naming convention, where the time stamp is the time at which that restart file is valid.

.. code-block::

        > wrfrst_d<domain>_<date>

|

Restart Capability
------------------

The restart capability allows extending a run to a longer simulation period when there is a reason it cannot be run at one time (e.g., the run extends beyond available wallclock time). It is effectively a continuous run made of multiple shorter runs; hence the results at the end of one or more restart runs should be identical to a single run without any restart.
|br|
|br|
To initiate the restart run, 

#. Prior to the initial simulation, set "restart_interval" in the namelist.input file to a value (in minutes) equal to or less than the simulation length of the initial model run. This creates a restart file that is written out when the model reaches the restart_interval. The file will have the naming convention "wrfrst_d<domain>_<date>," where the date string represents the time when the restart file is valid.

#. After the initial simulation completes, and there is a valid "wrfrst_d<domain>_<date>" file available, modify the namelist again by setting
	* **start_time** =  the restart time (<date> of the restart file) (in &time_control) 
	* **restart** = .true. (in &time_control) 

Some other namelist options to use for restarts are
	* **override_restart_timers=.true.**: Use this if the history and/or restart interval are modified prior to the restart run, and the new output times are not as expected (in &time_control)
	* **write_hist_at_0h_rst=.true.**: If history output is desired at the initial time of the restart simulation (in &time_control)

    .. note::
       Restart files are typically several times the size of history files. The model may be capable of writing history files (wrfout files) in netCDF format, but may fail to write a restart file because basic netCDF file support is only 2GB; however, by default WRF code compiles with large file support, which allows files up to 4GB. If you are still reaching this maximum, you can set "io_form_restart=102" (instead of 2), which forces the restart file to be written into multiple pieces, one per processor. As long as the model is restarted using the same number of processors (which is the recommended practice anyway), this option works well.

| 

|

WRF Nesting
-----------

A nested simulation is one in which a coarse-resolution domain (parent) contains at least one finer-resolution domain (child) embedded. These domains can be run together at the same time, or separately. The nest receives data driven along its lateral boundaries from its parent, and depending on the namelist setting for "feedback," the nest may also provide data back to the parent.

To determine whether a nest is needed, determine the size of the area necessary to fully encompass the phenomenon of interest, and keep in mind there needs to be considerable space around all sides of that area to serve as a buffer zone. Next determine the resolution necessary to resolve the event, as well as the resolution of the input data. A nest will be needed if
	* the input data are too coarse, by more than a factor of about 5-10x the resolution of the resolution required to resolve the phenomenon of interest. There will need to be a parent (or more) around the highest-resolution domain to ensure smoothness. Having too much of a difference between resolution of parents to children (including the difference between parent domain and the first-guess model input resolution) can cause unnecessary problems at the boundaries. For example, if needing to simulate an area at 3 km resolution, but the input data have a resolution of 1 degree (which is about 111 km), the grid ratio would be 37:1, which is much too large. 
	* the domain size is significantly increasing computational cost. To ensure the large-scale and meso- and/or micro-scale components are all resolved, depending on the size of the phenomemon of interest, the domain may need to be fairly large. If the entire area were at the highest resolution necessary, this could become computationally expensive. To address this, consider only putting the finest resolution over the exact area of interest (with reasonable space to buffer), and using a more-coarse-resolution domain to surround it. *Note: the solution can be affected by nest domain sizes.*

There are different types of nesting options. Click the links below to go to each section. 

| 

Basic Nesting
+++++++++++++

Simulating WRF with basic nesting allows either a **one-way** or **two-way** nesting option. 

A two-way nested simulation includes multiple domains at different grid resolutions that are run simultaneously and communicate with each other. The coarser (parent) domain provides boundary values for the higher-resolution nest (child), and the nest feeds its calculation back to the coarser domain. The model can handle multiple domains at the same nest level (no overlapping nests), and multiple nest levels (telescoping). With one-way nesting, communication only goes in one direction - from the parent domain to the child domain. There is no feedback to the parent.  

When preparing for a nested run, make sure code is compiled with "basic" nest option (option 1).

Nesting options are declared in the namelist. Variables that have multiple columns need to be edited (do not add columns to parameters that do not have multiple column values in the default namelist). Start with the default namelist. The following are the key namelist variables to modify:

.. csv-table::
   :width: 100%
   :widths: 20, 70
   :escape: \

   **feedback**, this is the key setup to define a two-way nested (or one-way nested) run. When feedback is on (=1)\, values of the coarse domain are overwritten by values of the variables (average of cell values for mass points\, and average of the cell-face values for horizontal momentum points) in the nest at coincident points. For masked fields\, only the single point value at the collocating points is fed back. If the parent_grid_ratio is even\, an arbitrary choice of the southwest corner point value is used for feedback\, which is why it is better to use an odd parent_grid_ratio when feedback=1. When feedback is off (=0)\, it is equivalent to a one-way nested run\, since nest results are not reflected in the parent domain.
   **start_\*** |br| **end_\***, start and end simulation times for the nest
   **input_from_file**, whether a nest requires an input file (e.g. wrfinput_d02). This is typically used for a real data case\, since the nest input file contains nest topography and land information.
   **fine_input_stream**, determines which fields (defined in Registry/Registry.EM_COMMON) from the nest input file are used in nest initialization. This typically includes static fields (e.g.\, terrain and landuse)\, and masked surface fields (e.g.\, skin temperature\, soil moisture and temperature). This option is useful for a nest starting at a later time than the coarse domain. See setting options in the namelist descriptions.
   **max_dom**, the total number of domains to run. For example\, if you want to have one coarse domain and one nest\, set this variable to 2.
   **grid_id**, domain identifier used in the wrfout naming convention. *The most coarse grid must have a grid_id of 1*.
   **parent_id**, indicates the parent domain of a nest. This should be set as the grid_id value of the parent (e.g.\, d02's parent is d01\, so parent_id for column two should be set to 1).
   **i_parent_start** |br| **j_parent_start**, lower-left corner starting indices of the nest domain within its parent domain. These parameters should be the same as in namelist.wps.
   **parent_grid_ratio**, integer grid size (resolution) ratio of the child domain to its parent. Typically odd number ratios are used in real-data applications (ratios of 3:1 and 5:1 have shown the best results; no more than 7:1).
   **parent_time_step_ratio**, integer time-step ratio for the nest domain\, which can be different from the parent_grid_ratio\, though they are typically set the same.
   **smooth_option**, a smoothing option for the parent domain in the area of the nest if feedback is on. Three options are available: 0 = no smoothing; 1 = 1-2-1 smoothing; 2 = smoothing-desmoothing.

|

|

One-way Nesting Using Ndown
+++++++++++++++++++++++++++

The **ndown** program is a tool used to run one-way nesting when the finer-grid-resolution domain is run subsequently after the coarser-grid-resolution run. The *ndown.exe* executable is run in between the two simulations. The initial and lateral boundary conditions for this finer-grid run are obtained from the coarse grid run, with input from higher resolution terrestrial fields (e.g. terrain, landuse, etc.), and masked surface fields (such as soil temperature and moisture). The ndown program can be useful for the following scenarios.

                * If a long simulation (e.g., several years) has already been run, and it is later decided to embed a nest with higher-resolution. 
                * If there are several nests and the number of grid points in one or more of the inner-most domains is much greater than the number of points in the parent domain(s). Most likely it will be necessary to use more processors to simulate the larger domains, but it is not possible to use too many processors for the smaller domains (an error will occur). In this case, it may be necessary to use ndown to run the domains separately.

|br|

:underline:`Steps to use Ndown for a one-way nested simulation`
        
           .. note::
              Note: using ndown requires the code to be compiled for nesting.

        #. Obtain output from a coarse grid WRF simulation. 
                * This is no different than any single-domain WRF run, as described above. 
                * Frequent output (e.g. hourly) from the coarse grid run is recommended to provide better boundary specifications.

        #. Run geogrid.exe and metgrid.exe for two domains.
                * as if this is for a 2-way nested run

        #. Run real.exe for 2 domains. 
                * The purpose of this step is to ingest higher resolution terrestrial fields and corresponding land-water masked soil fields.
                * Copy or link the met_em* files to the directory in which you are running real.exe. For e.g.,

                .. code-block::

                        > ln -sf <path-to-WPS-directory>/met_em* .

                * Edit namelist.input. Set *max_dom=2*, making sure columns 1 and 2 are set-up for a 2 domain run (edit the correct start time and grid dimensions).
                * Run real.exe. This produces files: *wrfinput_d01*, *wrfinput_d02*, and *wrfbdy_d01*

        #. Run ndown.exe to create the final fine-grid initial and boundary condition files.
                * Rename *wrfinput_d02* to *wrfndi_d02*

                .. code-block::

                        > mv wrfinput_d02 wrfndi_d02

               * Modify and check the following namelist.input parameters. 

                       * *io_form_auxinput2=2* must be added to the *&time_control* section of namelist.input to run ndown.exe successfully.
                       * *interval_seconds* should reflect the history output interval from the coarse domain model run.
                       * Make sure *max_dom=2*.
                       * Do not change physics options until after running the ndown program.
                       * Do not remove any fields from the Registry.
                       * *(Optional)* To refine the vertical resolution when running ndown, set *vert_refine_fact* (see details in `Namelist Variables`_ section of this guide). An alternativeis to use the utility *v_interp* to refine vertical resolution (see the section on `WRF Post-processing, Utilities, & Tools`_ for details).

               * Run ndown.exe, which uses input from the coarse grid *wrfout\** file(s), and the *wrfndi_d02* file. This produces files: *wrfinput_d02 and wrfbdy_d02*

               .. code-block::

                       > ./ndown.exe >& ndown.out
                        or 
                       > mpiexec -np 4 ./ndown.exe 

        #. Run the fine-grid WRF simulation.
                * Rename *wrfinput_d02* to *wrfinput_d01* and *wrfbdy_d02* to *wrfbdy_d01*

                .. code-block::

                        > mv wrfinput_d02 wrfinput_d01
                        > mv wrfbdy_d02 wrfbdy_d01

                * Rename (or move) the original *wrfout_d01\** files to something else (or another directory) so as to not overwrite them.
                * Modify and check the following namelist.input parameters. 

                        * Move the fine-grid domain settings for *e_we*, *e_sn*, *dx*, and *dy* from column 2 to column 1 so that this run is for the fine-grid domain only. 
                        * Make sure *time_step* is set to comply with the fine-grid domain (typically 6*DX).
                        * Set *max_dom=1*
                        * *(Optional)* At this stage, the WRF model's physics options may be modified from those used for the initial single domain run, with the exception of the land surface scheme (*sf_surface_physics*) which has different numbers of soil depths depending on the scheme.
                        * *(Optional)* To allow the initial and lateral boundaries to use the moist and scalar arrays, set *have_bcs_moist=.true.* and *have_bcs_scalar=.true.* (*This option should only be used during the WRF model run, after the ndown process, and microphysics options must remain the same between forecasts*). The advantage is the previous WRF model provides realistic lateral boundary tendencies for all microphysical variables, instead of a simple zero inflow or zero gradient outflow.

                * Run WRF for this grid.

        The output from this run is in the form *wrfout_d01*, but will actually be output for the fine-resolution domain. It may help to rename these to avoid future confusion.

| 

:underline:`Running ndown.exe for Three or More Domains`

        The ndown program can also be used for more than one nest, but the procedure is a bit cumbersome. Because of the way the code it written, it expects specific file names (specifically for d01 and d02), and therefore it is important to follow these steps precisely:

            .. note:: 
               This example is for nesting down to a 3rd domain (3 domains total), and assumes the wrfout_d01\* files are already created. 

        #. Run the geogrid.exe and metgrid.exe programs for 3 domains.

        #. Run real.exe for 3 domains.
               * Link or copy the met_em* files into the directory in which you are running real.exe.
               * Edit namelist.input. Set *max_dom=3*, making sure columns 1, 2 and 3 are set-up for a 3-domain run (edit the correct start time and grid dimensions).
               * Run real.exe. This produces files: *wrfinput_d01, wrfinput_d02, wrfinput_d03*, and *wrfbdy_d01*.

        #. Create the domain 02 grid initial and boundary condition files, by running ndown.exe (see the details in section above).

        #. Run the domain 2 WRF simulation (see details in the section above). There should now be wrfout_d01* files, which will correspond to domain 02.

        #. Make the domain 03 grid initial and boundary condition files, by running ndown.exe.
               * Rename *wrfinput_d03* to *wrfndi_d02* (this is the name the program expects)
               * Modify and check the following namelist.input parameters.
                       * Make sure *io_form_auxinput2 = 2* is set in the &time_control section of the namelist.
                       * Ensure *interval_seconds* is set to reflect the history output interval from the coarse domain model run.
                       * Set *max_dom=2*.
                       * Move the value of *i_parent_start* and *j_parent_start* from column 3 to column 2. Keep the value set to *=1* for column 1. 
                       * Do not change physics options until after running the ndown program.
               * Run ndown.exe, which uses input from the (new) coarse grid wrfout file(s), and the wrfndi_d02 file. This produces a *wrfinput_d02* and *wrfbdy_d02* file (both which will actually correspond to domain 03).

        #. Make the fine-grid (d03) WRF run.
               * Rename "*wrfinput_d02* to *wrfinput_d01*.
               * Rename *wrfbdy_d02* to *wrfbdy_d01*.
               * Rename (or move) the wrfout_d01* files to something else (or another directory) so as to not overwrite them (recall that these files correspond to d02).
               * Modify and check the following namelist.input parameters.
                      * Move the fine-grid domain settings for *e_we*, *e_sn*, *dx*, and *dy* from the original column 3 (domain 03) to column 1 (domain 01) so that this run is for the fine-grid domain only. 
                      * Make sure *time_step* is set to comply with the fine-grid domain (typically 6*DX).
                      * Set *max_dom=1*.


        After running wrf.exe, you will have new wrfout_d01* files. These correspond to domain 03. If you need to add any more nests, follow the same format, keeping the naming convention the same (always using *d02*).

        The following figure summarizes data flow for a one-way nested run using the program ndown.

        |

        .. image:: images/ndown_image1.png
           :width: 650px

        |

        |

        |br|


        .. image:: images/ndown_image2.png
           :width: 650px

|

Automatic Moving Nest (Vortex-following)
++++++++++++++++++++++++++++++++++++++++

The automatic moving nest (or vortex-following) option tracks the center of low pressure in a tropical cyclone, and allows the nested domain to move inside the parent as the cyclone moves. This can be useful because tropical cyclones typically move over a large area over a short time period. This option eliminates the need to use a large high-resolution nest (which can be computationally expensive), and tracks the cyclone as it moves inside its parent (coarse) domain. 

To use the automatic moving nested option, select the *vortex-following* nesting option (option 3) when configuring, in addition to the distributed-memory parallelization option (dmpar) to make use of multiple processors. *Note: This compile will not support the specified moving nested run or static nested run.* No nest input is needed, but note that the automatic moving nest works best for a well-developed vortex. To use values other than the default, add and edit the following namelist variables in the *&domains* section:

.. csv-table::
   :widths: 20, 70
   :width: 100%
   :escape: \

   **vortex_interval**, how often the vortex position is calculated in minutes (default is 15 minutes)
   **max_vortex_speed**, used with vortex_interval to compute the search radius for the new vortex center position (default is 40 m/sec)
   **corral_dist**, the closest distance in the number of coarse grid cells between the moving nest boundary and the mother domain boundary (default is 8). This parameter can be used to center the telescoped nests so that all nests are moved together with the storm.
   **track_level**, the pressure level (in Pa) where the vortex is tracked
   **time_to_move**, the time (in minutes) until the nest is moved. This option may help when the storm is still too weak to be tracked by the algorithm.

|   

When the automatic moving nest is employed, the model writes the vortex center location, with minimum mean sea-level pressure and maximum 10-m winds to the standard-out file (e.g. *rsl.out.0000*). Type the following command to produce a list of storm information at 15-minute intervals:

.. code-block::

        > grep ATCF rsl.out.0000

        ATCF    2007-08-20_12:00:00            20.37   -81.80     929.7 133.9 |br|
        ATCF    2007-08-20_12:15:00            20.29   -81.76     929.3 133.2

The initial location of the nest is specified through i_parent_start and j_parent_start in the namelist.input file.

|

:underline:`Using high-resolution terrain and landuse with a moving nest` |br|
There is an additional capability to incorporate high-resolution terrain and landuse input in a moving nest run (see `Chen et al., 2007`_). To activate this option,

        #. Before configuring and compiling the code, set

                .. code-block::

                        For csh 
                            > setenv TERRAIN_AND_LANDUSE 1

                        For bash
                            > export TERRAIN_AND_LANDUSE=1

        #. By default, the WPS program uses MODIS landuse data, but the above-mentioned high-resolution data set is from USGS. Therefore, to use this capability, the landuse data should be prepared using USGS. Before running geogrid.exe, in the *&domains* section of namelist.wps, set 

                .. code-block::

                        > geog_data_res = 'usgs_30s+default'

        #. And then set the following in the *&time_control* section of namelist.input:

                .. code-block::

                        > input_from_hires       = .true., .true.,
                        > rsmas_data_path        = 'terrain_and_landuse_data_directory'

         .. note::
            This option will overwrite the "input_from_file" option for nest domains.

|

Specified Moving Nest
+++++++++++++++++++++

The specified moving nest option allows you to dictate exactly where the nest moves; however, it can be quite intricate to set up. 

        * The code must be compiled with the *preset moves* nesting option (option 2), and configured for distributed-memory parallelization (dmpar) to make use of multiple processors. *Note: code compiled with the "preset moves" option will not support static nested runs or the vortex-following option.* 
        * Only coarse grid input files are required because nest initialization is defined from the coarse grid data. 
        * In addition to standard nesting namelist options, the following must be added to the *&domains* section of namelis.input

|br|

.. csv-table::
   :widths: 20, 70
   :width: 100%
   :escape: \

   **num_moves**, the total number of moves during the model run. A move of any domain counts against this total. The maximum is currently set to 50\, but can be changed by modifying *MAX_MOVES* in *frame/module_driver_constants.F* (and then recompiling the code to reflect the change\, but neither a ``clean -a`` or reconfiguration is necessary).
   **move_id**, a list of nest IDs (one per move) indicating which domain will move for a given move
   **move_interval**, the number of minutes from the beginning of the run until a move will occur. The nest will move on the next time step after the specified interval has passed.
   **move_cd_x** |br| **move_cd_y**, distance in the number of grid points and direction of the nest move (positive numbers indicate moving toward east and north\, while negative numbers indicate moving toward west and south)

      |

|

|

Run-time Capabilities
---------------------
There are numerous special options available for running WRF. For a full list of options, see the `namelist.input file options`_. Scroll down, or click of the topics below to learn more about the runtime options.

    * :ref:`SST Update`
    * :ref:`Adaptive Time-stepping`
    * :ref:`Stochastic Parameterization Schemes`
    * :ref:`Analysis/Grid Nudging` (Upper-air and/or Surface)
    * :ref:`Observational Nudging`
    * :ref:`Digital Filter Initialization`
    * :ref:`Bucket Options`
    * :ref:`Global Simulations`
    * :ref:`IO Quilting`

|

.. _SST Update:

SST Update
++++++++++

Most physics do not predict sea-surface temperature, vegetation fraction, albedo or sea ice. Most first-guess input data include an SST and sea-ice field, which is used to initialize the model and should be sufficient for short simulations since ocean temperatures do not change quickly. However, for simulations longer than about 5 days, the "sst_update" option is available to read-in additional time-varying data and update these fields. To use this option, you must obtain time-varying SST and sea ice fields. Twelve monthly values of vegetation fraction and albedo are available from the geogrid program. After the fields are processed via WPS_, set the following options in the namelist record &time_control before running real.exe and wrf.exe:

        .. note:: 
           "(max_dom)" indicates a value should be set for each domain you wish to nudge.

|

            * **io_form_auxinput4 = 2**
            * **auxinput4_inname = "wrflowinp_d<domain>"** (created by real.exe)
            * **auxinput4_interval = 360, 360, 360**

|br|

and in &physics

            **sst_update = 1**

        .. note::
           The sst_update option cannot be used with *sf_ocean_physics* or vortex-following options.

|

|

.. _Adaptive Time-stepping:

Adaptive Time-stepping
++++++++++++++++++++++

Adaptive time stepping is a method of maximizing the time step the model can use while maintaining numerical stablity. Model time step is adjusted based on the domain-wide horizontal and vertical stability criterion (called the Courant-Friedrichs-Lewy (CFL) condition). The following set of values typically work well.

        .. note::
           "(max_dom)" indicates a value should be set for each domain you wish to nudge.

|br|

        * **use_adaptive_time_step = .true.**
        * **step_to_output_time = .true.** (Note that nest domain output may still not write at the correct time. If this happens, try using **adjust_output_times = .true.** to correct this)
        * **target_cfl = 1.2, 1.2, 1.2** (max_dom)
        * **max_step_increase_pct = 5, 51, 51** (a large percentage value for the nest allows the nested time step more freedom to adjust - (max_Dom)) 
        * **starting_time_step = -1, -1, -1** (the default value "-1" means 4*DX at start time - (max_dom))
        * **max_time_step = -1, -1, -1** (the default value "-1" means 8*DX at start time - (max_dom)) 
        * **min_time_step = -1, -1, -1** (the default value "-1" means 3*DX at start time - (max_dom)) 
        * **adaptation_domain=** (an integer value indicating which domain is driving the adaptive time step)
         
See the `namelist.input file options`_ for additional information on these options.

|

|

.. _Stochastic Parameterization Schemes: 

Stochastic Parameterization Schemes
+++++++++++++++++++++++++++++++++++

The stochastic parameterization suite comprises a number of stochastic parameterization schemes, some widely used and some developed for very specific applications. It can be used to represent model uncertainty in ensemble simulations by applying a small perturbation at every time step to each member. Each of these schemes generates its own random perturbation field, characterized by spatial and temporal correlations and an overall perturbation amplitude, defined in the namelist record "&stoch."

Random perturbations are generated on the parent domain at every time step and, by default, interpolated to the nested domain(s). The namelist settings determine on which domains these perturbations are applied. For e.g., by setting "sppt=0,1,1," the perturbations are applied on the nested domains only.

Since the scheme uses Fast Fourier Transforms (FFTs) provided in the library FFTPACK, the recommended number of gridpoints in each direction is a product of small primes. Using a large prime in at least one direction may substantially increase computational cost.

|

         .. note::
            * All of the following options are set in an added "&stoch" section of namelist.input.
            * "max_dom" indicates a value is needed for each domain.

|

:underline:`Random perturbation field` |br|
This option generates a 3-D Gaussian random perturbation field for user-implemented applications. The perturbation field is saved as "rand_pert" in the history files. Activate this option by setting

        **rand_perturb=1** (max_dom)

|

:underline:`Stochastically perturbed physics tendencies (SPPT)` |br|
A random pattern is used to perturb accumulated physics tendencies (except those from micro-physics) of potential temperature, wind, and humidity. For details on the WRF implementation see `Berner et al., 2015`_. The perturbation field is saved as "rstoch" in the history files. Activate this option by setting

        **sppt=1** (max_dom)

|

:underline:`Stochastic kinetic-energy backscatter scheme (SKEBS)` |br|
A random pattern is used to perturb the potential temperature and rotational wind component. The perturbation fields are saved as "ru_tendf_stoch," "rv_tendf_stoch," and "rt_tendf_stoch" in the history files for u,v and θ, respectively. Wind perturbations are proportional to the square root of the
kinetic-energy backscatter rate, and temperature perturbations are proportional to the potential energy backscatter rate. For details on the WRF implementation see `Berner et al., 2011`_ and `WRF Implementation Details and Version history of a Stochastic Kinetic-Energy Backscatter Scheme (SKEBS)`_. Default parameters are for synoptic-scale perturbations in the mid-latitudes. Tuning strategies are discussed in `Romine et al. 2014`_ and `Ha et al. 2015`_. Activate this option by setting

        **skebs=1** (max_dom)

|

:underline:`Stochastically perturbed parameter scheme (SPP)` |br|
A random pattern is used to perturb parameters in selected physics packages, namely the GF convection scheme, the MYNN boundary layer scheme, and the RUC LSM. Parameter perturbations to a single physics package can be achieved by setting "spp_conv=1," "spp_pbl=1," or "spp_lsm=1." For implementation details see `Jankov et al.`_. The perturbation fields are saved as "pattern_spp_conv," "pattern_spp_pbl," and "pattern_spp_lsm" in the history files. Activate this option by setting

        **spp=1** (max_dom)

|

:underline:`Stochastic Perturbations to the boundary conditions (perturb_bdy)` |br|

        * **perturb_bdy=1** - The stochastic random field is used to perturb the boundary tendencies for wind and potential temperature. This option runs independently of SKEBS and may be run with or without the SKEB scheme, which operates solely on the interior grid. *Note that this option requires the generation of a domain-size random array, thus computation time may increase.*
        * **perturb_bdy=2** - A user-provided pattern is used to perturb the boundary tendencies. Arrays are initialized and called: "field_u_tend_perturb," "field_v_tend_perturb," and "field_t_tend_perturb." These arrays should be filled with the desired pattern in "spec_bdytend_perturb" in share/module_bc.F or "spec_bdy_dry_perturb" in dyn_em/module_bc_em.F. Once these files are modified, WRF must be recompiled (but neither a ?~@~Xclean -a?~@~Y nor a reconfigure are necessary).

|

:underline:`Stochastic perturbations to the boundary tendencies in WRF-CHEM (perturb_chem_bdy)` |br|
A random pattern is created and used to perturb the chemistry boundary tendencies in WRF-Chem. For this application, WRF-Chem should be compiled at the time of the WRF compilation. Activate this option by setting

        **rand_perturb=1** (max_dom) - see above for details about this option

The "perturb_chem_bdy" option runs independently of "rand_perturb" and as such may be run with or without the "rand_perturb" scheme, which operates solely on the interior grid. However, "perturb_bdy_chem=1" requires the generation of a domain-sized random array to apply perturbations in the lateral boundary zone, thus computation time may increase. When running WRF-Chem with "have_bcs_chem=.true." in &chem, chemical LBCs read from wrfbdy_d01 are perturbed with the random pattern created by "rand_perturb=1."

|

:underline:`WRF-Solar stochastic ensemble prediction system (WRF-Solar EPS)` |br|
WRF-Solar includes a stochastic ensemble prediction system (WRF-Solar EPS) tailored for solar energy applications (`Yang et al., 2021`_; `Kim et al., 2022`_). The stochastic perturbations can be introduced into variables of six parameterizations, controlling cloud and radiation processes. See details of the model on the `WRF-Solar EPS website`_. See `namelist.input file options`_ in the &stoch section.

|

|

.. _Analysis/Grid Nudging:

Analysis Nudging (Upper-air and/or Surface)
+++++++++++++++++++++++++++++++++++++++++++
      
Analysis nudging is a method of nudging the model toward data analysis, and is suitable for coarse resolution. The model is run with extra nudging terms for horizontal winds, temperature, and water vapor. These terms nudge point-by-point to a 3d space- and time-interpolated analysis field.

        |

:underline:`Instructions for Use`

        #. Prepare input data to WRF as usual using WPS. If nudging is desired in the nest domains, make sure all time periods for all domains are processed in WPS. If using surface-analysis nudging, the OBSGRID_ tool must be run after metgrid. OBSGRID will output a file called *wrfsfdda_d01* that is required for the WRF model to read when using this option.

        #. Set the following options in *&fdda* in namelist.input before running real.exe. *(max_dom)* indicates a value should be set for each domain you wish to nudge.
       
                * **grid_fdda=1**, turns on analysis nudging (max_dom)
                * **gfdda_inname='wrffdda_d<domain>'**, This is the defined name of the file the real program will write out.
                * **gfdda_interval_m=**, time interval of input data in minutes (max_dom)
                * **gfdda_end_h=**, end time of grid-nudging in hours (max_dom)
        
        |br|

            These are some other common options that can be set (for additional information and options, see *examples.namelist* in the *test/em_real* directory of the WRF code)    
            
                * **io_form_gfdda=2** : analysis data I/O format (2=netcdf)
                * **fgdt=** : calculation frequency (mins) for grid-nudging (0=every time step; (max_dom))
                * **if_no_pbl_nudging_uv=** : 1=no nudging of u and v in the PBL, 0=nudging in the PBL (max_dom)
                * **if_no_pbl_nudging_t=** : 1=no nudging of temperature in the PBL, 0=nudging in the PBL (max_dom)
                * **if_no_pbl_nudging_q=** : 1=no nudging of qvapor in the PBL, 0=nudging in the PBL (max_dom)
                * **guv=0.0003** : nudging coefficient for u and v (sec-1) (max_dom)
                * **gt=0.0003** : nudging coefficient for temperature (sec-1) (max_dom)
                * **gq=0.00001** : nudging coefficient for qvapor (sec-1) (max_dom)
                * **if_ramping=** : 0=nudging ends as a step function; 1=ramping nudging down at the end of the period
                * **dtramp_min=** : time (mins) for the ramping function (if_ramping)
            
            If doing surface analysis nudging, set

                * **grid_sfdda=1** : turns on surface analysis nudging (max_dom)
                * **sgfdda_inname="wrfsfdda_d<domain>"** : This is the defined name of the input file from OBSGRID.
                * **sgfdda_interval_m=** : time interval of input data in minutes
                * **sgfdda_end_h=** : end time of surface grid-nudging in hours

            An alternative surface data nudging option is activated by setting
                  **grid_sfdda=2**

            This option nudges surface air temperature and water vapor mixing ratio, similar to that with option 1, but uses tendencies generated from the direct nudging approach to constrain surface sensible and latent heat fluxes, thus ensuring thermodynamic consistency between the atmosphere and land surface. This works with YSU PBL and Noah LSM. (Alapaty et al. JAMC, 2008) |br| |br|

        #. Run real.exe, which, in addition to the wrfinput_d0* and wrfbdy_d01 files, will create a file named *wrffdda_d0\**.

        :underline:`Note` |br| 
        For additional guidance, see the `Steps to Run Analysis Nudging`_ document, along with the *test/em_real/examples.namelist* file in the WRF code.

        | 

:underline:`Spectral Nudging` |br|
Spectral Nudging is another upper-air nudging option that selectively nudges only the coarser scales, and is otherwise set up similarly to grid-nudging, but additionally nudges geopotential height. The wave numbers defined here are the number of waves contained in the domain, and the number is the maximum wave that is nudged.

            **grid_fdda** = 2; turns on spectral nudging option (max_dom) |br|
            **xwavenum** = 3 |br|
            **ywavenum** = 3
        
        | 
        
            .. note:: 
               The DFI option can not be used with nudging options.

        |

|

.. _Observational Nudging:

Observational Nudging
+++++++++++++++++++++

Observational nudging is a method of nudging the model toward observations. As in analysis nudging, the model is run with extra nudging terms for horizontal winds, temperature, and water vapor; however, in obs-nudging, points near observations are nudged based on model error at the observation site. This option is suitable for fine-scale or asynoptic observations. For additional information on the below content, see the `Observation Nudging Users Guide`_, `Experimental Nudging Options`_, and *README.obs_fdda* in *WRF/test/em_real/*.

        |

:underline:`Instructions for Use`

        In addition to the standard WPS preparation of input data, station observation files are required. Observation file names expected by WRF are *OBS_DOMAIN101* for domain 1, and *OBS_DOMAIN201* for domain 2, etc. These files must be created using the OBSGRID_ program. |br| |br| 

        Observation nudging is activated with the following namelist settings in *&fdda* (note that *(max_dom)* indicates the setting should be applied to all domains you wish to nudge.

                * **obs_nudge_opt=1** - turns on observational nudging (max_dom)
                * **fdda_start=** - obs nudging start time in minutes (max_dom)
                * **fdda_end=** - obs nudging end time in minutes (max_dom)

            and in *&time_control*

                * **auxinput11_interval_s=** - interval in seconds for observation data. It should be set to an interval small enough that all observations are included. 

        |

        Some additional and commonly-used namelist settings (in the &fdda section) are

                * **max_obs=150000** - The max number of observations used on a domain during any given time window
                * **obs_nudge_wind=** - set to 1 to nudge wind, 0=off (max_dom)
                * **obs_coef_wind=6.E-4** - nudging coefficient for wind (s-1) (max_dom)
                * **obs_nudge_temp=** - set to 1 to nudge temperature, 0=off (max_dom)
                * **obs_coef_temp=6.E-4** - nudging coefficient for temperature (s-1) (max_dom)
                * **obs_nudge_mois=** - set to 1 to nudge water vapor mixing ratio, 0=off (max_dom)
                * **obs_coef_mois=6.E-4** - nudging coefficient for water vapor mixing ratio (s-1) (max_dom)
                * **obs_rinxy=240.** - horizontal radius of influence in km (max_dom)
                * **obs_rinsig=0.1** - vertical radius of influence in eta 
                * **obs_twindo=0.6666667** - half-period time window over which an observation will be used for nudging, in hours (max_dom)
                * **obs_npfi=10** - frequency in coarse grid timesteps for diagnostic prints
                * **obs_ionf=2** - frequency in coarse grid timesteps for obs input and error calculation (max_dom)
                * **obs_idynin=** - set to 1 to turn on the option to use a ramp-down function for dynamic initialization, to gradually turn off the FDDA before the pure forecast
                * **obs_dtramp=40.** - time period in minutes over which the nudging is ramped down from one to zero, if setting obs_idynin=1
                * **obs_prt_freq=10** - frequency in obs index for diagnostic printout (max_dom)
                * **obs_prt_max=1000** - maximum allowed obs entries in diagnostic printout
                * **obs_ipf_errob=.true.** - true=print obs error diagnostics; false=off
                * **obs_ipf_nudob=.true.** - true=print obs nudge diagnostics; false=off
                * **obs_ipf_in4dob=.true.** - true=print obs input diagnostics; false=off |br| |br|

        Look for examples for additional nudging namelist parameters in the file ‘examples.namelists’ in the test/em_real/ directory.


            .. note::
               The DFI option can not be used with nudging options.

|

|

.. _Digital Filter Initialization:

Digital Filter Initialization
+++++++++++++++++++++++++++++

Digital filter initialization (DFI) is a method to remove initial model imbalance as, for example, measured by the surface pressure tendency. This may be important if you are interested in the 0-6 hour simulation/forecast. It runs a digital filter during a short model integration, backward and forward, and then starts the forecast. In WRF implementation, this is all done in a single job. DFI can be used for multiple domains with concurrent nesting, with feedback disabled.

|

:underline:`Instructions for Use`

        #. There is no special requirement for data preparation or any WPS programs. |br| |br|

        #. Start with the *example.namelist* file in the test/em_real/ directory, and look for the **&dfi_control** section. Cut and paste it into your namelist.input file. Edit the section to match your case configuration (e.g. dates). For a typical application, the following options are used:

                * **dfi_opt=3** - which DFI option to use (0=no DFI; 1=digital filter launch; 2=diabatic DFI; 3=twice DFI - option 3 is recommended; Note:  if doing a restart, this must be changed to 0)
                * **dfi_nfilter=7** - which digital filter type to use (0=uniform; 1=Lanczos; 2=Hamming; 3=Blackman; 4=Kaiser; 5=Potter; 6=Dolph window; 7=Dolph; 8=recursive high-order - option 7 is recommended)
                * **dfi_cutoff_seconds=3600** - cutoff period (in seconds) for the filter (should not be longer than the filter window)
                * **dfi_write_filtered_input=.true.** - option to produce a filtered wrfinput file ("wrfinput_initialized_d01") when running wrf. |br| |br|


            | The following time specifications are typically set so that integration goes backfor for 0.5 to 1 hour, and integration forward is for half that time.

                * **dfi_bckstop_year, dfi_bckstop_month, dfi_bckstop_day, dfi_bckstop_hour, dfi_bckstop_minute, dfi_bckstop_second**
                * **dfi_fwdstop_year, dfi_fwdstop_month, dfi_fwdstop_day, dfi_fwdstop_hour, dfi_fwdstop_minute, dfi_fwdstop_second**

        |

            * To use the constant boundary condition option, *set constant_bc=.true.* in the *&bdy_control* namelist record.
            * If planning to use a different time step for DFI, it can be set with the *time_step_dfi* option.


             .. note::
                * The DFI option can not be used with nudging options.
                * The DFI option can not be used with the multi_bdy_files=.true. option.

|

|

.. _Bucket Options:

Bucket Options
++++++++++++++

When running long simulations and wishing to obtain either rainfall accumulation (e.g., RAINC, RAINNC) and/or radiation budget accumulation (e.g., ACSWUPT, ACLWDNBC) terms, it is advised to use the bucket options "bucket_mm" and "bucket_J." With 32-bit accuracy, adding small numbers to very large numbers causes a loss of accuracy as the accumulation term increases. For simulations of days to weeks, the accumulations are usually okay, but for months to years, this has the effect of truncating the additions (particularly small ones may be zeroed-out). When these options are activated, part of the term is stored in an integer that increments by 1 each time the bucket value is reached.

        |

        **Water Accumulation** |br|
        Set "bucket_mm" in the &physics section of the namelist. This is the bucket reset value for water accumulations (in mm). This will produce two terms: RAINNC and I_RAINNC, where RAINNC now only contains the remainder. The total is retrieved from the output with |br|

                total = RAINNC+bucket_mm*I_RAINNC.

        A reasonable bucket value may be based on a monthly accumulation (e.g., 100 mm). Total precipitation equals RAINC + RAINNC, where
                * Total RAINNC = RAINNC+bucket_mm*I_RAINNC
                * Total RAINC = RAINC+bucket_mm*I_RAINC

        |

        **Radiation Accumulation** |br|
        Set "bucket_J" in the &physics section of the namelist. This is the bucket reset value for energy accumulations (in Joules). The radiation accumulation terms (e.g., ACSWUPT) are in Joules/m^2, so that the mean value over a simulation period is the difference divided by the time between, giving W/m^2. The typical value, based on a monthly accumulation, is 1.e9 J. Here the total is given by (ACSWUPT example - other radiative terms would follow the same equation concept) |br|

                total = ACSWUPT+bucket_J*I_ACSWUPT

|

|

.. _Global Simulations:

Global Simulations
++++++++++++++++++

WRF supports a global domain capability, but first note that since **this is not a commonly-used configuration in the model and it should be used with caution**. Not all physics and diffusion options have been tested with it, and some options may not work well with polar filters. Positive-definite and monotonic advection options do not work with polar filters in a global run because polar filters can generate negative values of scalars (which implies that WRF-Chem cannot be run with positive-definite and monotonic options in a global WRF setup). 

        .. note::
           For NWP global simulations, users are encouraged to explore the use of the NCAR `MPAS model`_.

|

:underline:`Instructions for Use`

        #. Run WPS, starting with the namelist template "namelist.wps.global."
                * Set **map_proj='lat-lon'**, and grid dimensions **e_we** and **e_sn**.
                * There is no need to set dx and dy. The geogrid program will calculate grid distances, whose values can be found in the global attribute section of the geo_em.d01.nc file.
                * Type ``ncdump -h geo_em.d01.nc`` to see the grid distances, which are needed for WRF's namelist.input. Grid distances in the x and y directions may be different, but it is best that they are set similarly or the same. WRF and WPS assume the earth is a sphere, with a radius of 6370 km. There are no restrictions on what to use for grid dimensions, but for effective use of the polar filter in WRF, the east-west dimension should be set to 2P*3Q*5R+1 (where P, Q, and R are any integers, including 0).
                * Run the remaining WPS programs as usual, but only for one time period. Because the domain covers the entire globe, lateral boundary conditions are not needed. |br| |br|
         
        #. Run real.exe for only a single time period. The lateral boundary file wrfbdy_d01 is not needed. |br| |br|
         
        #. Copy "namelist.input.global" to "namelist.input", and edit it for your configuration. |br| |br|

        #. Run wrf.exe.

|

|

.. _IO Quilting:

I/O Quilting
++++++++++++

The I/O Quilting option allows reserving a few processors to manage output only, which can be useful and sometimes performance-friendly if the domain size is very large, and/or the time taken to write each output is significant when compared to the time taken to integrate the model between output times. 

|br|

        .. note::
           This option should be used with care, and only used if the user is familiar with computing processes and knows what they are doing.

|br|

To use quilting, the following namelist parameters should be set in the &namelist_quilt record in namelist.input. 

        * **nio_tasks_per_group** : Number of processors to use per IO group for IO quilting (1 or 2 is typically sufficient)
        * **nio_groups** : How many IO groups for IO (default is 1)

|

        .. note::
           This option is only available for use with wrf.exe. It does not work for real or ndown.


|

|

|

|


.. _`namelist options`: namelist_variables.html
.. _`Chen et al., 2007`: http://dx.doi.org/10.1175/BAMS-88-3-311
.. _OBSGRID: ../post_processing_utilities_tools/obsgrid/obsgrid.rst 
.. _`Steps to Run Analysis Nudging`: https://www2.mmm.ucar.edu/wrf/users/docs/How_to_run_grid_fdda.html
.. _OBSGRID: ../post_processing_utilities_tools/obsgrid/obsgrid.rst 
.. _`Observation Nudging Users Guide`: https://www2.mmm.ucar.edu/wrf/users/docs/ObsNudgingGuide.pdf
.. _`Experimental Nudging Options`: https://www2.mmm.ucar.edu/wrf/users/docs/How_to_run_obs_fdda.html
.. _`MPAS model`: https://mpas-dev.github.io/
.. _WPS: ../wps/wps.html
.. _`Berner et al., 2015`: http://journals.ametsoc.org/doi/abs/10.1175/MWR-D-14-00091.1
.. _`Berner et al., 2011`: http://journals.ametsoc.org/doi/abs/10.1175/2010MWR3595.1
.. _`WRF Implementation Details and Version history of a Stochastic Kinetic-Energy Backscatter Scheme (SKEBS)`: http://www2.mmm.ucar.edu/wrf/users/docs/skebs_in_wrf.pdf
.. _`namelist.input file options`: ./namelist_variables.html
.. _`Romine et al. 2014`: http://journals.ametsoc.org/doi/citedby/10.1175/MWR-D-14-00100.1 
.. _`Ha et al. 2015`: http://journals.ametsoc.org/doi/10.1175/MWR-D-14-00395.1
.. _`Jankov et al.`: http://journals.ametsoc.org/doi/abs/10.1175/MWR-D-16-0160.1
.. _`WRF-Solar EPS website`: https://ral.ucar.edu/solutions/products/wrf-solar-eps
.. _`Namelist Variables`: ./namelist_variables.html 
.. _`WRF Post-processing, Utilities, & Tools`: ./post_processing_utilities_tools.html
.. _`Yang et al., 2021`: https://ieeexplore.ieee.org/abstract/document/9580552
.. _`Kim et al., 2022`: https://doi.org/10.1016/j.solener.2021.03.044
