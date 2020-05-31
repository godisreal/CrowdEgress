# CrowdEgress

The source code was intially written in Python 2.7, and you need to slightly modify the code if you want to run it in python3. Pygame and Numpy are required to run the code. A simple user interface is under development in version 2.0.  

How-To(Version 2.0): python simulation.py --> user interface (GUI) --> select input files --> visulize geometry settings --> start simulation

The program mainly consists of four component: User Interface, Simulation Core, Data Tool, Visualization.  

**User Interface**: The user interface is written in tkinter in startPage.py.  Users may call function startPage() from simulation routine to set up the input files.  An alternative method is using startPage.py to enable a graphic user interface (GUI) and start a simulation there.  Currently there is a simple version of GUI and it needs to be improved in several aspects.  

**Simulation Core**: The multi-agent simulation is implemented as simulation.py.  The component is packed in a class called simulation class, and it computes interaction of four types of entities: agents, walls, doors and exits.  This agent-based model is an extension of the traditional social force model by integrating group social force and interactive opinion dynamics. . The model aims at investigating protypes of pedestrian behavior in crowd evacuation.  

**Data Tool**: This component reads in data from input files, and write data to output files.  The input data is written by users in .csv files.  Please refer to .csv file for details in specification of agents, walls, doors and exits.  

**Visualization**:  The visulization component is packed in draw_func.py and currently pygame is used to visualize the simulation result online.  We may develop another offline visualization tool such that users can first run the simulation and get the output data, and then visualize the output data.  



### Collaborators are needed and your ideas are much valued!  


If you are a student or researcher who want to use this python package to test your own model or algorithm, please feel free to ask your question either by email or issue trackers, and I am glad to guide you to use this package!  

So if you are interested in this project and would like to contribute your ideas, please feel free to start an issue to propose your ideas!  Collaboration is welcome and comments are appreciated!  There are several things to do to improve the source code and document.  Please refer to the issue "To-do list" for details.  

Open discussion is much encouraged about the model and algorithm!  
Source code keeps changing but the model does not!  
