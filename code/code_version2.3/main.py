#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================
# 
# DESCRIPTION:
# This software is part of a python library to assist in developing and
# analyzing evacuation simulation results from Fire Dynamics Simulator with Evacuation (FDS+Evac).
# FDS+Evac is an open source software package developed by NIST. The source
# code is available at: https://github.com/firemodels/fds
#

import os, logging
from sys import argv, exit
from simulation import *

# Try logging stuff!
# May not be used in practial compuation! 
logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

print("================================")
print ("Length of input parameters:", len(argv))
print("================================")

# python [filename.csv]
if len(argv)==2:
    file1 = argv[1]
    if file1:
        if os.path.exists(file1):
            print ('load evac .csv file ',file1)
        else:
            print ("Input file %s does not exit!" %file1)
            print ("Or please use parameter -help to show readme.txt!  Thanks for using this program!")
            exit(-1)
    else:
        print ('Show help info in readme.txt!')
        if os.path.exists("readme.txt"):
            for line in open("readme.txt"):
                print (line)
        else:
            print ("The file readme.txt is not in this folder.")
            print ("Please search readme.txt in other folders, and read it first!")
        exit(-1)
        
        
    myTest = simulation()
    myTest.select_file(file1, None, 'no-debug')
    #myTest.read_data()
    show_geom(myTest)
    
    #myTest.preprocessGeom()
    #myTest.preprocessAgent()
    #myTest.buildMesh()
    #myTest.flowMesh()
    #myTest.computeDoorDirection()
    
    #if myTest.continueToSimu:
    #    show_flow(myTest)
    #    show_simu(myTest)
        
    if myTest.continueToSimu:
        myTest.readconfig()
        myTest.preprocessGeom()
        myTest.preprocessAgent()
        if myTest.solver == 1 or myTest.solver == 2:
            myTest.buildMesh()
            myTest.flowMesh()
            myTest.computeDoorDirection()
            show_flow(myTest)
            
        myTest.dataSummary()
        show_simu(myTest)
    else:
        os.remove(myTest.outDataName + ".txt")
        

# python [filename.csv] [filename.fds]
if len(argv)==3:
    file1 = argv[1]
    file2 = argv[2]

    if file1:
        if os.path.exists(file1):
            print ('load evac .csv file ',file1)
        else:
            print ("Input file %s does not exit!" %file1)
            print ("Or please use parameter -help to show readme.txt!  Thanks for using this program!")
            exit(-1)
    else:
        print ('Show help info in readme.txt!')
        if os.path.exists("readme.txt"):
            for line in open("readme.txt"):
                print (line)
        else:
            print ("The file readme.txt is not in this folder.")
            print ("Please search readme.txt in other folders, and read it first!")
        exit(-1)

    if file2:
        if os.path.exists(file2):
            print ('load evac .fds file ',file2)
        else:
            print ("Input file %s does not exit!" %file2)
            exit(-1)
            
    myTest = simulation()
    myTest.select_file(file1, file2, 'no-debug')
    #myTest.read_data()
    show_geom(myTest)
    
    
    #myTest.preprocessGeom()
    #myTest.preprocessAgent()

    #myTest.buildMesh()
    #myTest.flowMesh()
    #myTest.computeDoorDirection()
    
    #if myTest.continueToSimu:
    #    show_flow(myTest)
    #    show_simu(myTest)

    if myTest.continueToSimu:
        myTest.readconfig()
        myTest.preprocessGeom()
        myTest.preprocessAgent()
        if myTest.solver == 1 or myTest.solver == 2:
            myTest.buildMesh()
            myTest.flowMesh()
            myTest.computeDoorDirection()
            show_flow(myTest)
        myTest.dataSummary()
        show_simu(myTest)
    else:
        os.remove(myTest.outDataName + ".txt")

if len(argv)>3:
    print("Too many input parameters! Please read readme.txt first! Thanks for using this program!")
    exit(-1)

    
