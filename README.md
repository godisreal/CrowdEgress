# CrowdEgress

The source code was intially written in Python 2.7, and I am modifying the code slightly for python3. Pygame and Numpy are required to run the code. A simple user interface is under development in version 2.0 by using Tkinter.  

How-To(Version 2.0): python ui.py --> user interface (GUI) --> select input files --> visulize geometry settings --> start simulation

(1) When tkinter window (GUI) is activated, please select the input files for simulation.  Choose .csv file for evac input data.  Users can optionally use .fds file to create the compartment geometry, and the pedestrian features must be described in .csv file.  If .fds file is omitted, the compartment geometry should be described in .csv file.  Please take a look at the user guide and examples for details.  

(2) When pygame screen is activated, press certain keys to adjust the display features:  
Use pageup/pagedown to zoom in/zoom out the entities.  
Use space key to pause the simulation.  
Use arrows to move the entities vertically or horizonally in screen.  

(3) There are currently two examples in the repo.  Please execute run.bat in the subfolders to run the example.  The examples are run by using non-gui method.  Users can also learn how to write the .csv files from the examples.

The program mainly consists of four components: User Interface, Simulation Core, Data Tool, Visualization Tool.  

**User Interface**: The user interface is written in tkinter in ui.py.  A user run ui.py to enable a graphic user interface (GUI) where one selects the input files, initialize compartment geometry, and configure or start a simulation.  Currently there is a simple version of GUI and it needs to be improved in several aspects.  If you find any problems when using the user interface, please send me a message or direct start an issue here.  

**Simulation Core**: The multi-agent simulation is implemented in simulation.py.  The component is packed in a class called simulation class, and it computes interaction of four types of entities: agents, walls, doors and exits.  This agent-based model is an extension of the traditional social force model by Helbing, Farkas, Vicsek and Molnár.  The model aims at investigating protypes of pedestrian behavior in crowd evacuation.  

**Data Tool**: This component is included in data.py, which reads in data from input files and write data to output files.  The agent and exit data must be included in a .csv file.  The compartment geometry (i.e., walls and doors) is either read from the .csv file or .fds file (FDS input file).  Please refer to examples for details in specification of agents, walls, doors and exits.  

**Visualization Tool**:  The visulization component is packed in draw_func.py and pygame (SDL for Python) is used to visualize the simulation result.  We may develop another offline visualization tool such that users can first run the simulation and get the output data, and then visualize the output data.  


### Collaborators are needed and your ideas are much valued!  

If you are a student or researcher who want to use this python package to test your own model or algorithm, please feel free to ask your question either by email or issue trackers, and I am glad to guide you to use this package!  

So if you are interested in this project and would like to contribute your ideas, please feel free to start an issue to propose your ideas!  Collaboration is welcome and comments are appreciated!  There are several things to do to improve the source code and document.  Please refer to the issue "To-do list" for details.  

Open discussion is much encouraged about the model and algorithm!  
Source code keeps updating but the model does not!  
