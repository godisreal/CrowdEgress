
import os, sys
import Tkinter as tk
#import Tkinter.Filedialog
#from Tkinter import Tk
from Tkinter import *
#from Tkinter import Filedialog
import tkFileDialog

def startPage(FN_FDS=None, FN_EVAC=None):

    #FN_FDS=None  #'1'
    #FN_EVAC=None  #'2'
    #FN_Doors=None  #'3'

    FN_Info = ['FDS', 'EVAC'] #, 'Doors']
    FN=[None, None] #, None]
    FN[0]=FN_FDS
    FN[1]=FN_EVAC

    window = tk.Tk()
    window.title('my window')
    window.geometry('760x300')

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

    C1=tk.Checkbutton(window, text= 'Show Instruction Page', variable=CheckVar1, onvalue=1, offvalue=0)
    #C2=tk.Checkbutton(window, text= 'Use Group Force', variable=CheckVar2, onvalue=1, offvalue=0)
    C1.pack()
    #C2.pack()

    lb_guide = tk.Label(window,text =  "Please select the input files of the simulation\n" + "Geom: Use .fds or .csv  Evac: Use .csv")
    lb_guide.pack()

    lb0 = tk.Label(window,text =  "The FDS data file selected: "+str(FN[0])+"\n")
    lb0.pack()

    lb1 = tk.Label(window,text =  "The EVAC data file selected: "+str(FN[1])+"\n")
    lb1.pack()

    #lb2 = tk.Label(window,text =  "The exit data file selected: "+str(FN[2])+"\n")
    #lb2.pack()

    tk.Button(window, text='choose csv file for FDS data', command=lambda: selectFile(0)).pack()
    #FN_Agents = fname
    tk.Button(window, text='choose csv file for EVAC data', command=lambda: selectFile(1)).pack()
    #FN_Walls = fname
    #tk.Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()
    #FN_Doors = fname

    tk.Button(window, text='start now: read in data', command=window.quit).pack()
    #tkButton.place(x=5,y=220)
    #print FN_Agents, FN_Walls, FN_Doors
    print FN[0], FN[1] #, FN[2]

    window.mainloop()

    #print FN['Agents'], FN['Walls'], FN['Doors']
    print FN[0], FN[1] #, FN[2]

    #FN_FDS = FN[0]
    #FN_EVAC = FN[1]

    return FN

if __name__ == '__main__':
    startPage()

    
