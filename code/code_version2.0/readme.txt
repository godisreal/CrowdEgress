Please use code version 2.0.  Code version 1.0 is not maintained for some reason.  

There are normally two ways to start a simulation:

(1) The first method is to run command python ui.py to start GUI and select the input files.  When GUI screen is activated, please select the input files for the simulation.  Users can optionally use .fds file to create the compartment geometry, and the pedestrian features are described in .csv file.  If .fds file is omitted, the compartment geometry is described in .csv file.  If both .csv and .fds files are presented, the compartment structure will be created by using .fds file.  Please take a look at the examples for details.  If you try .fds file, please only keep one main evacuation mesh in .fds file, which means there is only one floor in simulaiton.  

(2) The second method is to use command python main.py <filename_CSV> <filename_FDS> to  start a simulation without using GUI.  Here <filename_CSV> is the .csv file name while <filename_FDS> is the fds. file name.  Clearly <filename_FDS> is optional and users can omit it if only .csv is used in simulation.  If no file name is given, the readme txt is shown in the console.  


Extract compartment data from a .fds file and save it into .csv format.   

The program was initially developed without considering .fds file.  So it is actually convenient to edit .csv by using Excel or other powerful tools.  User can alternatively extact the compartment data from .fds file and put them into .csv form.  The procedures are introduced as below.  

Start a simulation by selecting input files with or without GUI.  Then select to go to the testGeom phase.  Select output data in the menu bar and click on the speciic enenties that you want to save the data into .csv files.  