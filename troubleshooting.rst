.. role:: underline
    :class: underline

Troubleshooting
===============

When something goes wrong and the simulation stops, the first thing that should be done is to view the error log(s). If WRF is compiled with the dmpar (distributed memory) option, there will be rsl.out and rsl.error files available for each processor used. Otherwise, when the model is run, the error and output should be sent to a file, using the "&>" syntax. For e.g., 

        ``./wrf.exe >& output.log``

If there are several rsl\* files, the rsl.error.0000 file is most likely to contain the error, but this is not always the case. If there is no error at the end of that file, determine whether any other rsl\* files may be larger in size. This can sometimes be an indication of more information printed in that particular file. To see the file size, issue

        ``ls -ls rsl.*``

|

Model Stops - No Error or Segmentation Fault
--------------------------------------------

If the model aborts quickly, likely either there is not enough computer memory availableh to run the specific configuration, or there are problems with the input data. 

|

Inadequate Memory
+++++++++++++++++

:underline:`For small systems (e.g., desktop workstation or laptop)` |br|
Prior to configuring and compiling, try setting one of the following to determine if more memory and/or stack size can be obtained.

        ``unlimt`` |br|
        or
        ``ulimit -s unlimited``

|

        .. note::
           For OpenMP (smpar-compiled code), the stack size needs to be set large, but not unlimited. Unlimited stack size may crash the system.

|

:underline:`For HPC systems` |br|
Typically adding additional processors will resolve these issues. Take a look at `this FAQ_` on the "WRF & MPAS-A Forum" regarding choosing the appropriate number of processors, based on the size of the domain.

|

Problem with Input Data
+++++++++++++++++++++++

To check if the input data are the problem, use ncview or another netCDF file browser to check fields in the "met_em\*" or "wrfinput\*" files. Look at all times, variables, and levels and notice whether anything looks unrealistic or if data are missing.

|

Segmentation Fault
++++++++++++++++++

Segmentation faults can be difficult to track down. As there isn't usually a clear error message, it can take some trial and error to figure out the problem.

        * A segmentation fault is often the result of using too many or too few processors, or a bad decomposition. Take a look at `this FAQ_` on the "WRF & MPAS-A Forum" regarding choosing the appropriate number of processors, based on the size of the domain.

        * Sometimes a lack of disk space can result in this error. Check how much space is left available for the files to be written. If the domain is large or has a very high resolution, output files will be much larger (sometimes a few GB).

        * Many times a seg-fault can indicate a **CFL error**, which means the model has become numerically unstable, meaning the time step used for advancing the model is too large for a stable solution. The most common reasons for this are due to complex terrain, model layers are too thin, if using a large domain and the corners of the domain have a large map-scale factor (it should be ~1.0) that reduces the equivalent earth distance to the be much smaller than the model grid size. To check for this error, issue the command

        ``grep cfl rsl.error*``

If CFL notifications print to the screen, this is likely the reason for the model failure, and one of (or a combination of) the following steps can be taken to try to resolve the issue. 
        #. First try to reduce the timestep. The standard recommendation for time_step is 6xDX (e.g., if your DX = 30000, then you should not set time_step to anything larger than 180). However, if CFL errors continue to appear, try to reduce to something more like 4xDX or 3xDX. Sometimes this works, but not always. 
        #. Try adding **smooth_cg_topo=.true.** in the &domains section of the namelist, prior to running real if CFL errors happen along boundary zones. This option smoothes the outer rows/columns of the coarse model grid to match the low resolution topography that comes with the driving data. 
        #. If CFL errors occur near complex terrain, try to set **epssm=0.2** (up to 0.5) to see if that makes a difference. This option is used to slightly forward the centering of the vertical pressure gradient (or sound waves) in an effort to damp 3-d divergence. 
        #. Seting **w_damping=1** in &dynamics is another option.

|

Debugging
+++++++++

Sometimes, the model stops and none of the above suggestions are helpful. There can be a variety of reasons for this, and if that is the case, it may be necessary to try to debug the code to figure out exactly what is happening. There are a couple of ways to try to debug the code.

        #. For a small domain that can be run on a single processor, the "GNU" debugger can be used by issuing the following commands.

        ``./clean -a`` |br|
        ``./configure -D`` (choose a serial compilation)

        And then recompile. To run the model, issue

        ``gdb ./wrf.exe``

        When prompted, enter: ``run``

        The model should stop on the line causing the error. Typing "list" will provide additional information. Type "quit" when done.

        #. For larger domains, or to turn on bounds checking, tracebacks, etc., issue the following commands.

        ``./clean -a`` |br|
        ``./configure -D``

        And then recompile. Run the model, and when it fails, check the error or output logs, which should print the line of code that caused the model to fail.

        .. note::
           It is NOT recommend to set "debug_level" in namelist.input. This option is no longer in the default namelist because it rarely provides useful information and adds too much useless prints to the log files, making them difficult to read, and occasionally makes the files too large to write, causing an error.

|

Namelist Issues
---------------

"ERRORS while reading namelists..."
+++++++++++++++++++++++++++++++++++

This indicates errors and/or typos in the namelist.input file. Above the error message, the model tries to determine where the namelist has problems. Check and modify the line(s) mentioned. Edit the namelist.input file with caution. Many times the error is due to multiple column settings for a parameter that only requires a single entry. For example, the parameter "run_days" should be only given a single value. So if the following is listed in namelist.input
        
        ``run_days = 2, 2, 2``

a namelist error will occur. This can be fixed by simply removing the additional columns (i.e., run_days = 1), saving namelist.input and running again. If unsure, always start with an available default template.

|

"SIZE MISMATCH"
+++++++++++++++

For example, the following indicates a difference between information in the input file and the namelist.

        ``input_wrf.F:SIZE MISMATCH:namelist e_we = 70`` |br|
        ``input_wrf.F:SIZE MISMATCH:input file WEST-EAST_GRID_DIMENSION = 74``

In the above example, the input file has a west-east grid dimension of 74 grid spaces, while the value "e_we" in namelist.input is set to 70. In these cases, the information in the input file is the one that should be used, so setting "e_we=74" in the namelist would correct this issue.

|

|

Best Practices
--------------

Use the following resources for information on the best way to set-up model domains, and runtime options to improve the outcome and avoid errors.

        * `Namelist.wps: Best Practices`_ : Descriptions for common namelist.wps parameters and best practice guidance for setting up domains
        * `Namelist.input: Best Practices`_ : Descriptions for common namelist.input parameters for running real.exe and wrf.exe, along with best practice guidance
        * `Best Practice Presentation`_ given at the biannual WRF tutorials
        * `Best Practice Presentations`_ from the WRF & MPAS Annual Workshop

|

|

Frequently Asked Questions (FAQ)
--------------------------------

To see a full library of frequently asked questions, see the `FAQ section`_ of the `WRF & MPAS-A Users' Forum`_. It may also be beneficial to use the "search" utility on the forum to see other inquiries and responses related to run-time issues.

.. _`FAQ section`: https://forum.mmm.ucar.edu/forums/frequently-asked-questions.115/
.. _`WRF & MPAS-A Users' Forum`: https://forum.mmm.ucar.edu/
.. _`this FAQ`: https://forum.mmm.ucar.edu/threads/how-many-processors-should-i-use-to-run-wrf.5082/
.. _`Namelist.wps\: Best Practices`: https://www2.mmm.ucar.edu/wrf/users/namelist_best_prac_wps.html
.. _`Namelist.input\: Best Practices`: https://www2.mmm.ucar.edu/wrf/users/namelist_best_prac_wrf.html
.. _`Best Practice Presentation`: https://www2.mmm.ucar.edu/wrf/users/tutorial/presentation_pdfs/202101/chen_better_performance.pdf
.. _`Best Practice Presentations`: https://www2.mmm.ucar.edu/wrf/users/supports/best_practices_lectures_workshop.html

|

|

|

|
