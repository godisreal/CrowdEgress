
import os, sys, csv
import multiprocessing as mp
from simulation import *
from data_func import *
from draw_func import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
    from tkinter.ttk import Treeview
    import tkinter.filedialog as tkf
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    from ttk import Treeview
    from ttk import Entry
    import tkFileDialog as tkf


class GUI(object):

    def __init__(self, FN_FDS=None, FN_EVAC=None):

        #self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        #self.FN=[None, None] #, None]
        #self.FN[0]=FN_FDS
        #self.FN[1]=FN_EVAC

        self.ZOOM=60.0
        self.xSpa=30.0
        self.ySpa=30.0
        
        if os.path.exists("log.txt") and FN_EVAC is None and FN_FDS is None:
            for line in open("log.txt", "r"):
                if re.match('FN_FDS', line):
                    temp =  line.split('=')
                    FN_FDS = temp[1].strip()
                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    FN_EVAC = temp[1].strip()
                    
                    
        self.fname_FDS = FN_FDS
        self.fname_EVAC = FN_EVAC
        self.fname_OutTXT = None
        self.fname_OutBIN = None
        self.fname_OutNPZ = "vel_flow0.npz"
        self.currentdir = None
        self.currentSimu = None
        
        if self.fname_EVAC is not None:
            self.currentdir = os.path.dirname(self.fname_EVAC)
        
        self.window = Tk()
        self.window.title('crowd egress simulator')
        self.window.geometry('960x600')

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
        self.frameFlow = Frame(self.window)
        self.frameSoc = Frame(self.window)
        self.frameParameters = Frame(self.window)
        self.frameData = Frame(self.window)
        self.frameCSV = Frame(self.window)
        self.frameGuide = Frame(self.window)
        #self.frameExit = Frame(self.window)
        #self.frameSettings = Frame(self.window)

        scrollInfo = Scrollbar(self.window)#frameInformation)
        self.textInformation = Text(self.window, width=45,height=6,bg='lightgray',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textInformation.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollInfo.config(command=self.textInformation.yview)
        self.textInformation.config(yscrollcommand=scrollInfo.set)
        self.textInformation.insert(END, 'QuickStart: \nStep1: Please select csv file or fds file to read in evac data and compartement geometry data!\n')
        self.textInformation.insert(END, 'Step2: Create simulation object!\n')
        self.textInformation.insert(END, 'Step3: Compute and visualize simulation!\n')
        self.textInformation.insert(END, '\nWhen simulation starts, please try to press the following keys in your keybroad, and you will see the effects on the screen. \n')
        self.textInformation.insert(END, 'Press <pageup/pagedown> to zoom in or zoom out.\n')
        self.textInformation.insert(END, 'Press arrow keys to move the entities vertically or horizonally in screen.\n')
        self.textInformation.insert(END, 'Press 1/2/3 in number panel (Right side in the keyboard) to display the door or exit data on the screen.\n')
        self.textInformation.insert(END, 'Press <o> and <p> to show the egress flow field. \n')
        self.textInformation.insert(END, 'Press <space> to pause or resume the simulaton. \n')
        
        self.textInformation.insert(END, '\n\nFiles selected in the last run (Read from log.txt): \n')
        self.textInformation.insert(END, str(self.fname_EVAC)+"\n")
        self.textInformation.insert(END, str(self.fname_FDS)+"\n")


        self.notebook.add(self.frameRun,text="QuickStart")
        self.notebook.add(self.frameParameters,text="Parameters")
        self.notebook.add(self.frameFlow,text="MeshFlow")
        #self.notebook.add(self.frameInformation,text="Information")
        self.notebook.add(self.frameSoc,text="EvacAgent")       
        self.notebook.add(self.frameData,text="DataTool")
        self.notebook.add(self.frameCSV,text="CSVTool") 
        self.notebook.add(self.frameGuide,text="Readme")
        #self.notebook.add(self.frameSettings,text="Settings")
        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
        
        # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02
        
        #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        #from Tkinter.tkFileDialog import askopenfilename
        #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
        #def quit_botton(event):
        
        #self.tabRun=LabelFrame(self.frameRun, text='SelectFiles/QuickRunSimulation')
        #self.tabRun.grid(row=0, column=0, padx=3, pady=3, sticky='nswe')

        #self.tabFlow=LabelFrame(self.frameFlow, text='FlowSettings')
        #self.tabFlow.grid(row=0, column=0, padx=3, pady=3, sticky='nswe')

        ############################################################################
        # --------------------------------------------
        # frameRunSimulation
        # --------------------------------------------
        
        self.lb_guide = Label(self.frameRun, text = "Please select the input files for simulation:\n How-To: Select Input Files --> Create/Modify Simulation --> Run Simulation \n") 
        # + "Please check the examples for details")
        self.lb_guide.pack()
        

        self.lb_csv = Label(self.frameRun,text = "Use csv file to create agent data or together with compartement geometry data.\n"+"The input csv file selected: "+str(self.fname_EVAC)+"\n")
        self.lb_csv.pack()
        
        self.lb_fds = Label(self.frameRun,text =  "Optional: If fds is selected, the compartment geometry could be created by fds file. \n"+"The fds file selected: "+str(self.fname_FDS)+"\n")
        self.lb_fds.pack()


        self.buttonSelectFDS =Button(self.frameRun, text='choose fds file for FDS data', command=self.selectFDSFile)
        #self.buttonSelectFDS.place(x=2, y=60)
        self.buttonSelectFDS.pack() #place(x=20, y=146)
        self.showHelp(self.buttonSelectFDS, "Select fds file to set up the compartment geometry for the simulation")
        

        self.buttonSelectCSV =Button(self.frameRun, text='choose csv file for EVAC data', command=self.selectEvacFile)
        #self.buttonSelectCSV.place(x=2, y=120)
        self.buttonSelectCSV.pack() #place(x=20, y=176)
        self.showHelp(self.buttonSelectCSV, "Select .csv file to set up the agent parameters for the simulation")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        
        #self.buttonRead = Button(self.frameRun, text='read now: read in data', command=self.readData)
        #self.buttonRead.pack()
        self.buttonGeom = Button(self.frameRun, text='Create/Modify simulation object', command=self.testGeom)
        self.buttonGeom.pack() #place(x=20, y=206)
        self.showHelp(self.buttonGeom, "Create or modify the simulation data by reading the input file (FDS or CSV files as selected above).  \n Users can easily modify the data such as adding doors, walls or exits.")

        #self.buttonDel = Button(self.frameRun, text='delete now: delete simulation data', command=self.deleteGeom)
        #self.buttonDel.pack()
        #self.showHelp(self.buttonDel, "Delete the existing simulation so that users can create a new one.")
 
        self.buttonFlow = Button(self.frameRun, text='compute egress flow field', command=self.testFlow)
        self.buttonFlow.pack() #place(x=306, y=206)
        self.showHelp(self.buttonFlow, "Generate the door flow field.  \n Users should first select either the nearest-exit method (default) or exit probablity method")

        self.buttonComp = Button(self.frameRun, text='compute simulation and dump data', command=self.compSim)
        self.buttonComp.pack() #place(x=306, y=176)
        #self.buttonComp.grid(row=3, column=1, rowspan=2, ipady=7)
        #self.buttonComp.place(x=397,y=191)
        self.showHelp(self.buttonComp, "Only compute the numerical result without displaying in pygame.  \n Users can use another python program evac-prt5-tool to display the the numerical result.")
        
        self.buttonStart = Button(self.frameRun, text='compute and visualize simulation', command=self.startSim)
        self.buttonStart.pack() #place(x=20, y=236)
        self.showHelp(self.buttonStart, "Compute the numerical result and display the result timely in pygame.  \n Please select the items in parameter panel to adjust the appearance in pygame window. ")


        self.UseFDS_Var = IntVar()
        self.UseFDS_Var.set(1)
        self.UseFDS_CB=Checkbutton(self.frameRun, text= 'Use FDS file to create compartment geometry', variable=self.UseFDS_Var, onvalue=1, offvalue=0)
        self.UseFDS_CB.pack() #place(x=306, y=146)
        self.showHelp(self.UseFDS_CB, "Use FDS file to create compartment geometry, including walls, doors and exits.")


        self.AutoPlot_Var = IntVar()
        self.AutoPlot_Var.set(1)
        self.AutoPlot_CB=Checkbutton(self.frameRun, text= 'Automatically plot figures from output data', variable=self.AutoPlot_Var, onvalue=1, offvalue=0)
        self.AutoPlot_CB.pack() #place(x=306, y=236)
        self.showHelp(self.AutoPlot_CB, "Plot figures automatically when simulation is complete.")


        #buttonStart.place(x=5,y=220)
        print(self.fname_FDS, self.fname_EVAC)

        #####################################################################################33
        # --------------------------------------------
        # frameParameters
        # --------------------------------------------
        #self.SHOWTIME_Var = IntVar()
        #self.SHOWTIME_Var.set(1)
        #self.SHOWTIME_CB=Checkbutton(self.frameParameters, text= 'Show Time in Simulation', variable=self.SHOWTIME_Var, onvalue=1, offvalue=0)
        #self.SHOWTIME_CB.pack(side=TOP, padx=2, pady=2)
        #self.SHOWTIME_CB.place(x=2, y=6)
        #self.showHelp(self.SHOWTIME_CB, "Show time counts in the simulation.")
        
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
        self.SHOWFORCE_CB=Checkbutton(self.frameParameters, text= 'Show forces on agents', variable=self.SHOWFORCE_Var, onvalue=1, offvalue=0)
        self.SHOWFORCE_CB.place(x=2, y=6)
        self.showHelp(self.SHOWFORCE_CB, "Show various forces on agents with colors in the simulation. \n  Motive Force: Red;  Interpersonal Force: Pink; Wall Force: Purple;  Door Force: Green")
        
        self.NearExit_Var = IntVar()
        self.NearExit_Var.set(0)
        self.NearExit_CB=Checkbutton(self.frameParameters, text= 'Use nearest exit strategy', variable=self.NearExit_Var, onvalue=1, offvalue=0)
        self.NearExit_CB.place(x=2, y=66)
        self.showHelp(self.NearExit_CB, "Use nearest exit strategy to guide evacuee agents.")
        
        self.DumpData_Var = IntVar()
        self.DumpData_Var.set(1)
        self.DumpData_CB=Checkbutton(self.frameParameters, text= 'Dump data to a binary file', variable=self.DumpData_Var, onvalue=1, offvalue=0)
        self.DumpData_CB.place(x=300, y=66)
        self.showHelp(self.DumpData_CB, "Dump data to a binary file such that it can be visualized by our small program evac-prt5-tool.")        

        self.GroupBehavior_Var = IntVar()
        self.GroupBehavior_Var.set(1)
        self.GroupBehavior_CB=Checkbutton(self.frameParameters, text= 'Compute Group Behavior', variable=self.GroupBehavior_Var, onvalue=1, offvalue=0)
        self.GroupBehavior_CB.place(x=300, y=36)  #(x=300, y=96)
        self.showHelp(self.GroupBehavior_CB, "Compute Group Social Force and Self Repulsion.  \n Check this button only if you have specified the group parameters in input file.")  #Uncheck it if you do not know what it means.")  


        self.lbSoc2 = Label(self.frameParameters, text =  "Optional: Below please input the time interval for simulation step and data output step. \n")
        self.lbSoc2.place(x=12, y=130)

        self.lb_dtSim = Label(self.frameParameters, text = 'dtSim:')
        self.lb_dtSim.place(x=12, y=152)
        self.dtSim_gui = StringVar()
        nameEntered_dtSim = Entry(self.frameParameters, width=12, textvariable=self.dtSim_gui)
        nameEntered_dtSim.insert(0, '0.2')
        nameEntered_dtSim.place(x=62, y=152)

        self.lb_dtDump = Label(self.frameParameters, text = 'dtDump:')
        self.lb_dtDump.place(x=212, y=152)
        self.dtDump_gui = StringVar()
        nameEntered_dtDump = Entry(self.frameParameters, width=12, textvariable=self.dtDump_gui)
        nameEntered_dtDump.insert(0, '0.2')
        nameEntered_dtDump.place(x=269, y=152)
        

        self.lb3 = Label(self.frameParameters, text =  "Optional: If fds file is selected, the compartment geometry is created from fds file. \n")
        self.lb3.place(x=12, y=179)

        self.lb2 = Label(self.frameParameters, text =  "Optional: The single-floor mesh within x-y plane is read from fds file between z_min and z_max. \n")
        self.lb2.place(x=12, y=200)

        self.lb_zmin = Label(self.frameParameters, text = 'z_min:')
        self.lb_zmin.place(x=12, y=226)
        self.zmin_gui = StringVar()
        nameEntered_zmin = Entry(self.frameParameters, width=12, textvariable=self.zmin_gui)
        nameEntered_zmin.insert(0, '0.0')
        nameEntered_zmin.place(x=62, y=226)
        self.showHelp(nameEntered_zmin, "Use FDS file to create compartment geometry, \n and zmin is the lower bound in z axis for one-floor geometry mesh.")

        self.lb_zmax = Label(self.frameParameters, text = 'z_max:')
        self.lb_zmax.place(x=212, y=226)
        self.zmax_gui = StringVar()
        nameEntered_zmax = Entry(self.frameParameters, width=12, textvariable=self.zmax_gui)
        nameEntered_zmax.insert(0, '3.0')
        nameEntered_zmax.place(x=262, y=226)
        self.showHelp(nameEntered_zmax, "Use FDS file to create compartment geometry, \n and zmax is the upper bound in z axis for one-floor geometry mesh.")        
        ######################################################################################
        # --------------------------------------------
        # frameFlowSettings
        # --------------------------------------------
        # Changing our Label
        #ttk.Label(tabFlow, text='Please define the flow mesh as below:').grid(column=0, row=0, sticky='W')
        #self.lb_tabFlow = Label(self.tabFlow, text = 'Please define the flow mesh as below:')
        #self.lb_tabFlow.grid(column=0, row=1, sticky='W')
        
        self.lb_xmin = Label(self.frameFlow, text = 'x_min:')
        self.lb_xmin.place(x=12, y=6)

        # Adding a Textbox Entry widget
        self.xmin_gui = StringVar()
        nameEntered_xmin = Entry(self.frameFlow, width=12, textvariable=self.xmin_gui)
        nameEntered_xmin.insert(0, 'auto')
        nameEntered_xmin.place(x=122, y=6)
        self.showHelp(nameEntered_xmin, "Input the lower boundary value in x axis to create x-y planary mesh for one-floor geometry layout. \n Write 'auto' here if you do not know what it means and the program will automatically give the value.  ")


        self.lb_xmax = Label(self.frameFlow, text = 'x_max:')
        self.lb_xmax.place(x=12, y=36)

        # Adding a Textbox Entry widget
        self.xmax_gui = StringVar()
        nameEntered_xmax = Entry(self.frameFlow, width=12, textvariable=self.xmax_gui)
        nameEntered_xmax.insert(0, 'auto')
        nameEntered_xmax.place(x=122, y=36)
        self.showHelp(nameEntered_xmax, "Input the upper boundary value in x axis to create x-y planary mesh for one-floor geometry layout. \n Write 'auto' here if you do not know what it means and the program will automatically give the value.  ")

        self.lb_nxp = Label(self.frameFlow, text = 'num_x:')
        self.lb_nxp.place(x=12, y=66)

        # Adding a Textbox Entry widget
        self.nxp_gui = StringVar()
        nameEntered_nxp = Entry(self.frameFlow, width=12, textvariable=self.nxp_gui)
        nameEntered_nxp.insert(0, '35')
        nameEntered_nxp.place(x=122, y=66)
        self.showHelp(nameEntered_nxp, "Input the number of points in x axis for x-y planary mesh. \n The mesh is refined as the number of points increases, and more computational time will be needed. ")

        self.lb_ymin = Label(self.frameFlow, text = 'y_min:')
        self.lb_ymin.place(x=312, y=6)

        # Adding a Textbox Entry widget
        self.ymin_gui = StringVar()
        nameEntered_ymin = Entry(self.frameFlow, width=12, textvariable=self.ymin_gui)
        nameEntered_ymin.insert(0, 'auto')
        nameEntered_ymin.place(x=422, y=6)
        self.showHelp(nameEntered_ymin, "Input the lower boundary value in y axis to create x-y planary mesh for one-floor geometry layout. \n Write 'auto' here if you do not know what it means and the program will automatically give the value.  ")


        self.lb_ymax = Label(self.frameFlow, text = 'y_max:')
        self.lb_ymax.place(x=312, y=36)

        # Adding a Textbox Entry widget
        self.ymax_gui = StringVar()
        nameEntered_ymax = Entry(self.frameFlow, width=12, textvariable=self.ymax_gui)
        nameEntered_ymax.insert(0, 'auto')
        nameEntered_ymax.place(x=422, y=36)
        self.showHelp(nameEntered_ymax, "Input the upper boundary value in y axis to create x-y planary mesh for one-floor geometry layout. \n Write 'auto' here if you do not know what it means and the program will automatically give the value.  ")
        
        self.lb_nyp = Label(self.frameFlow, text = 'num_y:')
        self.lb_nyp.place(x=312, y=66)

        # Adding a Textbox Entry widget
        self.nyp_gui = StringVar()
        nameEntered_nyp = Entry(self.frameFlow, width=12, textvariable=self.nyp_gui)
        nameEntered_nyp.insert(0, '35')
        nameEntered_nyp.place(x=422, y=66)
        self.showHelp(nameEntered_nyp, "Input the number of points in y axis for x-y planary mesh. \n The mesh is refined as the number of points increases, and more computational time will be needed. ")

        self.buttonFlow2 = Button(self.frameFlow, text='compute egress flow field', command=self.testFlow)
        self.buttonFlow2.place(x=6, y=200)
        self.showHelp(self.buttonFlow2, "Generate the door flow field.  \n Users should first select either the nearest-exit method (default) or exit probablity method")

        #self.lb_outnpz = Label(self.frameFlow, text = 'The output npz file selected: None!  To show crowd fluid dynamics.')
        #self.lb_outnpz.place(x=12, y=206)        
        self.buttonCFD = Button(self.frameFlow, text='Read output npz file and show crowd fluid', command=self.selectOutNPZ)
        self.buttonCFD.place(x=6, y=230)
        self.showHelp(self.buttonCFD, "Read output npz file and show the numerical result of crowd fluid dynamics.")
        

        ##############################################
        # ============================================
        # --------------------------------------------
        # frameSoc SocialGroup
        # --------------------------------------------
        
        self.lbSoc1 = Label(self.frameSoc, text =  "Optional: Below please select the type of social interation force. \n 0: Social Force   1: Group Social Force    2: Magnetic force. ")
        self.lbSoc1.place(x=12, y=30)
        
        self.spin_socialforce = Spinbox(self.frameSoc, from_=0, to=2, width=5, bd=8) 
        self.spin_socialforce.place(x=656, y=30)
        self.showHelp(self.spin_socialforce, "Select the different formula of social force: \n 0: Social force; 1: Group Social Force; 2: Magnetic force.  ")  #Uncheck it if you do not know what it means.")
        
        self.lbSoc2 = Label(self.frameSoc, text =  "Optional: Below please input the time interval to update attention list and update target door in simulation. \n")
        self.lbSoc2.place(x=12, y=196)
        
        self.lb_dtAtt = Label(self.frameSoc, text = 'dtAtt:')
        self.lb_dtAtt.place(x=12, y=226)
        self.dtAtt_gui = StringVar()
        nameEntered_dtAtt = Entry(self.frameSoc, width=12, textvariable=self.dtAtt_gui)
        nameEntered_dtAtt.insert(0, '1.0')
        nameEntered_dtAtt.place(x=62, y=226)

        self.lb_dtExit = Label(self.frameSoc, text = 'dtExit:')
        self.lb_dtExit.place(x=212, y=226)
        self.dtExit_gui = StringVar()
        nameEntered_dtExit = Entry(self.frameSoc, width=12, textvariable=self.dtExit_gui)
        nameEntered_dtExit.insert(0, '1.0')
        nameEntered_dtExit.place(x=262, y=226)


        ##############################################
        # ============================================
        # --------------------------------------------
        # frameData Data Tool
        # --------------------------------------------

        self.buttonTpre = Button(self.frameData, text='plot pre-movement time from output data', command=self.selectOutBinFile_Tpre)
        self.buttonTpre.place(x=19, y=89)
        self.showHelp(self.buttonTpre, "Display the pre-movement time offline in matplotlib.  \n Please select the simulation output binary file. ")


        self.buttonVideo = Button(self.frameData, text='visualize agent-based simulation output data', command=self.startVideo)
        self.buttonVideo.place(x=19, y=126)
        self.showHelp(self.buttonVideo, "Display the simulation result offline in pygame.  \n Please select the simulation output binary file. ")

        
        self.lb_outtxt = Label(self.frameData, text = 'The output txt file selected: None!  To show probablity distribution of exit selection for each agent.')
        self.lb_outtxt.place(x=19, y=206)    
            
        self.buttonExitProb = Button(self.frameData, text='Read output files and plot the door selection probablity', command=self.selectOutTxtFile_DoorProb)
        self.buttonExitProb.place(x=19, y=230)
        self.showHelp(self.buttonExitProb, "Read output files and plot the door selection probablity.")

        self.spin_exitnumber = Spinbox(self.frameData, from_=0, to=100, width=5, bd=8) 
        self.spin_exitnumber.place(x=596, y=230)
        self.showHelp(self.spin_exitnumber, "Select the exit index to show the probability.  \n The exit index starts from 0 to the number_of_exit-1. To identify the exit index, please show exit data in TestGeom. ")

                
        ##############################################
        # ============================================
        # --------------------------------------------
        # frameCSV CSV Mdoel Tool
        # --------------------------------------------
        self.lb_wf = Label(self.frameCSV, text = 'The probablity distribution of exit selection is listed in the table for each agent.')
        self.lb_wf.place(x=12, y=6)
        
        #self.scrollbar_y = Scrollbar(self.frameCSV, orient=VERTICAL)
        #self.scrollbar_x = Scrollbar(self.frameCSV, orient=HORIZONTAL)
        
        self.table_agent2exit = Treeview(self.frameCSV, height=6, show="headings", columns=('agents', 'data1', 'data2'), selectmode='extended') #, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.table_agent2exit.column('agents', width=100)
        self.table_agent2exit.column('data1', width=100)
        self.table_agent2exit.column('data2', width=150)
        self.table_agent2exit.heading('agents', text="agents")
        self.table_agent2exit.heading('data1', text="data_p")
        self.table_agent2exit.heading('data2', text="exit_prob")
        self.table_agent2exit.place(x=296, y=30)

        #self.scrollbar_y.config(command=self.table_agent2exit.yview)
        #self.scrollbar_x.config(command=self.table_agent2exit.xview)
        #self.scrollbar_y.pack(side=RIGHT, fill=Y)
        #self.scrollbar_x.pack(side=BOTTOM, fill=X)
        
        self.buttonExitProb =Button(self.frameCSV, text='View exit selection probability', command=self.readData_exitprob)
        self.buttonExitProb.place(x=13, y=30)
        #self.buttonTree.pack()
        self.showHelp(self.buttonExitProb, "Show the agent parameters for exit selection probility.")

        self.buttonPD =Button(self.frameCSV, text='View decision balace parameter', command=self.readData_p)
        self.buttonPD.place(x=13, y=60)
        self.showHelp(self.buttonPD, "Show the agent parameters for exit selection probility.")
        

        self.buttonCSVView =Button(self.frameCSV, text='View csv data file', command=self.viewCSV)
        self.buttonCSVView.place(x=13, y=90)
        self.showHelp(self.buttonCSVView, "Show the agent data in csv data file.")
        
        ##########################################################################3
        # ============================================
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
        
        self.textGuide.insert(END, 'This manual introduces a simulation tool to study complex crowd behavior in social context. The agent-based model is extended based on the well-known social force model, and it mainly describes how agents interact with each other, and also with surrounding facilities such as walls, doors and exits. The simulation platform is compatible to the FDS+Evac, and the input data in FDS+Evac could be imported into our simulation platform to create single-floor compartment geometry, and a flow solver is used to generate the egress flow field towards exits. Most importantly, we plan to integrate advanced social and psychological theory into our simulation platform, especially investigating human behavior in emergency evacuation, such as pre-evacuation behavior, exit-selection activities, social group and herding effect and so forth.  \n\nThe program mainly consists of three component: User Interface, Simulation Core, Data and Visualization Tool. \n\n')
        
        self.textGuide.insert(END, '\nAgent-based model (ABM) describes interactions among individual agents and their surroundings. In the simulation there are four types of entities: agents, walls, doors and exits.  As below we will introduce how to specify these entities.')

        self.textGuide.insert(END, '\n\n{Agents}: Agents are the core entity in computation process. They interact with each other to form collective behavior of crowd. They also interact with above types of entities to form egress motion toward exits. The resulting program is essentially a multi-agent simulation of pedestrian crowd. Each agent is modeled by extending the well-known social force model. The model is further advanced by integrating several features including pre-evacuation behavior, group behavior, way-finding behavior and so forth.')  

        self.textGuide.insert(END, '\n\n<name>: Name assigned to each agent and it is arbitrarily given by users and optionally visualized in the simulation window (pygame screen).  The names of agents are given in the first column of the data array.  Users may leave this column blank if no names are assigned.  \n\n<InitalX, InitialY>: Initial position of an agent in 2D planar space. \n\n<InitialVx, InitialVy>: Initial velocity of an agent in 2D planar space.  \n\n|tau|: Tau parameter in the social force model, or as usually called relaxation time in many-particle systems or statistical physics, and it critically affects how fast the actual velocity converges to the desired velocity.  \n\n|tpre|: Time period for pre-evacuation stage. \n\n<p>: Parameter p in opinion dynamics, and it indicates how an agent opinion decision is impacted by surrounding others, and it critically affects herding effect in collective behavior. The measurement of this parameter is within [0, 1], and an agent opinion/decision completely follow others if p=1.  In contrast, if the agent makes decision only based on his or her own opinion, the parameter p=0, and this usually implies that the agent is a leader in a group.  \n\n<pMode>: This parameter affects how parameter p is dynamically changing.  Currently there are three values to be selected: random, fixed or stress.  If random is selected, it means that parameter p is randomly generated in the interval of [0, 1].  If fixed is selected, parameter p is given by the initial value in the input csv file.  If stress is selected, then a computational model is used adapt the parameter p dynamically to surroundings.  The mode of stress has some problem and it is not used in code version 2.3.  \n\n<p2>: This parameter affects how much an agent tends to make a decision based on the information timely collected from the srrounding facilities such as the distance to the target exits or received guidance from broadcast.  The measurement of this parameter is within [0, 1], and an agent opinion/decision completely follows the received information if p2=1.  In contrast, if the agent makes decision only based on his or her past experience and the new information is completely ignored, the parameter p2=0.   \n\n<talkRange>: The range to determin when agents have opinion exchange.  Such interaction could also be understood as herding effect or group opinion dynamics, which means agents exchange opinions by talking. \n\n|aType|: The type of way-finding behaviors.  Some agents may actively search for exits while others may just follow the crowd.  In current simulation all agents follow the egress flow field, and thus this parameter is not actually used in existing version of code.  \n\n|inComp|: a boolean variable to indicate if the agent is in computation loop or not. Normally it is given true. If users want to remove an agent in simulation, they could assign it be to false for test. \n\n<talkProb>: The probability to determin if agents have opinion exchange.  Such interaction could also be understood as herding effect or agents exchange opinions by talking. \n\n|mass|: The mass of agents. \n\n<radius>: The radius of agents.'  )
        
        self.textGuide.insert(END, '\n\nThe walls, doors and exits are alternatively specified by FDS input files. Users are welcome to use existing FDS input files to create compartment geometries. In current version only one-floor crowd simulation is supported. So if there are multiple evacuation meshes in FDS input files, they should all belong to the same z interval in the vertical direction (z axis). By using FDS input files the walls are created by \&OBST, and the doors are specified by \&HOLE or \&DOOR. The exits are obtained from \&EXIT in FDS input files. If users want to find more about how FDS define a compartment area, please refer to FDS UserGuide for more information.  If users do not use FDS input files, the above entities can alternatively be specified by using csv files as introduced below.')
        
        
        self.textGuide.insert(END, '\n\n{Walls}: Walls are obstruction in a compartment geometry that confine agent movement, and they set up the boundary of a room or certain space that agents cannot go through. In our program wall are either lines or rectangular areas. If any users are interested, please feel free to extend the wall types to circular or polyangular shape. If users import walls from a FDS input file, the walls are created as a rectangular type and it corresponds to \&OBST in FDS input file.  \nIf users specify a line obstruction, it is expected to input the position of starting point and ending point of a line. If users specify a rectangular obstruction, it is expected to input the diagonal position of upper left point and lower right point of a rectangular area.')

        self.textGuide.insert(END, '\n\n<startX, startY>: One diagonal point for rectangular obstruction; Or starting point for line obstruction. \n<endX, endY>: The other diagonal point for rectangular obstruction; Or ending point for line obstruction. \n\n<arrow>: Direction assigned to the obstruction so that agents will be guided when seeing this obstruction, especially when they do not have any target door or exit. The direction implies if the obstruction provides evacuees with any egress information such as exit signs on the walls or not. The value could be +1 for positive x direction, -1 for negative x direction, +2 for positive y direction and -2 for negative y direction. If no direction is given, the value is 0. \n\n|shape|: Either rectangular or line obstruction in current program; the default mode is rectangular model. \n\n|inComp|: a boolean variable to indicate if the obstruction is in computation loop or not. Normally it is given true/1. If users want to quickly remove a obstruction in simulation, it is assigned be to false/0.')

        self.textGuide.insert(END, '\n\n{Doors and Exit}: Doors are passageways that direct agents toward certain areas, and they may be placed over a wall so that agents can get through the wall by the door. Doors can also be placed as a waypoint if not attached to any walls, and they can be considered as arrows or markers on the ground that guide agent egress movement. In brief doors affect agent way-finding activities and they help agents to form a roadmap to exits. In current program doors are only specified as rectangular object.  Exits are a special types of doors which represent paths to the safety. Thus they may be deemed as safety areas, and computation of an agent is complete when the agent reaches an exit.  An exit is usually placed over a wall like doors, but it can also be put anywhere independently without walls. In the program exits are only defined as rectangular areas. The specific features of doors and exits are given as below.')  

        self.textGuide.insert(END, '\n\n<startX, startY>: One diagonal point for rectangular door/exit. \n<endX, endY>:The other diagonal point for rectangular door/exit. \n\n|arrow|: Direction assigned to the door or exit so that agents will be guided when seeing this entity, especially when they do not have any target door or exit. The direction implies if the door or exit provides evacuees with any egress information such as exit signs or not. The value could be +1 for positive x direction, -1 for negative x direction, +2 for positive y direction and -2 for negative y direction. If no direction is given, the value is zero. Please refer to FDS+Evac manual to better understand the direction setting. \n\n|shape|: Only rectangular door or exit in current program; the default shape is rectangular door/exit.  \n\n|inComp|: a boolean variable to indicate if the door/exit is in computation loop or not. Normally it is given true/1. If users want to quickly remove a door/exit in simulation, they could assign it be to false/0 for a quick test.')
        

    # Spinbox callback 
    #def spin_exitno(self):
    #    value = self.spin_exitnumber.get()
        #print(value)
        #scr.insert(tk.INSERT, value + '\n')


    def updateCtrlParam(self):

        self.currentSimu.dumpBin = self.DumpData_Var.get()
        self.currentSimu.autoPlot = self.AutoPlot_Var.get()

        #self.currentSimu.SHOWTIME = self.SHOWTIME_Var.get()
        self.currentSimu.SHOWSTRESS = self.SHOWSTRESS_Var.get()
        
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

        if isfloatnum(self.zmin_gui.get()) and isfloatnum(self.zmax_gui.get()):
            if float(self.zmin_gui.get())<=float(self.zmax_gui.get()):
                self.currentSimu.zmin=float(self.zmin_gui.get())
                self.currentSimu.zmax=float(self.zmax_gui.get())
            else:
                self.textInformation.insert(END, 'error: zmin>zmax! Automatic data used!')
                #messagebox.showinfo('error: zmin>zmax! Automatic data used!',err) No Use because pygame has been started here!
        elif self.zmin_gui.get()!='auto' or self.zmax_gui.get()!='auto':
            self.textInformation.insert(END, 'error: zmin and zmax should be float number! Automatic data used!')
            
        if isfloatnum(self.xmin_gui.get()) and isfloatnum(self.xmax_gui.get()):
            if float(self.xmin_gui.get())<=float(self.xmax_gui.get()):
                self.currentSimu.xmin=float(self.xmin_gui.get())
                self.currentSimu.xmax=float(self.xmax_gui.get())
            else:
                self.textInformation.insert(END, 'error: xmin>xmax! Automatic data used!')
        elif self.xmin_gui.get()!='auto' or self.xmax_gui.get()!='auto':
            self.textInformation.insert(END, 'error: xmin and xmax should be float number! Automatic data used!')
                    
        if isfloatnum(self.ymin_gui.get()) and isfloatnum(self.ymax_gui.get()):
            if float(self.ymin_gui.get())<=float(self.ymax_gui.get()):
                self.currentSimu.ymin=float(self.ymin_gui.get())
                self.currentSimu.ymax=float(self.ymax_gui.get())
            else:
                self.textInformation.insert(END, 'error: ymin>ymax! Automatic data used!')
        elif self.ymin_gui.get()!='auto' or self.ymax_gui.get()!='auto':
            self.textInformation.insert(END, 'error: ymin and ymax should be float number! Automatic data used!')

        if isfloatnum(self.dtSim_gui.get()) and isfloatnum(self.dtDump_gui.get()):
            self.currentSimu.DT=float(self.dtSim_gui.get())
            self.currentSimu.DT_DumpData=float(self.dtDump_gui.get())
        else:
            self.textInformation.insert(END, 'error: dtAtt and dtExit should be float number! Default data used!')

        if isfloatnum(self.dtAtt_gui.get()) and isfloatnum(self.dtExit_gui.get()):
            self.currentSimu.DT_OtherList=float(self.dtAtt_gui.get())
            self.currentSimu.DT_ChangeDoor=float(self.dtExit_gui.get())
        else:
            self.textInformation.insert(END, 'error: dtAtt and dtExit should be float number! Default data used!')
                
        if isintnum(self.nxp_gui.get()):
            self.currentSimu.xpt=int(self.nxp_gui.get())
        else:
            self.textInformation.insert(END, 'error: x point number should be integer! Automatic data used!')
            
        if isintnum(self.nyp_gui.get()):
            self.currentSimu.ypt=int(self.nyp_gui.get())
        else:
            self.textInformation.insert(END, 'error: y point number should be integer! Automatic data used!')

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
        self.fname_FDS = tkf.askopenfilename(filetypes=(("fds files", "*.fds"),("All files", "*.*")),initialdir=self.currentdir)
        #temp=re.split(r'/', self.fname_FDS)
        #temp=self.fname_FDS.split('/')
        temp=os.path.basename(self.fname_FDS)
        self.lb_fds.config(text = "Optional: If fds is selected, the compartment geometry is created by .fds file. \n"+"The FDS data file selected: "+str(self.fname_FDS)+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_FDS:', self.fname_FDS)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'FDS Input File Selected:   '+self.fname_FDS+'\n')

    def selectEvacFile(self):
        self.fname_EVAC = tkf.askopenfilename(filetypes=(("csv files", "*.csv"),("All files", "*.*")),initialdir=self.currentdir)
        #temp=self.fname_EVAC.split('/') 
        temp=os.path.basename(self.fname_EVAC)
        self.currentdir = os.path.dirname(self.fname_EVAC)
        self.lb_csv.config(text = "The input csv file selected: "+str(self.fname_EVAC)+"\n")
        #self.textInformation.insert(END, 'fname_EVAC:   '+self.fname_EVAC)
        print('fname', self.fname_EVAC)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'EVAC Input File Selected:   '+self.fname_EVAC+'\n')
        self.currentdir = os.path.dirname(self.fname_EVAC)

    def selectOutTxtFile_DoorProb(self):
        #tempdir=os.path.dirname(self.fname_EVAC)
        #print(tempdir)
        self.fname_OutTXT = tkf.askopenfilename(filetypes=(("txt files", "*.txt"),("All files", "*.*")),\
        initialdir=self.currentdir)
        temp=re.split(r'/', self.fname_OutTXT)
        #temp=self.fname_OutTXT.split('/') 
        self.lb_outtxt.config(text = "The output txt file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_outTxtFile:', self.fname_OutTXT)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'Output txt File Selected:   '+self.fname_OutTXT+'\n')
        exitNum = self.spin_exitnumber.get()
        print('Exit index in plot:', exitNum)
        readDoorProb(self.fname_OutTXT, int(exitNum))

    def selectOutBinFile_Tpre(self):
        #tempdir=os.path.dirname(self.fname_EVAC)
        #print(tempdir)
        self.fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("All files", "*.*")),\
        initialdir=self.currentdir)
        temp=re.split(r'/', self.fname_OutBIN)
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_outBinFile:', self.fname_OutBIN)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'Output binary File Selected:   '+self.fname_OutBIN+'\n')
        visualizeTpre(self.fname_OutBIN)

    def selectOutNPZ(self):
        tempdir=os.path.dirname(self.fname_EVAC)
        self.fname_OutNPZ = os.path.join(tempdir, "vel_flow1.npz")
        self.fname_OutNPZ = tkf.askopenfilename(filetypes=(("npz files", "*.npz"),("All files", "*.*")),\
        initialdir=os.path.dirname(self.fname_EVAC))
        temp=re.split(r'/', self.fname_OutNPZ)
        #temp=self.fname_OutNPZ.split('/') 
        #self.lb_outnpz.config(text = "The output npz file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_outNPZ_File:', self.fname_OutNPZ)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'Output npz File Selected:   '+self.fname_OutNPZ+'\n')
        visualizeCrowdfluid(self.fname_OutNPZ)

    def readData_exitprob(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        for i in range(self.currentSimu.num_agents):
            #for j in range(self.currentSimu.num_exits):
            self.table_agent2exit.insert('', i, values=(self.currentSimu.agents[i].ID, self.currentSimu.agents[i].p, self.currentSimu.agent2exit[i,:]))
        self.textInformation.insert(END, '\n'+'agent2exit data: \n '+str(self.currentSimu.agent2exit)+'\n')

    def readData_p(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        pArray=[]
        #for i in range(self.currentSimu.num_agents):
        for i in range(self.currentSimu.num_agents):
            #for j in range(self.currentSimu.num_exits):
            self.table_agent2exit.insert('', index='end', text=(self.currentSimu.agents[i].ID, self.currentSimu.agents[i].p))
        for idai, ai in enumerate(self.currentSimu.agents):
            #for j in range(self.currentSimu.num_exits):
            #pArray.append(self.currentSimu.agents[i].p)
            pArray.append(ai.p)
        self.textInformation.insert(END, '\n'+'decision parameter p: \n '+str(pArray)+'\n')


    def viewCSV(self):
        print(os.path.join(self.fname_EVAC))
        os.system('et.exe.lnk '+ os.path.join(self.fname_EVAC))

    #def deleteGeom(self):
    #    self.currentSimu = None

    def testGeom(self):
        #if self.currentSimu is None:
        self.currentSimu = simulation()
        #self.currentSimu.ZOOMFACTOR = ZOOM
        #self.currentSimu.xSpace=xSpa
        #self.currentSimu.ySpace=ySpa
        if self.UseFDS_Var.get():
            self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        else:
            self.currentSimu.select_file(self.fname_EVAC, None, "non-debug")
        self.currentSimu.preprocessAgent()
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
            if len(self.currentSimu.exits)>0 and self.currentSimu.solver!=0:
                self.currentSimu.buildMesh()
                self.currentSimu.flowMesh()
                self.currentSimu.computeDoorDirection()
            else:
                self.currentSimu.solver=0
            #if self.currentSimu.solver!=0:
                #show_flow(self.currentSimu)
            self.currentSimu.dataSummary()
            sunpro1 = mp.Process(target=show_simu(self.currentSimu))
            #sunpro1 = mp.Process(target=self.currentSimu.flowMesh())
            sunpro1.start()
            sunpro1.join()

        #show_geom(myTest)
        #myTest.show_simulation()
        #self.currentSimu.quit()

    def testFlow(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            #self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            if self.UseFDS_Var.get():
                self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            else:
                self.currentSimu.select_file(self.fname_EVAC, None, "non-debug")
        show_geom(self.currentSimu)
        #sunpro2 = mp.Process(target=show_geom(self.currentSimu)) 
        #sunpro2.start()
        #sunpro2.join()
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        #try:
        self.currentSimu.buildMesh()
        self.currentSimu.flowMesh()
        self.currentSimu.computeDoorDirection()
        #except:
        #    input("At least one exit should be placed in the layout! Please check!")
        show_flow(self.currentSimu)

    # Compute the numerical result and display the result timely in pygame
    def startSim(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            #self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            if self.UseFDS_Var.get():
                self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            else:
                self.currentSimu.select_file(self.fname_EVAC, None, "non-debug")
        #self.textInformation.insert(END, "Start Simulation Now!")
        self.setStatusStr("Simulation starts!  GUI window is not effective when Pygame screen is displayed!")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        if len(self.currentSimu.exits)>0 and self.currentSimu.solver!=0:
            self.currentSimu.buildMesh()
            self.currentSimu.flowMesh()
            self.currentSimu.computeDoorDirection()
        else:
            self.currentSimu.solver=0
        #if self.currentSimu.solver!=0:
        #    show_flow(self.currentSimu)
        self.currentSimu.dataSummary()
        sunpro1 = mp.Process(target=show_simu(self.currentSimu))        
        sunpro1.start()
        sunpro1.join()
        self.setStatusStr("Simulation not yet started!")
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()
    
    # Only compute the numerical result without displaying in pygame
    def compSim(self):
        if self.currentSimu is None:
            self.currentSimu = simulation()
            #self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            if self.UseFDS_Var.get():
                self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
            else:
                self.currentSimu.select_file(self.fname_EVAC, None, "non-debug")
        #self.textInformation.insert(END, "Start Simulation Now!")
        self.setStatusStr("Simulation starts!  GUI window is not effective now")
        self.updateCtrlParam()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        if len(self.currentSimu.exits)>0:
            self.currentSimu.buildMesh()
            self.currentSimu.flowMesh()
            self.currentSimu.computeDoorDirection()
        else:
            self.currentSimu.solver=0
        self.currentSimu.dataSummary()
        sunpro1 = mp.Process(target=compute_simu(self.currentSimu))        
        sunpro1.start()
        #sunpro1.join()
        self.setStatusStr("Simulation not yet started!")
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()

    # Only compute the numerical result without displaying in pygame
    def startVideo(self):

        self.fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("npz files", "*.npz"),("All files", "*.*")),\
        initialdir=self.currentdir)
        
        FN_Temp = os.path.join(self.currentdir, "config.txt")
        if os.path.exists(FN_Temp):
            for line in open(FN_Temp, "r"):
                if re.match('ZOOM', line):
                    temp =  line.split('=')
                    self.ZOOM = float(temp[1].strip())                    
                if re.match('xSpace', line):
                    temp =  line.split('=')
                    self.xSpa = float(temp[1].strip())
                if re.match('ySpace', line):
                    temp =  line.split('=')
                    self.ySpa = float(temp[1].strip())
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('Output data file selected:', self.fname_OutBIN)
        self.setStatusStr("Visualizing Simulation Data!")
        self.textInformation.insert(END, '\n'+'Output Data File Selected:   '+self.fname_OutBIN+'\n')
        temp= self.fname_OutBIN.split('.')
        if temp[1]=='bin':
            if self.UseFDS_Var.get():
                visualizeEvac(self.fname_OutBIN, self.fname_EVAC, self.fname_FDS, self.ZOOM, self.xSpa, self.ySpa)
            else:
                visualizeEvac(self.fname_OutBIN, self.fname_EVAC, None, self.ZOOM, self.xSpa, self.ySpa)
        if temp[1]=='npz':
            if self.UseFDS_Var.get():
                show_agents_npz(self.fname_OutBIN, self.fname_EVAC, self.fname_FDS, self.ZOOM, self.xSpa, self.ySpa)
            else:
                show_agents_npz(self.fname_OutBIN, self.fname_EVAC, None, self.ZOOM, self.xSpa, self.ySpa)

def isfloatnum(aString):
    try:
        float(aString)
        return True
    except:
        return False

def isintnum(aString):
    try:
        int(aString)
        return True
    except:
        return False
        
#==========================================
#===This is a small GUI widget used for debug mode=======
#==========================================
def startPage(FN_FDS=None, FN_EVAC=None):

    #FN_FDS=None  #'1'
    #FN_EVAC=None  #'2'
    #FN_Doors=None  #'3'
    currentdirname = os.path.dirname(FN_EVAC)
    
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
        FN[index] = tkf.askopenfilename(filetypes=(("csv files", "*.csv"),("fds files", "*.fds"),\
        ("All files", "*.*")), initialdir=currentdirname)
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


    
