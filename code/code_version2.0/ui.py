
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

        self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        self.FN=[None, None] #, None]
        self.FN[0]=FN_FDS
        self.FN[1]=FN_EVAC

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


        self.notebook.add(self.frameRun,text="Run")
        #self.notebook.add(self.frameSettings,text="Settings")
        self.notebook.add(self.frameParameters,text="Parameters")
        self.notebook.add(self.frameInformation,text="Info")
        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
        # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02
        
        #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        #from Tkinter.tkFileDialog import askopenfilename
        #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
        #def quit_botton(event):

        self.lb_guide = Label(self.frameRun, text =  "Please select the input files of the simulation\n" + "Geom: Use .fds or .csv  Evac: Use .csv")
        self.lb_guide.pack()

        self.lb0 = Label(self.frameRun,text =  "The FDS data file selected: "+str(self.FN[0])+"\n")
        self.lb0.pack()

        self.lb1 = Label(self.frameRun,text =  "The EVAC data file selected: "+str(self.FN[1])+"\n")
        self.lb1.pack()

        #self.lb2 = Label(frameRun,text =  "The exit data file selected: "+str(FN[2])+"\n")
        #self.lb2.pack()

        self.buttonSelectFDS =Button(self.frameRun, text='choose fds file for FDS data', command=lambda: self.selectFile(0)).pack()
        self.buttonSelectCSV =Button(self.frameRun, text='choose csv file for EVAC data', command=lambda: self.selectFile(1)).pack()
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()

        self.buttonStart = Button(self.frameRun, text='start now: read in data', command=self.startSim).pack()
        #buttonStart.place(x=5,y=220)
        print self.FN[0], self.FN[1]


    def start(self):
        self.window.mainloop()

    def selectFile(self, index):
        self.FN[index] = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        if index ==0:
            self.lb0.config(text = "The FDS data file selected: "+str(self.FN[index])+"\n")
        elif index ==1:
            self.lb1.config(text = "The EVAC data file selected: "+str(self.FN[index])+"\n")
        #elif index ==2:
        #    lb2.config(text = "The exit data file selected: "+str(FN[index])+"\n")
        print 'fname', self.FN[index]

    def startSim(self):
        myTest = simulation()
        myTest.select_file(self.FN[1], None, "non-gui")
        #myTest.read_data()
        sunpro1 = mp.Process(target=show_simu(myTest))
        sunpro1.start()
        sunpro1.join()
        #show_geom(myTest)
        #myTest.show_simulation()
        #myTest.quit()
            
    
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
        FN[index] = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        if index ==0:
            lb0.config(text = "The FDS data file selected: "+str(FN[index])+"\n")
        elif index ==1:
            lb1.config(text = "The EVAC data file selected: "+str(FN[index])+"\n")
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

    lb0 = Label(frameRun,text =  "The FDS data file selected: "+str(FN[0])+"\n")
    lb0.pack()

    lb1 = Label(frameRun,text =  "The EVAC data file selected: "+str(FN[1])+"\n")
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


    
