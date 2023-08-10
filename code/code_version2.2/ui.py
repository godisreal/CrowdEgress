
import os, sys
import multiprocessing as mp
from simulation import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
    import tkinter.filedialog as tkf
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    import tkFileDialog as tkf


class GUI(object):

    def __init__(self, FN_FDS=None, FN_EVAC=None):

        #self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        #self.FN=[None, None] #, None]
        #self.FN[0]=FN_FDS
        #self.FN[1]=FN_EVAC

        if os.path.exists("log.txt") and FN_EVAC is None and FN_FDS is None:
            for line in open("log.txt", "r"):
                if re.match('FN_FDS', line):
                    temp =  line.split('=')
                    FN_FDS = temp[1].strip()
                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    FN_EVAC = temp[1].strip()
                if re.match('ZOOM', line):
                    temp =  line.split('=')
                    ZOOM = float(temp[1].strip())                    
                if re.match('xSpace', line):
                    temp =  line.split('=')
                    xSpa = float(temp[1].strip())
                if re.match('ySpace', line):
                    temp =  line.split('=')
                    ySpa = float(temp[1].strip())
                    
                    
        self.fname_FDS = FN_FDS
        self.fname_EVAC = FN_EVAC
        self.currentSimu = None
        
        self.window = Tk()
        self.window.title('crowd egress simulator')
        self.window.geometry('700x500')

        self.statusStr = ""
        self.statusText = StringVar(self.window, value=self.statusStr) # at this point, statusStr = ""
        # added "self.rootWindow" above by Hiroki Sayama 10/09/2018
        self.setStatusStr("Simulation not yet started")
        self.status = Label(self.window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)
        

        self.notebook = Notebook(self.window)      
        self.notebook.pack(side=TOP, padx=2, pady=2)
        
        # added "self.rootWindow" by Hiroki Sayama 10/09/2018
        self.frameRun = Frame(self.window)
        #self.frameSettings = Frame(self.window)
        self.frameParameters = Frame(self.window)
        self.frameGuide = Frame(self.window)


        self.notebook.add(self.frameRun,text="RunSimulation")
        #self.notebook.add(self.frameSettings,text="Settings")
        self.notebook.add(self.frameParameters,text="Parameters")
        self.notebook.add(self.frameGuide,text="Readme")
        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
        # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02
        
        #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        #from Tkinter.tkFileDialog import askopenfilename
        #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
        #def quit_botton(event):

        # --------------------------------------------
        # frameRunSimulation
        # --------------------------------------------
        self.lb_guide = Label(self.frameRun, text =  "Please select the input files of the simulation\n" + "Use a single .csv  file to create compartment geometry and agents\n" + "Please check the examples for details")
        self.lb_guide.pack()

        self.lb1 = Label(self.frameRun,text =  "The input .csv file selected: "+str(self.fname_EVAC)+"\n")
        self.lb1.pack()

        self.lb0 = Label(self.frameRun,text =  "Optional: If .fds is selected, the compartment geometry is created by .fds file. \n"+ "The FDS file selected: "+str(self.fname_FDS)+"\n")
        self.lb0.pack()

        #self.lb2 = Label(frameRun,text =  "The exit data file selected: "+str(FN[2])+"\n")
        #self.lb2.pack()


        self.buttonSelectCSV =Button(self.frameRun, text='choose csv file for EVAC data', command=self.selectEvacFile)
        #self.buttonSelectCSV.place(x=12, y=120, anchor='nw')
        self.buttonSelectCSV.pack()
        self.showHelp(self.buttonSelectCSV, "Select .csv file to set up the agent parameters for the simulation")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        self.buttonSelectFDS =Button(self.frameRun, text='choose fds file for FDS data', command=self.selectFDSFile)
        #self.buttonSelectFDS.place(x=12, y=150, anchor='nw')
        self.buttonSelectFDS.pack()
        self.showHelp(self.buttonSelectFDS, "Select FDS file to set up the compartment geometry for the simulation")
        
        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        
        #self.buttonRead = Button(self.frameRun, text='read now: read in data', command=self.readData)
        #self.buttonRead.pack()
        self.buttonGeom = Button(self.frameRun, text='read now: create simulation data', command=self.testGeom)
        #self.buttonGeom.place(x=12, y=180, anchor='nw')
        self.buttonGeom.pack()
        self.showHelp(self.buttonGeom, "Create or modify the simulation data by reading the input file (FDS or CSV files as selected above).  \n Users can easily modify the data such as adding doors, walls or exits.")

        #self.buttonDel = Button(self.frameRun, text='delete now: delete simulation data', command=self.deleteGeom)
        #self.buttonDel.pack()
        #self.showHelp(self.buttonDel, "Delete the existing simulation so that users can create a new one.")

        self.buttonFlow = Button(self.frameRun, text='compute now: flow field', command=self.testFlow)
        self.buttonFlow.place(x=262, y=120, anchor='nw')
        self.buttonFlow.pack()
        #self.showHelp(self.buttonFlow, "Generate the door flow field.  \n Users should first select either the nearest-exit method (default) or exit probablity method")
        
        self.buttonComp = Button(self.frameRun, text='compute now: only compute simulation', command=self.compSim)
        #self.buttonComp.place(x=262, y=150, anchor='nw')
        self.buttonComp.pack()
        self.showHelp(self.buttonComp, "Only compute the numerical result without displaying in pygame.  \n Users can use another python program evac-prt5-tool to display the the numerical result.")
        
        self.buttonStart = Button(self.frameRun, text='start now: compute and show simulation', command=self.startSim)
        #self.buttonStart.place(x=262, y=180, anchor='nw')
        self.buttonStart.pack()
        self.showHelp(self.buttonStart, "Compute the numerical result and display the result timely in pygame.  \n Please select the items in parameter panel to adjust the appearance in pygame window. ")

        #buttonStart.place(x=5,y=220)
        print(self.fname_FDS, self.fname_EVAC)


        # --------------------------------------------
        # frameParameters
        # --------------------------------------------
        self.SHOWTIME_Var = IntVar()
        self.SHOWTIME_Var.set(1)
        self.SHOWTIME_CB=Checkbutton(self.frameParameters, text= 'Show Time in Simulation', variable=self.SHOWTIME_Var, onvalue=1, offvalue=0)
        #self.SHOWTIME_CB.pack(side=TOP, padx=2, pady=2)
        self.SHOWTIME_CB.place(x=2, y=6)
        self.showHelp(self.SHOWTIME_CB, "Show time counts in the simulation.")
        
        self.SHOWSTRESS_Var = IntVar()
        self.SHOWSTRESS_Var.set(0)
        self.SHOWSTRESS_CB=Checkbutton(self.frameParameters, text= 'Show Stress Level in Simulation', variable=self.SHOWSTRESS_Var, onvalue=1, offvalue=0)
        #self.SHOWSTRESS_CB.pack(side=TOP, padx=2, pady=2)
        self.SHOWSTRESS_CB.place(x=2, y=36)
        self.showHelp(self.SHOWSTRESS_CB, "Show agents' stress level data in the simulation.  Try to press key <S> in pyagme screen!")

        self.SHOWGEOM_Var = IntVar()
        self.SHOWGEOM_Var.set(0)
        self.SHOWGEOM_CB=Checkbutton(self.frameParameters, text= 'Show compartment data in simulation', variable=self.SHOWGEOM_Var, onvalue=1, offvalue=0)
        #self.SHOWGEOM_CB.pack(side=TOP, padx=2, pady=2)
        self.SHOWGEOM_CB.place(x=300, y=6)
        self.showHelp(self.SHOWGEOM_CB, "Show compartment geometry data in the simulation.")

        self.SHOWFORCE_Var = IntVar()
        self.SHOWFORCE_Var.set(1)
        self.SHOWFORCE_CB=Checkbutton(self.frameParameters, text= 'Show forces on agents in simulation', variable=self.SHOWFORCE_Var, onvalue=1, offvalue=0)
        self.SHOWFORCE_CB.place(x=300, y=36)
        self.showHelp(self.SHOWFORCE_CB, "Show various forces on agents in the simulation. \n  Motive Force: Red;  Interpersonal Force: Pink; Wall Force: Purple;  Door Force: Green")
        
        self.NearExit_Var = IntVar()
        self.NearExit_Var.set(1)
        self.NearExit_CB=Checkbutton(self.frameParameters, text= 'Use nearest exit strategy', variable=self.NearExit_Var, onvalue=1, offvalue=0)
        self.NearExit_CB.place(x=2, y=66)
        self.showHelp(self.NearExit_CB, "Use nearest exit strategy to guide evacuee agents.")
        
        self.DumpData_Var = IntVar()
        self.DumpData_Var.set(0)
        self.DumpData_CB=Checkbutton(self.frameParameters, text= 'Dump data to a binary file', variable=self.DumpData_Var, onvalue=1, offvalue=0)
        self.DumpData_CB.place(x=300, y=66)
        self.showHelp(self.DumpData_CB, "Dump data to a binary file such that it can be visualized by our small program evac-prt5-tool.")        

        self.GroupBehavior_Var = IntVar()
        self.GroupBehavior_Var.set(0)
        self.GroupBehavior_CB=Checkbutton(self.frameParameters, text= 'Compute Group Behavior', variable=self.GroupBehavior_Var, onvalue=1, offvalue=0)
        self.GroupBehavior_CB.place(x=300, y=96)
        self.showHelp(self.GroupBehavior_CB, "Compute Group Social Force and Self Repulsion.  \n Check this button only if you have specified the group parameters in input file.")  #Uncheck it if you do not know what it means.")  

        #print self.SHOWTIME_Var.get()


        # --------------------------------------------
        # frameGuide
        # --------------------------------------------
        scrollInfo = Scrollbar(self.frameGuide)
        self.textGuide = Text(self.frameGuide, width=45,height=13,bg='white',wrap=WORD,font=("Courier",10))
        #self.textGuide = Text(self.frameGuide, width=45,height=13,bg='lightgrey',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textGuide.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollInfo.config(command=self.textGuide.yview)
        self.textGuide.config(yscrollcommand=scrollInfo.set)
        
        self.textGuide.insert(END, 'QuickStart: \nStep1: Please select csv file or fds file to read in evac data and compartement geometry data!\n')
        self.textGuide.insert(END, 'Step2: Create simulation object!\n')
        self.textGuide.insert(END, 'Step3: Compute and visualize simulation!\n')
        self.textGuide.insert(END, '\nWhen simulation starts, please try to press the following keys in your keybroad, and you will see the effects on the screen. \n')
        self.textGuide.insert(END, 'Press <pageup/pagedown> to zoom in or zoom out.\n')
        self.textGuide.insert(END, 'Press arrow keys to move the entities vertically or horizonally in screen.\n')
        self.textGuide.insert(END, 'Press 1/2/3 in number panel (Right side in the keyboard) to display the door or exit data on the screen.\n')
        self.textGuide.insert(END, 'Press <o> and <p> to show the egress flow field. \n')
        self.textGuide.insert(END, 'Press <space> to pause or resume the simulaton. \n\n')
        
        self.textGuide.insert(END, '---------------------------------------------------\n')
        
        self.textGuide.insert(END, 'This manual introduces a simulation tool to study complex crowd behavior in social context. The agent-based model is extended based on the well-known social force model, and it mainly describes how agents interact with each other, and also with surrounding facilities such as walls, doors and exits. The simulation platform is compatible to the FDS+Evac, and the input data in FDS+Evac could be imported into our simulation platform to create single-floor compartment geometry, and a flow solver is used to generate the egress flow field towards exits. Most importantly, we plan to integrate advanced social and psychological theory into our simulation platform, especially investigating human behavior in emergency evacuation, such as pre-evacuation behavior, exit-selection activities, social group and herding effect and so forth.  \n\nThe program mainly consists of three component: User Interface, Simulation Core, Data and Visualization Tool. \n\n')
        
        self.textGuide.insert(END, '\nAgent-based model (ABM) describes interactions among individual agents and their surroundings. In the simulation there are four types of entities: agents, walls, doors and exits.  As below we will introduce how to specify these entities.')
        
        self.textGuide.insert(END, '\n\nThe walls, doors and exits are alternatively specified by FDS input files. Users are welcome to use existing FDS input files to create compartment geometries. In current version only one-floor crowd simulation is supported. So if there are multiple evacuation meshes in FDS input files, they should all belong to the same z interval in the vertical direction (z axis). By using FDS input files the walls are created by \&OBST, and the doors are specified by \&HOLE or \&DOOR. The exits are obtained from \&EXIT in FDS input files. If users want to find more about how FDS define a compartment area, please refer to FDS UserGuide for more information.  If users do not use FDS input files, the above entities can alternatively be specified by using csv files as introduced below.')
        
        
        self.textGuide.insert(END, '\n\n{Walls}: Walls are obstruction in a compartment geometry that confine agent movement, and they set up the boundary of a room or certain space that agents cannot go through. In our program wall are either lines or rectangular areas. If any users are interested, please feel free to extend the wall types to circular or polyangular areas. If users import walls from a FDS input file, the walls are created as a rectangular type and it corresponds to \&OBST in FDS input file.  \nIf users specify a line obstruction, it is expected to input the position of starting point and ending point of a line. If users specify a rectangular obstruction, it is expected to input the diagonal position of upper left point and lower right point of a rectangular area.')

        self.textGuide.insert(END, '\n\n<startX, startY>: Upper left point for rectangular obstruction; Or starting point for line obstruction. \n<endX, endY>:Lower right point for rectangular obstruction; Or ending point for line obstruction. \n\n<arrow>: Direction assigned to the obstruction so that agents will be guided when seeing this obstruction, especially when they do not have any target door or exit. The direction implies if the obstruction provides evacuees with any egress information such as exit signs on the walls or not. The value could be +1 for positive x direction, -1 for negative x direction, +2 for positive y direction and -2 for negative y direction. If no direction is given, the value is 0. \n\n|id|: id number assigned to this obstruction; id number is optionally shown in the pygame screen so that users can easily modify the obstruction. \n\n|inComp|: a boolean variable to indicate if the obstruction is in computation loop or not. Normally it is given true/1. If users want to quickly remove a obstruction in simulation, it is assigned be to false/0. \n\n|mode|: Either rectangular or line obstruction in current program; the default mode is rectangular model.')

        self.textGuide.insert(END, '\n\n{Doors and Exit}: Doors are passageways that direct agents toward certain areas, and they may be placed over a wall so that agents can get through the wall by the door. Doors can also be placed as a waypoint if not attached to any walls, and they can be considered as arrows or markers on the ground that guide agent egress movement. In brief doors affect agent way-finding activities and they help agents to form a roadmap to exits. In current program doors are only specified as rectangular object.  Exits are a special types of doors which represent paths to the safety. Thus they may be deemed as safety areas, and computation of an agent is complete when the agent reaches an exit.  An exit is usually placed over a wall like doors, but it can also be put anywhere independently without walls. In the program exits are only defined as rectangular areas. The specific features of doors and exits are given as below.')  

        self.textGuide.insert(END, '\n\n<startX, startY>: Upper left point for rectangular door/ exit. \n<endX, endY>:Lower right point for rectangular door/exit. \n\n|arrow|: Direction assigned to the door or exit so that agents will be guided when seeing this entity, especially when they do not have any target door or exit. The direction implies if the door or exit provides evacuees with any egress information such as exit signs or not. The value could be +1 for positive x direction, -1 for negative x direction, +2 for positive y direction and -2 for negative y direction. If no direction is given, the value is zero. Please refer to FDS+Evac manual to better understand the direction setting. \n\n|id|: id number assigned to the door/exit; id number is optionally shown in the pygame screen so that users can easily identify the door information. \n\n|inComp|: a boolean variable to indicate if the door/exit is in computation loop or not. Normally it is given true/1. If users want to quickly remove a door/exit in simulation, they could assign it be to false/0 for a quick test. \n\n|exitSign|: a boolean variable to indicate if the door/exit is attached with an exit sign or not. If there is an exit sign the boolean variable is given true/1. Actually it is not that useful in existing door selection algorithm.  So users may omit this feature currently. ')
        
        
        self.textGuide.insert(END, '\n\n{Agents}: Finally and most importantly, agents are the core entity in computation process. They interact with each other to form collective behavior of crowd. They also interact with above types of entities to form egress motion toward exits. The resulting program is essentially a multi-agent simulation of pedestrian crowd. Each agent is modeled by extending the well-known social force model. The model is further advanced by integrating several features including pre-evacuation behavior, group behavior, way-finding behavior and so forth.')  

        self.textGuide.insert(END, '\n\n<InitalX, InitialY>: Initial position of an agent in 2D planar space. \n\n<DestX, DestY>: Destination position in 2D planar space.  This value is almost not used in current computational loop because the destination position is automatically determined by the exit selection algorithm.  When the exit is selected by an agent, the destination position is given by the exit position. \n\n|mass|: The mass of agents.  \n\n|tau|: Tau parameter in the social force model, or as usually called relaxation time in many-particle systems or statistical physics, and it critically affects how fast the actual velocity converges to the desired velocity.  \n\n|tpre|: Time period for pre-evacuation stage. \n\n|interRange|: The range when agents have herding effect, which means they may exchange opinions by talking. \n\n|p|: parameter p in opinion dynamics, and it affects herding effect.  \n\n|pMode|: This parameter affects how parameter p is dynamically changing.  Currently it is not used in computational loop.  \n\n|aType|: The type of way-finding behaviors.  Some agents may actively search for exits while others may just follow the crowd.  In current simulation all agents follow the egress flow field, and thus this parameter is not actually used in existing version of code.  \n\n|ID|: ID number assigned to this agent. ID number is optionally shown in the pygame screen. \n\n|inComp|: a boolean variable to indicate if the agent is in computation loop or not. Normally it is given true. If users want to remove an agent in simulation, they could assign it be to false for test.')

    def updateCtrlParam(self):
        self.currentSimu.SHOWTIME = self.SHOWTIME_Var.get()
        self.currentSimu.SHOWSTRESS = self.SHOWSTRESS_Var.get()
        self.currentSimu.dumpBin = self.DumpData_Var.get()
        
        if self.SHOWGEOM_Var.get():
            self.currentSimu.SHOWWALLDATA=True
            self.currentSimu.SHOWDOORDATA=True
            self.currentSimu.SHOWEXITDATA=True
        else:
            self.currentSimu.SHOWWALLDATA=False
            self.currentSimu.SHOWDOORDATA=False
            self.currentSimu.SHOWEXITDATA=False
            
        if self.SHOWFORCE_Var.get():
            self.currentSimu.DRAWWALLFORCE=True
            self.currentSimu.DRAWDOORFORCE=True
            self.currentSimu.DRAWGROUPFORCE=True
            #self.currentSimu.DRAWSELFREPULSION=True
        else:
            self.currentSimu.DRAWWALLFORCE=False
            self.currentSimu.DRAWDOORFORCE=False
            self.currentSimu.DRAWGROUPFORCE=False
            #self.currentSimu.DRAWSELFREPULSION=False

        if self.NearExit_Var.get():
            self.currentSimu.solver=1
        else:
            self.currentSimu.solver=2

        if self.GroupBehavior_Var.get():
            self.currentSimu.GROUPBEHAVIOR=True
            self.currentSimu.SELFREPULSION=True
        else:
            self.currentSimu.GROUPBEHAVIOR=False
            self.currentSimu.SELFREPULSION=False

    def start(self):
        self.window.mainloop()

    def quitGUI(self):
        #pylab.close('all')
        self.window.quit()
        self.window.destroy()

    def setStatusStr(self,newStatus):
        self.statusStr = newStatus
        self.statusText.set(self.statusStr)

    def showHelp(self, widget, text):
        def setText(self):
            self.statusText.set(text)
            self.status.configure(foreground='black')
            
        def showHelpLeave(self):
            self.statusText.set(self.statusStr)
            self.status.configure(foreground='black')
        widget.bind("<Enter>", lambda e : setText(self))
        widget.bind("<Leave>", lambda e : showHelpLeave(self))
        

    def selectFDSFile(self):
        self.fname_FDS = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        temp=re.split(r'/', self.fname_FDS)
        #temp=self.fname_FDS.split('/') 
        self.lb0.config(text = "Optional: If .fds is selected, the compartment geometry is created by .fds file. \n"+"The FDS data file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_FDS:', self.fname_FDS)
        self.setStatusStr("Simulation not yet started!")

    def selectEvacFile(self):
        self.fname_EVAC = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        temp=self.fname_EVAC.split('/') 
        self.lb1.config(text = "The input .csv file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, 'fname_EVAC:   '+self.fname_EVAC)
        print('fname', self.fname_EVAC)
        self.setStatusStr("Simulation not yet started!")

    #def readData(self):
    #    self.currentSimu = simulation()
    #    self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-gui")
    #    #myTest.read_data()

    #def deleteGeom(self):
    #    self.currentSimu = None

    def testGeom(self):
        #if self.currentSimu is None:
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        sunpro2 = mp.Process(target=show_geom(self.currentSimu)) 
        sunpro2.start()
        #sunpro2.join()
        if self.currentSimu.continueToSimu:
            #self.currentSimu.preprocessGeom()
            #self.currentSimu.preprocessAgent()
            #self.currentSimu.flowMesh()
            self.updateCtrlParam()
            self.currentSimu.preprocessGeom()
            self.currentSimu.preprocessAgent()
            self.currentSimu.buildMesh()
            self.currentSimu.flowMesh()
            self.currentSimu.computeDoorDirection()
            sunpro1 = mp.Process(target=show_simu(self.currentSimu))
            #sunpro1 = mp.Process(target=self.currentSimu.flowMesh())
            sunpro1.start()
            #sunpro1.join()

        #show_geom(myTest)
        #myTest.show_simulation()
        #self.currentSimu.quit()

    def testFlow(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        show_geom(self.currentSimu)
        #sunpro2 = mp.Process(target=show_geom(self.currentSimu)) 
        #sunpro2.start()
        #sunpro2.join()
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        self.currentSimu.buildMesh()
        self.currentSimu.flowMesh()
        self.currentSimu.computeDoorDirection()
        show_flow(self.currentSimu)

    # Compute the numerical result and display the result timely in pygame
    def startSim(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        #self.textInformation.insert(END, "Start Simulation Now!")
        self.setStatusStr("Simulation starts!  GUI window is not effective when Pygame screen is displayed!")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        self.currentSimu.buildMesh()
        self.currentSimu.flowMesh()
        self.currentSimu.computeDoorDirection()
        sunpro1 = mp.Process(target=show_simu(self.currentSimu))        
        sunpro1.start()
        #sunpro1.join()
        self.setStatusStr("Simulation not yet started!")
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()
    
    # Only compute the numerical result without displaying in pygame
    def compSim(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        #self.textInformation.insert(END, "Start Simulation Now!")
        self.setStatusStr("Simulation starts!  GUI window is not effective now")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        self.currentSimu.buildMesh()
        self.currentSimu.flowMesh()
        self.currentSimu.computeDoorDirection()
        sunpro1 = mp.Process(target=compute_simu(self.currentSimu))        
        sunpro1.start()
        #sunpro1.join()
        self.setStatusStr("Simulation not yet started!")
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()
            
#==========================================
#===This is a small GUI widget used for debug mode=======
#==========================================
def startPage(FN_FDS=None, FN_EVAC=None):

    #FN_FDS=None  #'1'
    #FN_EVAC=None  #'2'
    #FN_Doors=None  #'3'

    FN_Info = ['FDS', 'EVAC'] #, 'Doors']
    FN=[None, None] #, None]
    FN[0]=FN_FDS
    FN[1]=FN_EVAC

    window = Tk()
    window.title('my window')
    window.geometry('760x300')

    notebook = Notebook(window)      
    # self.notebook.grid(row=0,column=0,padx=2,pady=2,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:30:25
    notebook.pack(side=TOP, padx=2, pady=2)
    
    # added "self.rootWindow" by Hiroki Sayama 10/09/2018
    frameRun = Frame(window)
    frameSettings = Frame(window)
    #frameParameters = Frame(window)
    #frameInformation = Frame(window)


    notebook.add(frameRun,text="Run")
    notebook.add(frameSettings,text="Settings")
    #notebook.add(frameParameters,text="Parameters")
    #notebook.add(frameInformation,text="Info")
    notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
    # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02
    
    #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
    # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
    #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

    #from Tkinter.tkFileDialog import askopenfilename
    #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
    #def quit_botton(event):
        
    def selectFile(index):
        #tk.messagebox.showinfo(title='Hi', message='hahahaha') # return 'ok'
        #tk.messagebox.showwarning(title='Hi', message='nononono') # return 'ok'
        #tk.messagebox.showerror(title='Hi', message='No!! never') # return 'ok'
        #print(tk.messagebox.askquestion(title='Hi', message='hahahaha')) # return 'yes' , 'no'
        #print(tk.messagebox.askyesno(title='Hi', message='hahahaha')) # return True, False
        #print(tk.messagebox.asktrycancel(title='Hi', message='hahahaha')) # return True, False
        #print(tk.messagebox.askokcancel(title='Hi', message='hahahaha')) # return True, False
        #print(tk.messagebox.askyesnocancel(title="Hi", message="haha")) # return, True, False, None
        #from Tkinter.tkFileDialog import askopenfilename
        FN[index] = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        if index ==0:
            lb0.config(text = "Optional: The fds file selected: "+str(FN[index])+"\n")
        elif index ==1:
            lb1.config(text = "The input csv file selected: "+str(FN[index])+"\n")
        #elif index ==2:
        #    lb2.config(text = "The exit data file selected: "+str(FN[index])+"\n")
        print('fname', FN[index])

    #lb = tk.Label(window,text = '')
    #lb.pack()
    #print FN_Agents, FN_Walls, FN_Doors

    # Define checkbox for selection
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()

    CB1=Checkbutton(frameRun, text= 'Use FDS File as Geometry Input File', variable=CheckVar1, onvalue=1, offvalue=0)
    #CB2=Checkbutton(window, text= 'Use Group Force', variable=CheckVar2, onvalue=1, offvalue=0)
    CB1.pack()
    #CB2.pack()

    #print CheckVar1.get()

    lb_guide = Label(frameRun,text =  "Please select the input files of the simulation\n" + "Geom: Use .fds or .csv  Evac: Use .csv")
    lb_guide.pack()

    lb0 = Label(frameRun,text =  "Optional: The fds file selected: "+str(FN[0])+"\n")
    lb0.pack()

    lb1 = Label(frameRun,text =  "The input csv file selected: "+str(FN[1])+"\n")
    lb1.pack()

    #lb2 = Label(frameRun,text =  "The exit data file selected: "+str(FN[2])+"\n")
    #lb2.pack()

    buttonSelectFDS =Button(frameRun, text='choose fds file for FDS data', command=lambda: selectFile(0)).pack()
    buttonSelectCSV =Button(frameRun, text='choose csv file for EVAC data', command=lambda: selectFile(1)).pack()
    #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()
    #FN_Doors = fname
    #if CheckVar1.get():
    #    buttonSelectFDS.configure(state=DISABLED)
    #TestV=CheckVar1.get()

    buttonStart = Button(frameRun, text='start now: read in data', command=window.quit).pack()
    #buttonStart.place(x=5,y=220)
    #print FN_Agents, FN_Walls, FN_Doors

    print("As below is the input files you update now!")
    #print FN[0]
    #print FN[1] #, FN[2]

    window.mainloop()

    #print FN['Agents'], FN['Walls'], FN['Doors']
    #print FN[0], FN[1] #, FN[2]
    #print TestV

    #FN_FDS = FN[0]
    #FN_EVAC = FN[1]

    return FN

if __name__ == '__main__':
    myGUI=GUI()
    myGUI.start()


    
