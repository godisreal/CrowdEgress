
import os
from sys import argv, exit
from simulation import *

print("================================")
print ("Length of input parameters:", len(argv))
print("================================")

if len(argv)==2:
    file1 = argv[1]
    if file1 == '-help':
        print ('Show help info in readme.txt!')
        exit(-1)
    elif file1:
        if os.path.exists(file1):
            print ('load evac .csv file ',file1)
        else:
            print ("Input file %s does not exit!" %file1)
            exit(-1)

    myTest = simulation()
    myTest.select_file(file1, None, 'no-debug')
    #myTest.read_data()
    show_geom(myTest)
    myTest.preprocessGeom()
    myTest.preprocessAgent()

    if myTest.continueToSimu:
        show_simu(myTest)

if len(argv)==3:
    file1 = argv[1]
    file2 = argv[2]

    if file1 == '-help':
        print ('Show help info in readme.txt!')
        exit(-1)
    elif file1:
        if os.path.exists(file1):
            print ('load evac .csv file ',file1)
        else:
            print ("Input file %s does not exit!" %file1)
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
    myTest.preprocessGeom()
    myTest.preprocessAgent()

    if myTest.continueToSimu:
        show_simu(myTest)

if len(argv)>3:
    print("Too many input parameters!")
    exit(-1)

    
