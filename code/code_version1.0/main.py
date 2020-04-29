# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import pygame
import pygame.draw
import numpy as np
from agent_model_obst3 import *
from obst import *
#from passage import *
from math_func import *
#from color_func import *
from data_func import *
from math import *
#from config import *
import re
import random
#from random import *
#import csv
#from readCSV import *
from ctypes import *
from draw_geom import *
#from startPage import *
import os

#from pygame.locals import *
#from sys import exit

# Below are variables for users to set up pygame features
################################################################
SCREENSIZE = [800, 400]
RESOLUTION = 180
#BACKGROUNDCOLOR = [255,255,255]
LINEWIDTH = 2
AGENTSIZE = 6
ZOOMFACTOR = 20.0
DT = 0.3
DT_OtherList = 3.0
#WALLSFILE = "walls.csv"
#AGENTCOLOR = [0,0,255]

xSpace=10.0
ySpace=10.0
xyShift = np.array([xSpace, ySpace])

# Below are global variables to set up the simulation
################################################################
TIMECOUNT = True
THREECIRCLES = False  	# Use 3 circles to draw agents
SHOWVELOCITY = True	# Show velocity and desired velocity of agents
SHOWINDEX = True        # Show index of agents
SHOWTIME = True         # Show a clock on the screen
SHOWINTELINE = True     # Draw a line between interacting agents
MODETRAJ = False        # Draw trajectory of agents' movement
COHESION = False	    # Enable the group social force
SELFREPULSION = False	# Enable self repulsion
WALLBLOCKHERDING = True
TPREMODE = 3        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 
PAUSE = False
SHOWWALLDATA = True
SHOWDOORDATA = True
SHOWEXITDATA = True
TESTFORCE = False
SHOWSTRESS = False
DRAWWALLFORCE = True
DRAWDOORFORCE = True
DRAWGROUPFORCE = False
DRAWSELFREPULSION = False
GROUPBEHAVIOR = False
TESTMODE = False #True
#STARTPAGE = False

# No Need to Use StartPage
#if STARTPAGE:
#     startPage(SCREENSIZE)

#agentFeatures = readCSV("agentData2018.csv", 'string')
#[Num_Agents, Num_Features] = np.shape(agentFeatures)
#print >> f, 'Number of Agents:', Num_Agents, '\n'
#print >> f, "Features of Agents\n", agentFeatures, "\n"

## ======  Read in Data from .CSV File or .FDS File =======
## =============  Check Data ====================
## =============  This is an important step ============

inputDataCorrect = True
#FN_EVAC = 'tpre2020-1.csv' #'newDataForm2017.csv'  # 
#FN_FDS = 'Ex2017.fds'
#FN_FDS = 'TPRE_DET2.fds'
#FN_FDS = None

FN_FDS=None
FN_EVAC =None

if os.path.exists("outData.txt"):
    for line in open("outData.txt", "r"):
        if re.match('FN_FDS', line):
            temp =  line.split('=')
            FN_FDS = temp[1].strip()
        if re.match('FN_EVAC', line):
            temp =  line.split('=')
            FN_EVAC = temp[1].strip()

if TESTMODE: 
    print FN_FDS
    print FN_EVAC
    print "As above is the input file selected in your last run!"
    raw_input('Input File Selection from Last Run.')

from startPage import*
[FN_FDS, FN_EVAC] = startPage(FN_FDS, FN_EVAC)

# The file to record the some output data of simulation
f = open("outData.txt", "w+")

print >> f, 'FN_FDS=', FN_FDS
print >> f, 'FN_EVAC=', FN_EVAC #,'\n'

###  Read in Data from .CSV File ###
agents = readAgents(FN_EVAC)
exits = readExits(FN_EVAC)

Num_Agents = len(agents)
Num_Exits = len(exits)

#walls = readWalls('obst_test.csv')
#doors = readDoors('hole_test.csv')
#exits = readExits('exit_test.csv')

if FN_FDS != None:
    walls = readOBST(FN_FDS, 'obst_test.csv')
    doors = readHOLE(FN_FDS, 'hole_test.csv')
    #exits = readEXIT(FN_FDS, 'exit_test.csv')
    Num_Walls = len(walls)
    Num_Doors = len(doors)
    #Num_Exits = len(exits)
else:
    walls = readWalls(FN_EVAC)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
    doors = readDoors(FN_EVAC)
    Num_Walls = len(walls)
    Num_Doors = len(doors)

###=== Probablity of Knowing Exit ========
tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&Ped2Exit')
agent2exit = readFloatArray(tableFeatures, len(agents), len(exits))
#agent2exit = readCSV("Agent2Exit2018.csv", "float")

###=== Door Direction for Each Exit ========
tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&Exit2Door')
exit2door = readFloatArray(tableFeatures, len(exits), len(doors))
#exit2door = readCSV("Exit2Door2018.csv", "float")

if np.shape(agent2exit)!= (Num_Agents, Num_Exits): #or np.shape(agent2exit)[1]!=
    print('\nError on input data: exits or agent2exit \n')
    print >>f, '\nError on input data: exits or agent2exit \n'
    raw_input('Error on input data: exits or agent2exit!  Please check')
    inputDataCorrect = False

if np.shape(exit2door)!= (Num_Exits, Num_Doors): 
    print '\nError on input data: exits or exit2door \n'
    print >>f, '\nError on input data: exits or exit2door \n'
    raw_input('Error on input data: exits or exit2door!  Please check')
    inputDataCorrect = False

if GROUPBEHAVIOR: 
    # Initialize Desired Interpersonal Distance
    tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupD')
    DFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    #DFactor_Init = readCSV("D_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupA')
    AFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    #AFactor_Init = readCSV("A_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupB')
    BFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    #BFactor_Init = readCSV("B_Data2018.csv", 'float')

    print >> f, "Wall Matrix\n", walls, "\n"
    print >> f, "D Matrix\n", DFactor_Init, "\n"
    print >> f, "A Matrix\n", AFactor_Init, "\n"
    print >> f, "B Matrix\n", BFactor_Init, "\n"

    if np.shape(DFactor_Init)!= (Num_Agents, Num_Agents):
        print '\nError on input data: DFactor_Init\n'
        print >>f, '\nError on input data: DFactor_Init\n'
        raw_input('Error on input data: DFactor_Init!  Please check')
        inputDataCorrect = False
        
    if np.shape(AFactor_Init)!= (Num_Agents, Num_Agents): 
        print '\nError on input data: AFactor_Init\n'
        print >>f, '\nError on input data: AFactor_Init\n'
        raw_input('Error on input data: AFactor_Init!  Please check')
        inputDataCorrect = False

    if np.shape(BFactor_Init)!= (Num_Agents, Num_Agents): 
        print '\nError on input data: BFactor_Init\n'
        print >>f, '\nError on input data: BFactor_Init\n'
        raw_input('Error on input data: BFactor_Init!  Please check')
        inputDataCorrect = False
    
    DFactor = DFactor_Init
    AFactor = AFactor_Init
    BFactor = BFactor_Init
else:
    DFactor = np.ones((Num_Agents, Num_Agents))
    AFactor = np.ones((Num_Agents, Num_Agents))
    BFactor = np.ones((Num_Agents, Num_Agents))


comm = np.zeros((Num_Agents, Num_Agents))
talk = np.zeros((Num_Agents, Num_Agents))

if inputDataCorrect:
    print "Input data format is correct!"
else:
    print "Input data format is wrong! Please check and modify!"

### Display a summary of input data
print 'Display a summary of input data as below. '
print 'number of agents: ', Num_Agents
print 'number of walls: ', Num_Walls
print 'number of doors: ', Num_Doors
print 'number of exits: ', Num_Exits
print '\n'

if TESTMODE:
    print "Now you can check if the input data is correct or not!"
    print "If everything is OK, please press ENTER to continue!"
    UserInput = raw_input('Check Input Data Here!')

#===================================================
#==========Preprocessing the Geom Data =====================
#========= Find Relationship of Door and Wall ==================
for wall in walls:
    wall.findAttachedDoors(doors)
    print "wall #No:", wall.id, 'isSingle:', wall.isSingleWall
    for door in wall.attachedDoors:
        print "attached door #No. :", door.id

for door in doors:
    door.findAttachedWalls(walls)
    print "door #No:", door.id, 'isSingle:', door.isSingleDoor
    for wall in door.attachedWalls:
        print "attached wall #No. :", wall.id


#Users may easily change some attributes of agents before the simulation
#########################################

#agents[1].pos = np.array([60, 8])
#agents[1].dest = np.array([20.0,10.0])        
#agents[1].direction = normalize(agents[1].dest - agents[1].pos)
agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.2
agents[1].dest = doors[1].pos

#agents[2].pos = np.array([60, 12])    
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6
agents[2].p = 0.6 #0.1
agents[2].pMode = 'fixed'
agents[2].interactionRange = 6.0
agents[2].dest = doors[1].pos

#agents[0].changeAttr(32, 22, 0, 0)
agents[0].pMode = 'fixed'


# Assign destinations of agents
# This is not yet used in the door selection routine
for idai,ai in enumerate(agents):
    temp = np.random.multinomial(1, agent2exit[ai.ID, :], size=1)
    print agent2exit[ai.ID, :]
    print temp
    exit_index = np.argmax(temp)
    ai.dest = exits[exit_index].pos
    ai.pathMap = exit2door[exit_index]
    ai.exitInMind = exits[exit_index]   # This is the exit in one's original mind
    print 'ai:', ai.ID, '--- exit:', exit_index
    

#agents[0].dest = exits[1].pos
#agents[1].dest = exits[1].pos
#agents[2].dest = exits[1].pos
#agents[3].dest = exits[0].pos
#agents[4].dest = exits[0].pos
#agents[5].dest = exits[0].pos
#agents[6].dest = exits[2].pos

        
#========== Test of Geometry of Building Structure===============
#========== Change Exit2Door Direction / Door Direction ==========
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Test Geom')
clock = pygame.time.Clock()
#screen.fill(white)

menu_01 = False
menu_02 = False
menu_left = False
change_arrows = False
draw_state = False
running = True
while running and inputDataCorrect:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            t_pause = pygame.time.get_ticks()/1000

        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            mouse_pos = np.array([mouseX, mouseY])
            
            #[button1, button2, button3]
            button = pygame.mouse.get_pressed()
            print('Three Buttons:', button)#1, button2, button3)

            # The button response has some problem in pygame.
            # So I will not use it (Not differentiate if it is right key or left key in mouse pressed)
            if button == (0,0,1):
                menu_left = True
                
            if button ==(1,0,0):
                menu_left = False

            ### Menu No 1:  Output Data ###
            if mouseX<60 and mouseX>0 and mouseY<20 and mouseY>3:
                menu_01 = not menu_01
            else:
                 #menu_01 =False
                 if  menu_01:
                      if mouseX<120 and mouseX>0 and mouseY<40 and mouseY>23:
                         # Show Door Info
                         SHOWWALLDATA= not SHOWWALLDATA
                         updateDoorData(doors, 'doorDataRev.csv')
                         menu_01 =False
                      elif mouseX<120 and mouseX>0 and mouseY<60 and mouseY>43:
                         # Show Door Info
                         SHOWDOORDATA= not SHOWDOORDATA
                         updateExit2Doors(exit2door, 'Exit2DoorRev.csv')
                         menu_01 =False
                      elif mouseX<120 and mouseX>0 and mouseY<80 and mouseY>63:
                         # Show Door Info
                         SHOWEXITDATA= not SHOWEXITDATA
                         menu_01 =False
                      else:
                         menu_01 =False

            ### Menu No 2: Show Data ###
            if mouseX<120 and mouseX>60 and mouseY<20 and mouseY>3:
                menu_02 = not menu_02
            else:
                 #menu_02 =False
                 if  menu_02:
                      if mouseX<200 and mouseX>80 and mouseY<40 and mouseY>23:
                         # Show Door Info
                         SHOWWALLDATA= not SHOWWALLDATA
                         menu_02 =False
                      elif mouseX<200 and mouseX>80 and mouseY<60 and mouseY>43:
                         # Show Door Info
                         SHOWDOORDATA= not SHOWDOORDATA
                         menu_02 =False
                      elif mouseX<200 and mouseX>80 and mouseY<80 and mouseY>63:
                         # Show Door Info
                         SHOWEXITDATA= not SHOWEXITDATA
                         menu_02 =False
                      else:
                         menu_02 =False

            ### Menu No 3: Start Simulation ###
            if mouseX<220 and mouseX>150 and mouseY<20 and mouseY>3:
                running = False
                t_pause = pygame.time.get_ticks()/1000

            if not draw_state:
                for exit in exits:
                    if exit.inside((mouse_pos-xyShift)*(1/ZOOMFACTOR)):
                        draw_state = True
                        draw_exit = exit
                        #draw_lines = []
                        #break
            else:
                if draw_exit.inside((mouse_pos-xyShift)*(1/ZOOMFACTOR)):
                    draw_state = False

        elif event.type == pygame.MOUSEBUTTONUP:
            (mouseX2, mouseY2) = pygame.mouse.get_pos()
            mouse_pos2 = np.array([mouseX2, mouseY2])

            #if button ==(1,0,0):
            change_arrows = True
            if not draw_state:
                draw_arrows = []
                draw_arrows.append((mouse_pos-xyShift)*(1/ZOOMFACTOR))
                draw_arrows.append((mouse_pos2-xyShift)*(1/ZOOMFACTOR))
                for door in doors:
                    if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                        w1=draw_arrows[-2]
                        w2=draw_arrows[-1]
                        result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                        #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                        if result1 != None:
                            #exit2door[draw_exit.id, door.id]=1
                            door.arrow=1
                        elif result2 != None:
                            #exit2door[draw_exit.id, door.id]= -2
                            door.arrow=-2
                        elif result3 != None:
                            #exit2door[draw_exit.id, door.id]= -1
                            door.arrow=-1
                        elif result4 != None:
                            #exit2door[draw_exit.id, door.id]= 2
                            door.arrow=2
            else:
                draw_arrows = []
                draw_arrows.append((mouse_pos-xyShift)*(1/ZOOMFACTOR))
                draw_arrows.append((mouse_pos2-xyShift)*(1/ZOOMFACTOR))
                for door in doors:
                    if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                        w1=draw_arrows[-2]
                        w2=draw_arrows[-1]
                        result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                        #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                        if result1 != None:
                            exit2door[draw_exit.id, door.id]=1
                            #door.arrow=1
                        elif result2 != None:
                            exit2door[draw_exit.id, door.id]= -2
                            #door.arrow=-2
                        elif result3 != None:
                            exit2door[draw_exit.id, door.id]= -1
                            #door.arrow=-1
                        elif result4 != None:
                            exit2door[draw_exit.id, door.id]= 2
                            #door.arrow=2
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                SHOWWALLDATA = not SHOWWALLDATA
            elif event.key == pygame.K_KP2:
                SHOWDOORDATA = not SHOWDOORDATA
            elif event.key == pygame.K_KP3:
                SHOWEXITDATA = not SHOWEXITDATA
            elif event.key == pygame.K_SPACE:
                updateDoorData(doors, 'doorDataRev.csv')
                updateExit2Doors(exit2door, 'Exit2DoorRev.csv')
            elif event.key == pygame.K_PAGEUP:
                ZOOMFACTOR = ZOOMFACTOR +1
            elif event.key == pygame.K_PAGEDOWN:
                ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
            elif event.key == pygame.K_UP:
                ySpace=ySpace-10
            elif event.key == pygame.K_DOWN:
                ySpace=ySpace+10
            elif event.key == pygame.K_LEFT:
                xSpace=xSpace-10
            elif event.key == pygame.K_RIGHT:
                xSpace=xSpace+10
                

    ####################################
    # Drawing the geometries: walls, doors, exits
    ####################################

    xyShift = np.array([xSpace, ySpace])
    
    drawWall(screen, walls, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
    drawDoor(screen, doors, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
    drawExit(screen, exits, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

    #####################################
    #### Draw Agents at Initial Positions ###
    #####################################
    for idai, agent in enumerate(agents):
        
        if agent.inComp == 0:
            continue
        
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
        scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
        pygame.draw.circle(screen, red, scPos, AGENTSIZE, LINEWIDTH)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
        screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

    if draw_state:

        # Draw Selected Exit
        startPos = np.array([draw_exit.params[0],draw_exit.params[1]])
        endPos = np.array([draw_exit.params[2],draw_exit.params[3]])

        x= ZOOMFACTOR*draw_exit.params[0]+xSpace
        y= ZOOMFACTOR*draw_exit.params[1]+ySpace
        w= ZOOMFACTOR*(draw_exit.params[2] - draw_exit.params[0])
        h= ZOOMFACTOR*(draw_exit.params[3] - draw_exit.params[1])
            
        pygame.draw.rect(screen, orange, [x, y, w, h], LINEWIDTH+2)

        for door in doors:
            drawDirection(screen, door, exit2door[draw_exit.id, door.id], ZOOMFACTOR, xSpace, ySpace)
        
        #if len(draw_lines)>1:
        #    for i in range(len(draw_lines)-1):
        #        #print('i in draw_lines:', i)
        #        pygame.draw.line(screen, red, draw_lines[i]*ZOOMFACTOR, draw_lines[i+1]*ZOOMFACTOR, LINEWIDTH)
    
    if change_arrows:
        if len(draw_arrows)>1:
            pygame.draw.line(screen, red, draw_arrows[0]*ZOOMFACTOR+xyShift, draw_arrows[1]*ZOOMFACTOR+xyShift, LINEWIDTH)

     # Show Mouse Position
    (mouseX2, mouseY2) = pygame.mouse.get_pos()
    mouse_pos2 = np.array([mouseX2, mouseY2])
    #pygame.mouse.set_visible(False)
    #pygame.mouse.get_pressed() -> button1, button2, button3
    
    myfont=pygame.font.SysFont("arial",16)
    text_surface=myfont.render(str((mouse_pos2-xyShift)*(1/ZOOMFACTOR)), True, tan, black)
    screen.blit(text_surface, mouse_pos2)
    text_surface=myfont.render(str(mouse_pos2), True, lightblue, black)
    screen.blit(text_surface, mouse_pos2+[0.0, 20.0])

    #if menu_left is True:
    if menu_01 is True:
        #surface.fill(white, (0, 20, 60, 60))
        pygame.draw.rect(screen, tan, [0, 20, 120, 60])
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('output_doors', True, white, tan)
        screen.blit(text_surface, [0,23])#+[0.0,20.0]) #+xyShift)
        text_surface=myfont.render('output_exit2door', True, white, tan)
        screen.blit(text_surface, [0,43])#+[0.0,40.0]) #+xyShift)
        text_surface=myfont.render('output_agents', True, white, tan)
        screen.blit(text_surface, [0,63])#+[0.0,60.0]) #+xyShift)
        #text_surface=myfont.render('show_agentforce', True, red, white)
        #screen.blit(text_surface, mouse_pos+[0.0,60.0]) #+xyShift)

     #if menu_left is True:
    if menu_02 is True:
        #surface.fill(white, (0, 20, 60, 60))
        pygame.draw.rect(screen, tan, [80, 20, 120, 60])
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('show/hide walls', True, white, tan)
        screen.blit(text_surface, [80,23])#+[0.0,20.0]) #+xyShift)
        text_surface=myfont.render('show/hide doors', True, white, tan)
        screen.blit(text_surface, [80,43])#+[0.0,40.0]) #+xyShift)
        text_surface=myfont.render('show/hide exits', True, white, tan)
        screen.blit(text_surface, [80,63])#+[0.0,60.0]) #+xyShift)
        #text_surface=myfont.render('show_agentforce', True, red, white)
        #screen.blit(text_surface, mouse_pos+[0.0,60.0]) #+xyShift)
        

    #--------Menu Bar at Top Left-----------
    #pygame.draw.rect(screen, tan, [720, 3, 60, 20], LINEWIDTH)
    myfont=pygame.font.SysFont("arial",14)
    text_surface=myfont.render('OutputData', True, white, tan)
    screen.blit(text_surface, [0,3]) #+xyShift)

    myfont=pygame.font.SysFont("arial",14)
    text_surface=myfont.render('ShowData', True, white, tan)
    screen.blit(text_surface, [80,3]) #+xyShift)

    myfont=pygame.font.SysFont("arial",14)
    text_surface=myfont.render('Simulation!', True, white, tan)
    screen.blit(text_surface, [150,3]) #+xyShift)
            
    pygame.display.flip()
    #clock.tick(20)
    
if TESTMODE:
    start = raw_input("Start simulation now?")

##########################################
### Simulation starts here with Pygame
##########################################

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Modified Social Force Model')
clock = pygame.time.Clock()
#screen.fill(white)

#myfont=pygame.font.SysFont("arial",16)
#text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
#screen.blit(text_surface, (16,20))

t_sim = 0.0
tt_OtherList = 0.0
#t_pause=0.0
running = True
while running and inputDataCorrect:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            #button = pygame.mouse.get_pressed()            
        # elif event.type == pygame.MOUSEBUTTONUP:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                ZOOMFACTOR = ZOOMFACTOR +1
            elif event.key == pygame.K_PAGEDOWN:
                ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
            elif event.key == pygame.K_t:
                MODETRAJ = not MODETRAJ
            elif event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
            elif event.key == pygame.K_v:
                SHOWVELOCITY = not SHOWVELOCITY
            elif event.key == pygame.K_i:
                SHOWINDEX = not SHOWINDEX
            elif event.key == pygame.K_KP1:
                SHOWWALLDATA = not SHOWWALLDATA
            elif event.key == pygame.K_KP2:
                SHOWDOORDATA = not SHOWDOORDATA
            elif event.key == pygame.K_KP3:
                SHOWEXITDATA = not SHOWEXITDATA
            elif event.key == pygame.K_UP:
                ySpace=ySpace-10
            elif event.key == pygame.K_DOWN:
                ySpace=ySpace+10
            elif event.key == pygame.K_LEFT:
                xSpace=xSpace-10
            elif event.key == pygame.K_RIGHT:
                xSpace=xSpace+10

    if MODETRAJ == False:
        screen.fill(white)

    if PAUSE is True:
        t_now = pygame.time.get_ticks()/1000
        t_pause = t_now-tt
        continue

    # Compute the agents one by one in loop
    for idai,ai in enumerate(agents):
        
        # Whether ai is in computation
        if ai.inComp == 0:
            continue
	
	#Pre-evacuation Time Effect
        tt = pygame.time.get_ticks()/1000 - t_pause
        if (tt < ai.tpre):
            ai.desiredSpeed = random.uniform(0.3,1.6)
        else: 
            ai.desiredSpeed = random.uniform(2.0,3.0)
	
        #ai.dest = ai.memory.peek()
	
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old
        peopleInter = 0.0
        wallInter = np.array([0.0, 0.0])
        doorInter = np.array([0.0, 0.0])
        otherDir = np.array([0.0, 0.0])
        otherSpeed = 0.0
        #otherMovingNum = 0
	
        ai.actualSpeed = np.linalg.norm(ai.actualV)
        ai.desiredSpeed = np.linalg.norm(ai.desiredV)
	
        #print >> f, "desired speed of agent i:", ai.desiredSpeed, "/n"
        #print >> f, "actual speed of agent i:", ai.actualSpeed, "/n"
	
        if ai.desiredSpeed != 0: 
            ai.ratioV = ai.actualSpeed/ai.desiredSpeed
        else: 
            ai.ratioV = 1
	
        ######################
        # Wall force adjusted
        # Stress indicator is used (Or known as ratioV)
        ai.stressLevel = 1 - ai.ratioV
        ai.test = 0.0 #??
        #ai.diw_desired = max(0.2, ai.ratioV)*0.6
        #ai.A_WF = 700*max(0.3, ai.ratioV)
        #ai.B_WF = 1.6*max(min(0.6, ai.ratioV),0.2)
	
        ai.diw_desired = max(0.5, ai.ratioV)*0.6
        #ai.A_WF = 30*max(0.5, ai.ratioV)
        ai.B_WF = 2.2*max(min(0.5, ai.ratioV),0.2) 
	
	
        ######################
        # Herding indicator adjusted
        # There are two method:
        # 1. White Noise Method
        # 2. Stress Level Method (Or known as ratioV: Helbing's Equation)
        #if ai.p == 0.0:
        if ai.pMode == 'random':
            ai.p = random.uniform(-0.3, 0.6)  # Method-1
            #ai.p = random.uniform(-0.3, 0.6*ai.stressLevel)
            #ai.p = 1 - ai.ratioV  	# Method-2
        elif ai.pMode =='increase':
            pass
        elif ai.pMode =='decrease':
            pass
	    
        if t_sim > tt_OtherList:
            ai.others=[]
        
            #############################################
            # Compute interaction of agents
            # Group force and herding effect
            # Find the agents who draw ai's attention

            for idaj,aj in enumerate(agents):
                
                if aj.inComp == 0:
                    comm[idai, idaj] = 0
                    talk[idai, idaj] = 0
                    continue
                
                rij = ai.radius + aj.radius
                dij = np.linalg.norm(ai.pos - aj.pos)
                 
                #Difference of current destinations
                dij_dest = np.linalg.norm(ai.dest - aj.dest)
                 
                #Difference of desired velocities
                vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)
                 
                #Difference of actual velocities
                vij_actualV = np.linalg.norm(ai.actualV - aj.actualV)
                 
                phiij = vectorAngleCos(ai.actualV , (aj.pos - ai.pos))
                anisoF = ai.lamb + (1-ai.lamb)*(1+cos(phiij))*0.5
                 
                #print >> f, "anisotropic factor", anisoF, "/n"
                 
                if idai == idaj:
                    continue
                        
                #####################################################
                # Check whether there is a wall between agent i and j
                no_wall_ij = True
                if WALLBLOCKHERDING: 
                    for idwall, wall in enumerate(walls):
                        if wall.inComp ==0:
                            continue
                        #result, flag = ai.iswallInBetween(aj, wall)
                        result, flag = wall.wallInBetween(ai.pos, aj.pos)
                        if flag==True:
                            no_wall_ij = False
                            break
                            
                see_i2j = True
                if np.dot(ai.actualV, aj.pos-ai.pos)<0.2:
                    see_i2j = False
                if np.linalg.norm(ai.actualV)<0.2:
                    temp=random.uniform(-180, 180)
                    if temp < 70 and temp > -70:
                        see_i2j =True
                 
                #############################################
                # Turn on or off group social force
                # Also known as cohesive social force
                #if COHESION and no_wall_ij and see_i2j:
                #    peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF
             
                #############################################
                # Traditional Social Force and Physical Force
                if no_wall_ij: #and see_i2j:
                    peopleInter += ai.agentForce(aj)*anisoF
                             
                talk[idai, idaj] = 0
                ###################################################
                # Interactive Opinion Dynamics Starts here
                # Including Herding Effect, Group Effect and Talking Behavior
                # There are several persons around you.  Which draws your attention?  
                ###################################################
                if dij < ai.B_CF*BFactor[idai, idaj] + rij*DFactor[idai, idaj] and no_wall_ij and see_i2j:
                #if dij < ai.interactionRange and no_wall_ij and see_i2j:
                    comm[idai, idaj] = 1
                    ai.others.append(aj)
                    
                    #DFactor[idai, idaj] = (1-ai.p)*DFactor[idai, idaj]+ai.p*DFactor[idaj, idai]
                    #AFactor[idai, idaj] = (1-ai.p)*AFactor[idai, idaj]+ai.p*AFactor[idaj, idai]
                    #BFactor[idai, idaj] = (1-ai.p)*BFactor[idai, idaj]+ai.p*BFactor[idaj, idai]
                    #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*aj.desiredV		
                else: 
                    comm[idai, idaj] = 0

                # Loop of idaj,aj ends here
                ###########################
            
            print '=== ai id ===::', idai
            print 'ai.others len:', len(ai.others)
            
            if len(ai.others)!=0: #and tt>ai.tpre:
                otherDir, otherSpeed = ai.opinionDynamics()
                ai.direction = (1-ai.p)*ai.direction + ai.p*otherDir
                ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherSpeed
                ai.desiredV = ai.desiredSpeed*ai.direction

            tt_OtherList = t_sim+DT_OtherList
            
        
        for aj in ai.others:

            idaj=aj.ID
            print 'others ID', idaj
            #############################################
            # Turn on or off group social force
            # Also known as cohesive social force
            		
            dij = np.linalg.norm(ai.pos - aj.pos)
	     
            #Difference of current destinations
            dij_dest = np.linalg.norm(ai.dest - aj.dest)
	     
            #Difference of desired velocities
            vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)
	     
            #Difference of actual velocities
            vij_actualV = np.linalg.norm(ai.actualV - aj.actualV)

            phiij = vectorAngleCos(ai.actualV , (aj.pos - ai.pos))
            anisoF = ai.lamb + (1-ai.lamb)*(1+cos(phiij))*0.5
			
            if dij<ai.interactionRange: #and 0.6<random.uniform(0.0,1.0):
            #ai.talk_prob<random.uniform(0.0,1.0):
                DFactor[idai, idaj]=2.0
                AFactor[idai, idaj]=600
                BFactor[idai, idaj]=300
                ai.tau = ai.talk_tau
                talk[idai, idaj]=1
            else:
                DFactor[idai, idaj]=DFactor_Init[idai, idaj]
                AFactor[idai, idaj]=AFactor_Init[idai, idaj]
                BFactor[idai, idaj]=BFactor_Init[idai, idaj]
                ai.tau = ai.moving_tau
                talk[idai, idaj]=0

            peopleInter += ai.agentForce(aj)*anisoF

            if COHESION:
                peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF

            #if tt > aj.tpre: 
            #    ai.tpre = (1-ai.p)*ai.tpre + ai.p*aj.tpre
            if dij < ai.interactionRange:
                ai.tpre = 0.5*ai.tpre + 0.5*aj.tpre

        #ai.others=list(set(ai.others))
        #################################
        # Herding Effect Computed
        #if otherMovingNum != 0:
            #ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
            #ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + #ai.p*otherMovingSpeed/otherMovingNum
            #ai.desiredV = ai.desiredSpeed*ai.direction

            #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir

        ########################################################
        # Turn on or off self-repulsion by boolean variable SELFREPULSION
        # Also known as sub-consciousness effect in crowd dynamics
        ########################################################
        if SELFREPULSION and (len(ai.others) != 0):
            selfRepulsion = ai.selfRepulsion(DFactor[idai, idai], AFactor[idai, idai], BFactor[idai, idai])#*ai.direction
            #peopleInter += selfRepulsion
        else: 
            selfRepulsion = 0.0

        outsideDoor = True
        for door in doors:
            if door.inComp ==0:
                continue
            #doorInter += ai.doorForce(door)
            if door.inside(ai.pos):
                wallInter = np.array([0.0, 0.0])
                outsideDoor = False
                #doorInter = ai.doorForce(door)
                #break

        #########################
        # Calculate Wall Repulsion
        if outsideDoor:
            for wall in walls:
                if wall.inComp ==0:
                    continue
                wallInter += ai.wallForce(wall)
                #wallInter += wall.wallForce(ai)

        #print('Forces from Walls:', wallInter)
        #print('Forces from people:', peopleInter)
	
        #############################################
        # Calculate Motive Forces
        # Consider TPRE features
        #############################################	
        #tt = pygame.time.get_ticks()/1000-t_pause
        if (tt < ai.tpre and TPREMODE == 1):
            ai.desiredV = ai.direction*0.0
            ai.desiredSpeed = 0.0
            #ai.dest = ai.pos
            ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
            motiveForce = ai.adaptVel()
	
        #ai.sumAdapt += motiveForce*0.2  #PID: Integration Test Here
        
        #tt = pygame.time.get_ticks()/1000-t_pause
        if (tt < ai.tpre and TPREMODE == 2):
            motiveForce = np.array([0.0, 0.0])

        if (tt < ai.tpre and TPREMODE == 3):
            pass
            if outsideDoor:
                doorInter = np.array([0.0, 0.0])
                
            goSomeone = ai.moveToAgent()
            if goSomeone != None:
                gsid = goSomeone.ID
                ai.diretion = normalize(goSomeone.pos - ai.pos)
                ai.desiredSpeed = random.uniform(0.6,1.6)
                ai.desiredV = ai.diretion*ai.desiredSpeed
                ai.tau = random.uniform(0.6,1.6) #ai.tpre_tau
                motiveForce = ai.adaptVel()
                print ('&&& In Tpre Stage:')
                print ('goSomeone:', goSomeone.ID)
            else:
                ai.desiredV = ai.direction*0.0
                ai.desiredSpeed = 0.0
                ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
                motiveForce = ai.adaptVel()
                print '&&& In Tpre Stage:'
                print 'goSomeone is None.'

        #temp = 0.0
        #maxWallForce = 0.0
        #wallDirection = np.array([0.0, 0.0])
	
        #for idwall, wall in enumerate(walls):
        #temp = np.linalg.norm(ai.wallForce(wall))
        #    if temp > maxWallForce: 
        #	maxWallForce = temp
        #	wallDirection = np.array([wall[0],wall[1]]) - np.array([wall[2],wall[3]])
        #	closeWall = wall
	
        if (tt >= ai.tpre):
        #################################
        # Wall Effect Computed: 
        # Is There Any Wall Nearby On The Route?
        # If So, Adjust Desired Direction

            #####################################################
            # Check whether there is a wall between agent i and the destination
            no_wall_dest = True
            for idwall, wall in enumerate(walls):
                if wall.inComp ==0:
                    continue
                result, flag = wall.wallInBetween(ai.pos, ai.dest)
                if result != None:
                    no_wall_dest = False
                    break
               
            # Start to search visible doors
            ai.targetDoors=ai.findVisibleTarget(walls, doors)
            print 'ai:', ai.ID, 'Length of targetDoors:', len(ai.targetDoors)
            
            # Start to search visible exits
            ai.targetExits=ai.findVisibleTarget(walls, exits)

            #ai.findVisibleTarget(walls, doors)
            #ai.findVisibleTarget(walls, exits)
            
            goDoor = ai.selectTarget(exit2door)
            #goDoor.computePos()
            if goDoor==None:
                print 'goDoor is None.'
                doorInter = np.array([0.0, 0.0])
            else:
                print 'go Door:', goDoor.id, goDoor.pos
                doorInter = ai.doorForce(goDoor, 'edge', 0.3)
                
            #dir1=goDoor.direction()
            #dir2=goDoor.pos-ai.pos
            #if goDoor!=None: #and np.dot(dir1, dir2)>=0:
                goDoorPx = goDoor.pos #visiblePx(ai, walls)
                ai.direction = normalize(goDoorPx-ai.pos)
                ai.desiredV = ai.desiredSpeed*ai.direction

                ### ??? ###
                if goDoor.inside(ai.pos):
                    if len(ai.route)==0:
                        ai.route.append(goDoor.pos)
                    #if ai.route[len(ai.route)-1] is not goDoor.pos
                    #    print 'Error in ai.route!'
                    elif ai.route[len(ai.route)-1] is not goDoor.pos:
                        ai.route.append(goDoor.pos)

            # Interaction with enviroment
            # Search for wall on the route
            # temp = 0.0
            closeWall = walls[0] #None #walls[0]
            closeWallDist = 10.0 # Define how close the wall is
            for wall in walls:
                if wall.inComp ==0:
                    continue
                crossp, diw, arrow = ai.wallOnRoute(wall, 1.0)
                if diw!=None and diw < closeWallDist:
                    closeWallDist = diw
                    closeWall = wall


            closeWallEffect = True
            crossp, diw, wallDirection = ai.wallOnRoute(closeWall, 1.0)
            if diw!=None and goDoor!=None and outsideDoor:
                if goDoor.inside(crossp):
                    wallInter = wallInter - ai.wallForce(closeWall)
                    closeWallEffect = False
                else:
                    if np.dot(wallDirection, ai.desiredV) < 0.0 and wall.arrow==0:
                        #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                        wallDirection = -wallDirection
                    #ai.direction = ai.direction + wallDirection*20/diw
                    ai.direction = normalize(ai.direction)
                    ai.desiredV = ai.desiredSpeed*ai.direction


            if diw!=None and goDoor==None: # and not ai.targetDoors:
            #if closeWall!=None:
            #    diw = ai.wallOnRoute(closeWall)
                #wallDirection = np.array([closeWall.params[0],closeWall.params[1]]) - np.array([closeWall.params[2],closeWall.params[3]])
                #wallDirection = -normalize(wallDirection)
                #if wall.arrow==0 or ai.aType=='search': 
                if np.dot(wallDirection, ai.actualV) < 0.0 and wall.arrow==0:
                    #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                    wallDirection = -wallDirection

                #if (isnan(closeWall.pointer1[0]) or isnan(closeWall.pointer1[1])) and (isnan(closeWall.pointer2[0]) or isnan(closeWall.pointer2[1])) or ai.aType=='search': 
                if isnan(closeWall.pointer1[0]) or isnan(closeWall.pointer1[1]) or ai.aType=='search':
                    pass
                    if diw==None:
                        print 'diw==None'
                        print 'ai:', idai
                        print 'closeWall:', closeWall.id
                        print '################################'
		    
                    ai.direction = ai.direction + wallDirection*20/diw
                    ai.direction = normalize(ai.direction)
                    ai.desiredV = ai.desiredSpeed*ai.direction
                    #ai.destmemory.append([wall[2],wall[3]]+0.1*wallDirection)
                #elif ai.destmemory[-1] is not [closeWall[5], closeWall[6]]:  
                    #ai.destmemory[-1][0]!=closeWall[5] or ai.destmemory[-1][1]!= closeWall[6]:
                    #ai.destmemory.append([wall[0],wall[1]]+0.1*wallDirection)
                    #ai.destmemory.append([closeWall[5], closeWall[6]])
                    #ai.direction = normalize(ai.destmemory[-1]-ai.pos)
                    #ai.desiredV = ai.desiredSpeed*ai.direction
                else:
                    temp1= np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    temp2= np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                    for aj in ai.others:
                        temp1 = temp1+np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-aj.pos)
                        temp2 = temp2+np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-aj.pos)
                    if temp1<temp2:
                        ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    else:
                        ai.direction = normalize([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                    #ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    ai.desiredV = ai.desiredSpeed*ai.direction
            
                #ai.direction = ai.direction + wallDirection/np.linalg.norm(wallDirection)*20/diw
                #ai.desiredV = ai.desiredSpeed*ai.direction
	    
            #if np.linalg.norm(ai.pos-ai.destmemory[-1])<=1e-3:
            #    ai.destmemory.pop()
            ai.tau=ai.moving_tau
            motiveForce = ai.adaptVel()	
            
            #print 'destmemeory', len(ai.destmemory)

        # Compute total force
        sumForce = motiveForce + peopleInter + wallInter + doorInter + ai.diss*ai.actualV + selfRepulsion #+ ai.sumAdapt

        # Compute acceleration
        accl = sumForce/ai.mass
        
        # Compute velocity
        ai.actualV = ai.actualV + accl*DT # consider dt = 0.5

        ai.wallrepF = wallInter
        ai.doorF = doorInter
        ai.groupF = peopleInter
        ai.selfrepF = selfRepulsion

        if TESTFORCE:
            print '@motiveForce:', np.linalg.norm(motiveForce), motiveForce
            print '@peopleInter:', np.linalg.norm(peopleInter), peopleInter
            print '@wallInter:', np.linalg.norm(wallInter), wallInter
            print '@doorInter:', np.linalg.norm(doorInter), doorInter
            print '@diss:', np.linalg.norm(ai.diss*ai.actualV), ai.diss*ai.actualV
            print '@selfRepulsion:', np.linalg.norm(selfRepulsion), selfRepulsion
        
        ###########################################
        # Solution to Overspeed: Agents will not move too fast
        ai.actualSpeed = np.linalg.norm(ai.actualV)
        if (ai.actualSpeed >= ai.maxSpeed):
            ai.actualV = ai.actualV*ai.maxSpeed/ai.actualSpeed
            #ai.actualV[0] = ai.actualV[0]*ai.maxSpeed/ai.actualSpeed
            #ai.actualV[1] = ai.actualV[1]*ai.maxSpeed/ai.actualSpeed
    
        # Calculate Positions
        ai.pos = ai.pos + ai.actualV*DT
        #print(ai.pos)
        #print(accl,ai.actualV,ai.pos)
    
        ai.desiredV_old = ai.desiredV
        ai.actualV_old = ai.actualV
    
        ###########################################
        ## Output time when agents reach the safety
        #if TIMECOUNT and (ai.pos[0] >= 35.0) and (ai.Goal == 0):
        if TIMECOUNT and (np.linalg.norm(ai.pos-ai.dest)<=0.2) and (ai.Goal == 0):
            print('Reaching the goal:')
            ai.inComp = 0
            ai.Goal = 1
            ai.timeOut = pygame.time.get_ticks()
            #ai.timeOut = clock.get_time()/1000.0
            print 'Time to Reach the Goal:', ai.timeOut
            print >> f, 'Time to Reach the Goal:', ai.timeOut
        
        ###########################################
        ## Remove agent when agent reaches the destination    
        #if np.linalg.norm(ai.pos-ai.dest)<=1e-3:
         #   agents.remove(agents[idai])

        ###########################################
        ## Remove agent when agent reaches the exit    
        for exit in exits:
            if exit.inComp == 0:
                continue
            if exit.inside(ai.pos):
                ai.inComp = 0

    #############################
    ######### Drawing Process ######
    xyShift = np.array([xSpace, ySpace])
    t_sim = t_sim + DT

    ####################
    # Showing Time
    ####################
    if SHOWTIME:
        tt = pygame.time.get_ticks()/1000-t_pause
        myfont=pygame.font.SysFont("arial",14)
        time_surface=myfont.render("Physics Time:" + str(tt), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [470,370]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("Simulation Time:" + str(t_sim), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [630,370]) #[750,350]*ZOOMFACTOR)

    drawWall(screen, walls, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
    drawDoor(screen, doors, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
    drawExit(screen, exits, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

    #   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(), AGENTSIZE, LINEWIDTH)
    
    ####################
    # Drawing the agents
    ####################
    #for agent in agents:
    
    for idai, agent in enumerate(agents):
        
        if agent.inComp == 0:
            continue
        
        #scPos = np.array([0, 0])
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
        scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
        
        #temp = int(100*agent.ratioV)
        #AGENTCOLOR = [0,0,temp]
        color_para = [0, 0, 0]
        color_para[0] = int(255*min(1, agent.ratioV))
        pygame.draw.circle(screen, color_para, scPos, int(ai.radius*ZOOMFACTOR), LINEWIDTH)
	#int(ai.radius*ZOOMFACTOR), LINEWIDTH)
        
        if THREECIRCLES:
            leftS = [0, 0]
            leftShoulder = agent.shoulders()[0]
            leftS[0] = int(leftShoulder[0]*ZOOMFACTOR+xSpace)
            leftS[1] = int(leftShoulder[1]*ZOOMFACTOR+ySpace)
        
            rightS = [0, 0]
            rightShoulder = agent.shoulders()[1]	
            rightS[0] = int(rightShoulder[0]*ZOOMFACTOR+xSpace)
            rightS[1] = int(rightShoulder[1]*ZOOMFACTOR+ySpace)
            
            #print 'shoulders:', leftS, rightS
            pygame.draw.circle(screen, color_para, leftS, AGENTSIZE/2, 3)
            pygame.draw.circle(screen, color_para, rightS, AGENTSIZE/2, 3)
        
        if SHOWVELOCITY:
            #endPosV = [0, 0]
            #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
            #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
            endPosV = (agent.pos+agent.actualV)*ZOOMFACTOR+xyShift
        
            #endPosDV = [0, 0]
            #endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR+xSpace)
            #endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR+ySpace)
            endPosDV = (agent.pos+agent.desiredV)*ZOOMFACTOR+xyShift
        
            #stressShow = 0
            #stressShow = int(255*agent.ratioV)
            #pygame.draw.line(screen, blue, leftS, rightS, 3)
            pygame.draw.line(screen, blue, scPos, endPosV, 2)
            pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)

        if DRAWWALLFORCE:
            #endPosV = [0, 0]
            #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
            #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
            endPosWF = (agent.pos+agent.wallrepF)*ZOOMFACTOR+xyShift
        
            #pygame.draw.line(screen, blue, scPos, endPosV, 2)
            pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
            #khaki = 240,230,140

        if DRAWDOORFORCE:
            endPosDF = (agent.pos+agent.doorF)*ZOOMFACTOR+xyShift
            pygame.draw.line(screen, green, scPos, endPosDF, 2)

        if DRAWGROUPFORCE:
            endPosGF = (agent.pos+agent.groupF)*ZOOMFACTOR+xyShift
            pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

        if DRAWSELFREPULSION:
            endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
            pygame.draw.line(screen, lightpink, scPos, endPosRF, 2)
            
        
        for idaj, agentOther in enumerate(agents):
            scPosOther = [0, 0]
            scPosOther[0] = int(agentOther.pos[0]*ZOOMFACTOR+xSpace)
            scPosOther[1] = int(agentOther.pos[1]*ZOOMFACTOR+ySpace)
            
            agentPer = agent.pos+0.8*normalize(agentOther.pos - agent.pos)
            scPosDir = [0, 0]
            scPosDir[0] = int(agentPer[0]*ZOOMFACTOR+xSpace)
            scPosDir[1] = int(agentPer[1]*ZOOMFACTOR+ySpace)
            
            #leftShoulder, rightShoulder = agent.shoulders()
            #leftS = [int(leftShoulder[0]*ZOOMFACTOR), int(leftShoulder[1]*ZOOMFACTOR)]
            #rightS = [int(rightShoulder[0]*ZOOMFACTOR), int(rightShoulder[1]*ZOOMFACTOR)]
            
            if comm[idai, idaj] == 1 and SHOWINTELINE: 
                pygame.draw.line(screen, blue, scPos, scPosOther, 2)
                #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                pygame.draw.line(screen, green, scPos, scPosDir, 4)

            if talk[idai, idaj] == 1 and SHOWINTELINE: 
                pygame.draw.line(screen, red, scPos, scPosOther, 3)
                pygame.draw.line(screen, green, scPos, scPosDir, 4)
        
        #print(scPos)
	
        if SHOWINDEX:
            tt = pygame.time.get_ticks()/1000-t_pause
            myfont=pygame.font.SysFont("arial",14)
            if tt < agent.tpre:
                text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
            else: 
                text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

        if SHOWSTRESS:
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render(str(agent.ratioV), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift+[0,6])

    pygame.display.flip()
    clock.tick(20)

f.close()

