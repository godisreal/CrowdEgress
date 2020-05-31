

#import Tkinter as tk
#import Tkinter.Filedialog
#from Tkinter import Tk
#from Tkinter import Filedialog
#import tkFileDialog

import os, sys

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    import tkFileDialog
    
class ctrlVar(object):

        def __init__(self, fileName=None):

            # Below are global variables to set up the simulation
            ################################################################
            self.TIMECOUNT = True
            self.THREECIRCLES = False  	# Use 3 circles to draw agents

            self.PAUSE = False
            self.MODETRAJ = False        # Draw trajectory of agents' movement
            
            self.GROUPBEHAVIOR = True       # Enable the group social force
            self.SELFREPULSION = False	# Enable self repulsion
            self.WALLBLOCKHERDING = True
            self.TPREMODE = 3        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 

            self.SHOWVELOCITY = True	# Show velocity and desired velocity of agents
            self.SHOWINDEX = True        # Show index of agents
            self.SHOWTIME = True         # Show a clock on the screen
            self.SHOWINTELINE = True     # Draw a line between interacting agents
            self.SHOWSTRESS = False
            self.SHOWWALLDATA = True
            self.SHOWDOORDATA = True
            self.SHOWEXITDATA = True
            self.DRAWWALLFORCE = True
            self.DRAWDOORFORCE = True
            self.DRAWGROUPFORCE = False
            self.DRAWPHYSICALFORCE = False
            self.DRAWSELFREPULSION = False
            self.DRAWMOTIVEFORCE = False
            
            self.TESTMODE = False #True
            self.TESTFORCE = False
            #self.GUI = True
            #self.STARTPAGE = False

            self.ZOOMFACTOR = 20.0
            self.xSpace=10.0
            self.ySpace=10.0
            
            if fileName is not None and os.path.exists(fileName):
                for line in open(fileName, "r"):
                    if re.match('TIMECOUNT', line):
                        temp =  line.split('=')
                        self.TIMECOUNT = int(temp[1].strip())
                    if re.match('THREECIRCLES', line):
                        temp =  line.split('=')
                        self.THREECIRCLES = int(temp[1].strip())
                    if re.match('SHOWVELOCITY', line):
                        temp =  line.split('=')
                        self.SHOWVELOCITY = int(temp[1].strip())
                    if re.match('SHOWINDEX', line):
                        temp =  line.split('=')
                        self.SHOWINDEX = int(temp[1].strip())


import os, sys
import multiprocessing as mp
from simulation import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    import tkFileDialog
    
class GUI(object):

    def __init__(self, FN_FDS=None, FN_EVAC=None):

        #self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        #self.FN=[None, None] #, None]
        #self.FN[0]=FN_FDS
        #self.FN[1]=FN_EVAC

        self.fname_FDS = FN_FDS
        self.fname_EVAC = FN_EVAC
        self.currentSimu = None
        
        self.window = Tk()
        self.window.title('crowd egress simulator')
        self.window.geometry('760x300')

        self.notebook = Notebook(self.window)      
        self.notebook.pack(side=TOP, padx=2, pady=2)
        
        # added "self.rootWindow" by Hiroki Sayama 10/09/2018
        self.frameRun = Frame(self.window)
        #self.frameSettings = Frame(self.window)
        self.frameParameters = Frame(self.window)
        self.frameInformation = Frame(self.window)


        self.notebook.add(self.frameRun,text="RunSimulation")
        #self.notebook.add(self.frameSettings,text="Settings")
        self.notebook.add(self.frameParameters,text="Parameters")
        self.notebook.add(self.frameInformation,text="Information")
        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
        # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02
        
        #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        #from Tkinter.tkFileDialog import askopenfilename
        #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
        #def quit_botton(event):

        self.lb_guide = Label(self.frameRun, text =  "Please select the input files of the simulation\n" + "Use a single .csv  file to create compartment geometry and agents\n" + "Please check the examples for details")
        self.lb_guide.pack()

        self.lb1 = Label(self.frameRun,text =  "The input .csv file selected: "+str(self.fname_EVAC)+"\n")
        self.lb1.pack()

        self.lb0 = Label(self.frameRun,text =  "Optional: If .fds is selected, the compartment geometry is created by .fds file. \n"  "The FDS file selected: "+str(self.fname_FDS)+"\n")
        self.lb0.pack()

        #self.lb2 = Label(frameRun,text =  "The exit data file selected: "+str(FN[2])+"\n")
        #self.lb2.pack()

        self.buttonSelectFDS =Button(self.frameRun, text='choose fds file for FDS data', command=self.selectFDSFile)
        self.buttonSelectFDS.pack()
        self.buttonSelectCSV =Button(self.frameRun, text='choose csv file for EVAC data', command=self.selectEvacFile)
        self.buttonSelectCSV.pack()
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        
        #self.buttonRead = Button(self.frameRun, text='read now: read in data', command=self.readData)
        #self.buttonRead.pack()
        #self.buttonGeom = Button(self.frameRun, text='read now: test geom', command=self.testGeom)
        #self.buttonGeom.pack()
        
        self.buttonStart = Button(self.frameRun, text='start now: start simulation', command=self.startSim)
        self.buttonStart.pack()
        #buttonStart.place(x=5,y=220)
        print self.fname_FDS, self.fname_EVAC

        timeVar = IntVar()
        timeVar.set(0)
        self.CB1=Checkbutton(self.frameParameters, text= 'Show Time in Simulation', variable=timeVar, onvalue=1, offvalue=0)
        self.CB1.pack(side=TOP, padx=2, pady=2)

        # --------------------------------------------
        # frameInformation
        # --------------------------------------------
        scrollInfo = Scrollbar(self.frameInformation)
        self.textInformation = Text(self.frameInformation, width=45,height=13,bg='lightgray',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textInformation.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollInfo.config(command=self.textInformation.yview)
        self.textInformation.config(yscrollcommand=scrollInfo.set)


    def start(self):
        self.window.mainloop()

    def selectFDSFile(self):
        self.fname_FDS = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        self.lb0.config(text = "The FDS data file selected: "+str(self.fname_FDS)+"\n")
        print 'fname_FDS:', self.fname_FDS

    def selectEvacFile(self):
        self.fname_EVAC = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        self.lb1.config(text = "The EVAC data file selected: "+str(self.fname_EVAC)+"\n")
        print 'fname', self.fname_EVAC

    #def readData(self):
    #    self.currentSimu = simulation()
    #    self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-gui")
    #    #myTest.read_data()

    def testGeom(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-gui")
        sunpro1 = mp.Process(target=show_geom(self.currentSimu))        
        sunpro1.start()
        sunpro1.join()
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()

    def startSim(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-gui")
        self.textInformation.insert(END, "Start Simulation Now!")
        #self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        sunpro1 = mp.Process(target=show_simu(self.currentSimu))        
        sunpro1.start()
        sunpro1.join()
        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()

        
    
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
    frameParameters = Frame(window)
    frameInformation = Frame(window)


    notebook.add(frameRun,text="Run")
    notebook.add(frameParameters,text="Parameters")
    notebook.add(frameInformation,text="Info")
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
        FN[index] = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        if index ==0:
            lb0.config(text = "Optional: The fds file selected: "+str(FN[index])+"\n")
        elif index ==1:
            lb1.config(text = "The input csv file selected: "+str(FN[index])+"\n")
        #elif index ==2:
        #    lb2.config(text = "The exit data file selected: "+str(FN[index])+"\n")
        print 'fname', FN[index]

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
    print FN[0], FN[1] #, FN[2]

    window.mainloop()

    #print FN['Agents'], FN['Walls'], FN['Doors']
    print FN[0], FN[1] #, FN[2]
    #print TestV

    #FN_FDS = FN[0]
    #FN_EVAC = FN[1]

    return FN

if __name__ == '__main__':
    myGUI=GUI()
    myGUI.start()


    
