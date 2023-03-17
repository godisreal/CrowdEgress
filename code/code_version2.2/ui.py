
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

        self.fname_FDS = FN_FDS
        self.fname_EVAC = FN_EVAC
        self.currentSimu = None
        
        self.window = Tk()
        self.window.title('crowd egress simulator')
        self.window.geometry('700x420')

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
        #self.buttonSelectCSV.place(x=2, y=120)
        self.buttonSelectCSV.pack()
        self.showHelp(self.buttonSelectCSV, "Select .csv file to set up the agent and exit for the simulation")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        self.buttonSelectFDS =Button(self.frameRun, text='choose fds file for FDS data', command=self.selectFDSFile)
        #self.buttonSelectFDS.place(x=2, y=60)
        self.buttonSelectFDS.pack()
        self.showHelp(self.buttonSelectFDS, "Select FDS file to set up the compartment geometry for the simulation")
        
        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        
        #self.buttonRead = Button(self.frameRun, text='read now: read in data', command=self.readData)
        #self.buttonRead.pack()
        self.buttonGeom = Button(self.frameRun, text='read now: test geom', command=self.testGeom)
        self.buttonGeom.pack()

        self.buttonFlow = Button(self.frameRun, text='read now: test flow', command=self.testFlow)
        self.buttonFlow.pack()
        
        self.buttonStart = Button(self.frameRun, text='start now: start simulation', command=self.startSim)
        self.buttonStart.pack()
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
        self.SHOWSTRESS_Var.set(1)
        self.SHOWSTRESS_CB=Checkbutton(self.frameParameters, text= 'Show Stress Level in Simulation', variable=self.SHOWSTRESS_Var, onvalue=1, offvalue=0)
        #self.SHOWSTRESS_CB.pack(side=TOP, padx=2, pady=2)
        self.SHOWSTRESS_CB.place(x=2, y=36)
        self.showHelp(self.SHOWSTRESS_CB, "Show agents' stress level data in the simulation.  Try to press key <S> in pyagme screen!")

        self.SHOWGEOM_Var = IntVar()
        self.SHOWGEOM_Var.set(1)
        self.SHOWGEOM_CB=Checkbutton(self.frameParameters, text= 'Show compartment data in simulation', variable=self.SHOWGEOM_Var, onvalue=1, offvalue=0)
        #self.SHOWGEOM_CB.pack(side=TOP, padx=2, pady=2)
        self.SHOWGEOM_CB.place(x=300, y=6)
        self.showHelp(self.SHOWGEOM_CB, "Show compartment geometry data in the simulation.")

        self.SHOWFORCE_Var = IntVar()
        self.SHOWFORCE_Var.set(1)
        self.SHOWFORCE_CB=Checkbutton(self.frameParameters, text= 'Show forces on agents in simulation', variable=self.SHOWFORCE_Var, onvalue=1, offvalue=0)
        self.SHOWFORCE_CB.place(x=2, y=66)
        self.showHelp(self.SHOWFORCE_CB, "Show various forces on agents in the simulation.")

        #print self.SHOWTIME_Var.get()

        # --------------------------------------------
        # frameInformation
        # --------------------------------------------
        scrollInfo = Scrollbar(self.frameInformation)
        self.textInformation = Text(self.frameInformation, width=45,height=13,bg='lightgray',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textInformation.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollInfo.config(command=self.textInformation.yview)
        self.textInformation.config(yscrollcommand=scrollInfo.set)
        

    def updateCtrlParam(self):
        self.currentSimu.SHOWTIME = self.SHOWTIME_Var.get()
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

    def testGeom(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        sunpro2 = mp.Process(target=show_geom(self.currentSimu)) 
        sunpro2.start()
        #sunpro2.join()
        if self.currentSimu.continueToSimu:
            self.currentSimu.flowMesh()
            self.currentSimu.preprocessGeom()
            self.currentSimu.preprocessAgent()
            self.updateCtrlParam()
            sunpro1 = mp.Process(target=show_simu(self.currentSimu))
            #sunpro1 = mp.Process(target=self.currentSimu.flowMesh())
            sunpro1.start()
            #sunpro1.join()

        #show_geom(myTest)
        #myTest.show_simulation()
        self.currentSimu.quit()

    def testFlow(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        show_geom(self.currentSimu)
        #sunpro2 = mp.Process(target=show_geom(self.currentSimu)) 
        #sunpro2.start()
        #sunpro2.join()
        self.currentSimu.flowMesh()

    def startSim(self):
        self.currentSimu = simulation()
        self.currentSimu.select_file(self.fname_EVAC, self.fname_FDS, "non-debug")
        #self.textInformation.insert(END, "Start Simulation Now!")
        self.setStatusStr("Simulation starts!  GUI window is not effective when Pygame screen is displayed!")
        self.updateCtrlParam()
        self.currentSimu.flowMesh()
        self.currentSimu.preprocessGeom()
        self.currentSimu.preprocessAgent()
        sunpro1 = mp.Process(target=show_simu(self.currentSimu))        
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


    
