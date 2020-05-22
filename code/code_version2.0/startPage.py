

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
    startPage()


    
