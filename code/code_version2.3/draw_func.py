
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

import pygame
import pygame.draw
import numpy as np
from math_func import *
from data_func import *
from agent import *
import sys, os
import matplotlib.pyplot as plt

#from math_func import *

########################
##### Color Info as below ###
########################

red=255,0,0
green=0,255,0
blue=0,0,255
white=255,255,255
yellow=255,255,0
IndianRed=205,92,92
tan = 210,180,140
skyblue = 135,206,235
orange = 255,128,0
khaki = 240,230,140
black = 0,0,0
purple = 160, 32, 240
magenta = 255, 0, 255
lightpink =255, 174, 185
lightblue =178, 223, 238
cyan = 0, 255, 255
lightcyan = 224, 255, 255
lightgreen = 193, 255, 193

# Some Constant Parameters for Pygame 
SCREENSIZE = [900, 600]
RESOLUTION = 180
#BACKGROUNDCOLOR = [255,255,255]
LINEWIDTH = 2
#AGENTSIZE = 6

####################
# Drawing the walls
####################
def drawWalls(screen, walls, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for wall in walls:
        
        if wall.inComp == 0:
            continue
        
        if wall.mode=='line':
            startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
            endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
            startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, 2)
            

            if SHOWDATA:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
                screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
                text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
                screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

        elif wall.mode=='rect':
            x= ZOOMFACTOR*wall.params[0]
            y= ZOOMFACTOR*wall.params[1]
            w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
            h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
            
            pygame.draw.rect(screen, red, [x+xSpace, y+ySpace, w, h], 2)

            if SHOWDATA:
                pass
                startPos = np.array([wall.params[0],wall.params[1]])
                endPos = np.array([wall.params[2],wall.params[3]])

                myfont=pygame.font.SysFont("arial",10)

                #text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
                #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

                #text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
                #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)


def drawSingleWall(screen, wall, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if wall.inComp == 0:
        print('Error: Draw a wall that is not in Computation!\n')
        return
    
    if wall.mode=='line':
        startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
        endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
        startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
        endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
        pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, lw)
        

        if SHOWDATA:
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
            text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
            screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

    elif wall.mode=='rect':
        x= ZOOMFACTOR*wall.params[0]
        y= ZOOMFACTOR*wall.params[1]
        w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
        h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
        
        pygame.draw.rect(screen, red, [x+xSpace, y+ySpace, w, h], lw)

        if SHOWDATA:
            pass
            startPos = np.array([wall.params[0],wall.params[1]])
            endPos = np.array([wall.params[2],wall.params[3]])

            myfont=pygame.font.SysFont("arial",10)

            #text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
            #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)
    

    ####################
    # Drawing the doors
    ####################

def drawDoors(screen, doors, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for door in doors:

        if door.inComp == 0:
            continue
        
        #startPos = np.array([door[0], door[1]])
        #endPos = np.array([door[2], door[3]])

        startPos = np.array([door.params[0],door.params[1]]) #+xyShift
        endPos = np.array([door.params[2],door.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*door.params[0] 
        y= ZOOMFACTOR*door.params[1] 
        w= ZOOMFACTOR*(door.params[2] - door.params[0])
        h= ZOOMFACTOR*(door.params[3] - door.params[1])
            
        pygame.draw.rect(screen, green, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:
            
            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('Door:'+str(door.oid)+'/'+str(door.name)+'/'+str(door.arrow), True, green, black)
            screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)


def drawSingleDoor(screen, door, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if door.inComp == 0:
        print('Error: Draw a door that is not in Computation!\n')
        return
    
    #startPos = np.array([door[0], door[1]])
    #endPos = np.array([door[2], door[3]])

    startPos = np.array([door.params[0],door.params[1]]) #+xyShift
    endPos = np.array([door.params[2],door.params[3]]) #+xyShift

    #Px = [0, 0]
    #Px[0] = int(Pos[0]*ZOOMFACTOR)
    #Px[1] = int(Pos[1]*ZOOMFACTOR)
    #pygame.draw.circle(screen, red, Px, LINESICKNESS)

    x= ZOOMFACTOR*door.params[0] 
    y= ZOOMFACTOR*door.params[1] 
    w= ZOOMFACTOR*(door.params[2] - door.params[0])
    h= ZOOMFACTOR*(door.params[3] - door.params[1])
        
    pygame.draw.rect(screen, green, [x+ xSpace, y+ ySpace, w, h], lw)

    if SHOWDATA:
        
        myfont=pygame.font.SysFont("arial",10)
        text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
        screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

        #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
        #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

        myfont=pygame.font.SysFont("arial",13)
        text_surface=myfont.render('Door:'+str(door.oid)+'/'+str(door.name)+'/'+str(door.arrow), True, green, black)
        screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)


    ####################
    # Drawing the exits
    ####################

def drawExits(screen, exits, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for exit in exits:

        if exit.inComp == 0:
            continue

        startPos = np.array([exit.params[0],exit.params[1]]) #+xyShift
        endPos = np.array([exit.params[2],exit.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*exit.params[0]
        y= ZOOMFACTOR*exit.params[1]
        w= ZOOMFACTOR*(exit.params[2] - exit.params[0])
        h= ZOOMFACTOR*(exit.params[3] - exit.params[1])
            
        pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:

            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('Exit:'+str(exit.oid)+'/'+str(exit.name)+'/'+str(exit.arrow), True, red, white)
            screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)


def drawSingleExit(screen, exit, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if exit.inComp == 0:
        print('Error: Draw an exit that is not in Computation!\n')
        return

    startPos = np.array([exit.params[0],exit.params[1]]) #+xyShift
    endPos = np.array([exit.params[2],exit.params[3]]) #+xyShift

    #Px = [0, 0]
    #Px[0] = int(Pos[0]*ZOOMFACTOR)
    #Px[1] = int(Pos[1]*ZOOMFACTOR)
    #pygame.draw.circle(screen, red, Px, LINESICKNESS)

    x= ZOOMFACTOR*exit.params[0]
    y= ZOOMFACTOR*exit.params[1]
    w= ZOOMFACTOR*(exit.params[2] - exit.params[0])
    h= ZOOMFACTOR*(exit.params[3] - exit.params[1])
        
    pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], lw)

    if SHOWDATA:

        myfont=pygame.font.SysFont("arial",10)
        text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
        screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

        #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
        #screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

        myfont=pygame.font.SysFont("arial",13)
        text_surface=myfont.render('Exit:'+str(exit.oid)+'/'+str(exit.name)+'/'+str(exit.arrow), True, red, white)
        screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)


def drawDirection(screen, door, arrow, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    
    if arrow == 1:
        direction = np.array([1.0, 0.0])
    elif arrow == -1:
        direction = np.array([-1.0, 0.0])
    elif arrow == 2:
        direction = np.array([0.0, 1.0])
    elif arrow == -2:
        direction = np.array([0.0, -1.0])
    elif arrow == 0:
        direction = np.array([0.0, 0.0])
    
    startPx=door.pos
    endPx=door.pos+direction
    pygame.draw.line(screen, green, startPx*ZOOMFACTOR+xyShift, endPx*ZOOMFACTOR+xyShift, 2)

    #dir = endPx - startPx
    #dir2 = np.array([-dir[0], dir[1]])
    #dir2 = normalize(dir2)
    #arrowPx = endPx - dir*0.2
    #arrowPx1 = arrowPx + 0.6*dir2
    #arrowPx2 = arrowPx - 0.6*dir2
    #pygame.draw.line(screen, green, endPx*ZOOMFACTOR+xyShift, arrowPx1*ZOOMFACTOR+xyShift, 2)
    #pygame.draw.line(screen, green, endPx*ZOOMFACTOR+xyShift, arrowPx2*ZOOMFACTOR+xyShift, 2)


def show_mesh(screen, x_min, y_min, x_max, y_max, x_points, y_points, BLDindex, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0, SHOWDATA=False, debug=False):
    
    print(np.shape(BLDindex))
    (dimX,dimY)=np.shape(BLDindex)
    
    #print(dimX, dimY)
    #dimX is x_points+2
    #dimY is y_points+2
    
    if np.shape(BLDindex)!= (x_points+2, y_points+2): 
        print('\nError in input data BLDindex \n')
        #f.write('\nError in input data BLDindex \n')
        if sys.version_info[0] == 2:
            raw_input('\nError in input data BLDindex \n Please check!')
        if sys.version_info[0] == 3:
            input('\nError in input data BLDindex \n Please check!')

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)
    
    xDim=np.linspace(x_min-del_x, x_max+del_x, x_points+2) #Should be the same as x
    yDim=np.linspace(y_min-del_y, y_max+del_y, y_points+2) #Should be the same as y
    
    if debug:
        print("Dim info:\n")
        print(xDim)
        print(yDim)

    xyShift = np.array([xSpace, ySpace])

    for i in range(dimX):
        for j in range(dimY):
            
            '''
            if BLDindex[i,j]==0:
                startPos = np.array([xDim[i],yDim[j]]) #np.array([int(xDim[i]),int(yDim[j])])
                endPos = np.array([int(xDim[i]),int(yDim[j])])
                pygame.draw.circle(screen, [0,60,0], startPos*ZOOMFACTOR, 6, 2)
                pygame.draw.line(screen, [0,60,0], startPos*ZOOMFACTOR-[0,0.8]+xyShift, startPos*ZOOMFACTOR+[0,0.8]+xyShift, 2)
            else:
                startPos = np.array([xDim[i],yDim[j]]) #np.array([int(xDim[i]),int(yDim[j])])
                endPos = np.array([int(xDim[i]),int(yDim[j])])
                pygame.draw.circle(screen, [0,60,0], startPos*ZOOMFACTOR, 6, 2)
                pygame.draw.line(screen, [0,60,0], startPos*ZOOMFACTOR-[0,0.8]+xyShift, startPos*ZOOMFACTOR+[0,0.8]+xyShift, 2)                
            '''
                
            if BLDindex[i,j]==0:
                ghostcellpos=np.array([xDim[i],yDim[j]])
                pygame.draw.line(screen, cyan, ghostcellpos*ZOOMFACTOR-[0,0.6]+xyShift, ghostcellpos*ZOOMFACTOR+[0,0.6]+xyShift, 15)
                #ghostcellpos=np.array([xDim[i],yDim[j]])
                pygame.draw.line(screen, cyan, ghostcellpos*ZOOMFACTOR-[0.6,0]+xyShift, ghostcellpos*ZOOMFACTOR+[0.6,0]+xyShift, 15)
            else:
                fieldcell=np.array([0,0])
                fieldcell[0]=int(xDim[i]*ZOOMFACTOR+xSpace)
                fieldcell[1]=int(yDim[j]*ZOOMFACTOR+ySpace)
                pygame.draw.circle(screen, red, fieldcell, 2, 2)
                                
            #vec=np.array([Ud[i,j],Vd[i,j]])
            #startPos = np.array([xDim[i],yDim[j]])
            #endPos = startPos + VECFACTOR*normalize(vec) #
            #pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
            

def show_vel(screen, x_min, y_min, x_max, y_max, x_points, y_points, Ud, Vd, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0, SHOWDATA=False, debug=False):

    #Ud=np.load("Ud.npy")
    #Vd=np.load("Vd.npy")
    print(np.shape(Ud))
    (dimX,dimY)=np.shape(Ud)

    #dim=np.shape(U)
    #print(dimX, dimY)

    #dimX is x_points+2
    #dimY is y_points+2

    if (dimX, dimY)!= (x_points+2, y_points+2): 
        print('\nError in input data Ud or Vd \n')
        #f.write('\nError in input data Ud or Vd \n')
        if sys.version_info[0] == 2:
            raw_input('\nError in input data Ud or Vd \n Please check!')
        if sys.version_info[0] == 3:
            input('\nError in input data Ud or Vd \n Please check!')

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)
    
    xDim = np.linspace(x_min-del_x, x_max+del_x, x_points+2) #Should be the same as x
    yDim = np.linspace(y_min-del_y, y_max+del_y, y_points+2) #Should be the same as y
    
    if debug:
        print("Dim info:\n")
        print(xDim)
        print(yDim)

    #BLDindex = build_compartment(x_min, y_min, x_max, y_max, x_points, y_points, walls, doors, exits)
    #BLDindex = build_compartment(x_min, y_min, x_max, y_max, dimX-2, dimY-2, walls, doors, exits)
    
    # Visualize gradient field by pygame
    #BACKGROUNDCOLOR = [255,255,255]
    #LINECOLOR = [255,0,0]
    #SHOWDATA=False
    VECFACTOR = 0.3

    #pygame.init()
    #screen = pygame.display.set_mode(SCREENSIZE)
    #screen.fill(BACKGROUNDCOLOR)
    xyShift = np.array([xSpace, ySpace])

    for i in range(dimX):
        for j in range(dimY):
            #if BLDindex[i,j]==0:
                #startPos = np.array([xDim[i],yDim[j]]) #np.array([int(xDim[i]),int(yDim[j])])
                #endPos = np.array([int(xDim[i]),int(yDim[j])])
                #pygame.draw.circle(screen, [0,60,0], startPos*ZOOMFACTOR, 6, 2)
                #pygame.draw.line(screen, [0,60,0], startPos*ZOOMFACTOR-[0,0.8]+xyShift, startPos*ZOOMFACTOR+[0,0.8]+xyShift, 2)
            vec=np.array([Ud[i,j],Vd[i,j]])
            startPos = np.array([xDim[i],yDim[j]])
            endPos = startPos + VECFACTOR*normalize(vec) #
            pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)

        #drawWalls(screen, simu.walls, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        #drawDoors(screen, simu.doors, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        #drawExits(screen, simu.exits, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        


def show_geom(simu, debug=False):

    # The file to record the output data of simulation
    #FN_Temp = simu.outDataName + ".txt"
    #f = open(FN_Temp, "a+")

    #f.write("\n\nTest Geometry of Compartment. \n")
    #f.write('FN_FDS=', simu.FN_FDS)
    #f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print ("Input data is not correct!  Please modify input data file!")
        return

    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
    walls = simu.walls
    doors = simu.doors #list(simu.doors)
    exits = simu.exits
    agents = simu.agents
    exit2door = simu.exit2door
    #agent2exit = simu.agent2exit
    
    nw = len(walls)
    nd = len(doors)
    ne = len(exits)
    
    xyShift = np.array([xSpace, ySpace])
    
    #========== Test of Geometry of Building Structure===============
    #========== Change Exit2Door Direction / Door Direction ==========
    
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Test Geom')
    clock = pygame.time.Clock()
    #screen.fill(white)

    menu_01 = False
    menu_02 = False
    menu_03 = False
    menu_04 = False
    menu_05 = False
    menu_06 = False
    #menu_07 = False
    menu_left = False # Not used for right button of mouse
    
    change_arrows = False
    draw_state = False
    move_agent_state = False
    
    running = True
    while running: 
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.display.quit()
                simu.continueToSimu=False
                simu.quit()
                os.remove(simu.outDataName + ".txt")
                #os.remove(simu.outDataName + ".bin")
                #simu.t_pause = pygame.time.get_ticks()/1000

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
                ### This method is useful to generate menu bar in pygame
                if mouseX<60 and mouseX>0 and mouseY<20 and mouseY>3:
                    menu_01 = not menu_01
                else:
                     #menu_01 =False
                     if  menu_01:
                         if mouseX<120 and mouseX>0 and mouseY<40 and mouseY>23:
                             # dump door direction data
                             print ("Output door data into bldDataRev.csv in the working example folder! Please check!")
                             updateDoorData(doors, os.path.join(simu.fpath, 'bldDataRev.csv'))
                              #simu.FN_EVAC+simu.FN_FDS) #simu.outDataName+'doorDataRev.csv')
                             menu_01 =False
                         elif mouseX<120 and mouseX>0 and mouseY<60 and mouseY>43:
                             # dump exit2door data
                             #print ("Output exit2door data into Exit2DoorRev.csv! Please check!")
                             #updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
                             print ("Output exit data into bldDataRev.csv in the working example folder! Please check!")
                             updateExitData(exits, os.path.join(simu.fpath, 'bldDataRev.csv')) #simu.outDataName+'exitDataRev.csv')
                             menu_01 =False
                         elif mouseX<120 and mouseX>0 and mouseY<80 and mouseY>63:
                             # dump wall data
                             print ("Output wall data into bldDataRev.csv in the working example folder! Please check!")
                             #updateWallData(simu.walls, 'wallDataRev.csv')
                             #print(simu.fpath, os.path.join(simu.fpath, 'bldDataRev.csv'))
                             updateWallData(walls, os.path.join(simu.fpath, 'bldDataRev.csv')) #simu.outDataName+'wallDataRev.csv')
                             menu_01 =False
                         elif mouseX<120 and mouseX>0 and mouseY<100 and mouseY>83:
                             # dump exit2door data
                             print ("Output exit2door data into bldDataRev.csv in the working example folder! Please check!")
                             updateExit2Doors(exit2door, os.path.join(simu.fpath, 'bldDataRev.csv'))
                             menu_01 =False
                          # elif mouseX<120 and mouseX>0 and mouseY<122 and mouseY>105:
                          # To add something else in future development
                          #   simu.SHOWEXITDATA= not simu.SHOWEXITDATA
                          #   menu_01 =False
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
                             simu.SHOWDOORDATA= not simu.SHOWDOORDATA
                             menu_02 =False
                          elif mouseX<200 and mouseX>80 and mouseY<60 and mouseY>43:
                             # Show Exit Info
                             simu.SHOWEXITDATA= not simu.SHOWEXITDATA
                             menu_02 =False
                          elif mouseX<200 and mouseX>80 and mouseY<80 and mouseY>63:
                             # Show Wall Info
                             simu.SHOWMESH= not simu.SHOWMESH
                             menu_02 =False
                          else:
                             menu_02 =False

                ### Menu No 3: Start Simulation ###
                if mouseX<220 and mouseX>150 and mouseY<20 and mouseY>3:
                    menu_03 = not menu_03
                    menu_04 = False
                    menu_05 = False
                    menu_06 = False
                    
                if mouseX<290 and mouseX>220 and mouseY<20 and mouseY>3:
                    menu_03 = False
                    menu_04 = not menu_04
                    menu_05 = False
                    menu_06 = False
                    
                if mouseX<360 and mouseX>290 and mouseY<20 and mouseY>3:
                    menu_03 = False
                    menu_04 = False
                    menu_05 = not menu_05
                    menu_06 = False
                    
                if mouseX<430 and mouseX>360 and mouseY<20 and mouseY>3:
                    menu_03 = False
                    menu_04 = False
                    menu_05 = False
                    menu_06 = not menu_06

                if mouseX<500 and mouseX>430 and mouseY<20 and mouseY>3:
                    running = False
                    #simu.quit()
                    simu.continueToSimu=True
                    simu.t_pause = pygame.time.get_ticks()/1000

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

                if not move_agent_state:
                    for agent in agents:
                        if np.linalg.norm((mouse_pos-xyShift)*(1/ZOOMFACTOR)-agent.pos)<1.0:
                            move_agent_state = True
                            move_agent = agent
                else:
                    if np.linalg.norm((mouse_pos-xyShift)*(1/ZOOMFACTOR)-agent.pos)<1.0:
                        move_agent_state = False

            elif event.type == pygame.MOUSEBUTTONUP:
                (mouseX2, mouseY2) = pygame.mouse.get_pos()
                mouse_pos2 = np.array([mouseX2, mouseY2])

                if mouseX>=0 and mouseX<=500 and mouseY>=0 and mouseY<=20:
                    continue
                elif mouseX2>=0 and mouseX2<=500 and mouseY2>=0 and mouseY2<=20:
                    continue
                else:
                    if menu_03 is True:
                        move_agent_state = False
                        px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                        px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                        addWall(walls, px1, px2, mode='line')
                        #menu_03 = False

                    if menu_04 is True:
                        move_agent_state = False
                        px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                        px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                        x1 = px1[0]
                        y1 = px1[1]
                        x2 = px2[0]
                        y2 = px2[1]
                        # It seems that it is not necessary to check x1<x2 and y1<y2
                        #if x1<x2 and y1<y2:
                        #    pass
                        addWall(walls, px1, px2, mode='rect')

                    if menu_05 is True:
                        move_agent_state = False
                        px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                        px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                        x1 = min(px1[0],px2[0])
                        y1 = min(px1[1],px2[1])
                        x2 = max(px1[0],px2[0])
                        y2 = max(px1[1],px2[1])
                        #if x1<x2 and y1<y2:
                        #    pass
                        #addDoor(doors, [x1,y1], [x2,y2], mode='rect')
                        addDoor(doors, px1, px2, mode='rect')
                        print('Direction of the door added:', doors[-1].arrow)

                    if menu_06 is True:
                        move_agent_state = False
                        px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                        px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                        x1 = px1[0]
                        y1 = px1[1]
                        x2 = px2[0]
                        y2 = px2[1]
                        #if x1<x2 and y1<y2:
                        #    pass
                        addExit(exits, px1, px2, mode='rect')

                if move_agent_state:
                    xyPos = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                    move_agent.pos = xyPos
                    move_agent_state = False
                    

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
                                #exit2door[draw_exit.oid, door.oid]=1
                                door.arrow=1
                            elif result2 != None:
                                #exit2door[draw_exit.oid, door.oid]= -2
                                door.arrow=-2
                            elif result3 != None:
                                #exit2door[draw_exit.oid, door.oid]= -1
                                door.arrow=-1
                            elif result4 != None:
                                #exit2door[draw_exit.oid, door.oid]= 2
                                door.arrow=2
                else:
                    draw_arrows = []
                    draw_arrows.append((mouse_pos-xyShift)*(1/ZOOMFACTOR))
                    draw_arrows.append((mouse_pos2-xyShift)*(1/ZOOMFACTOR))
                    
                    
                    if exit2door is not None and np.shape(exit2door) == (len(exits), len(doors)):
                        for door in doors:
                            if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                                w1=draw_arrows[-2]
                                w2=draw_arrows[-1]
                                result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                                #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                                if result1 != None:
                                    exit2door[draw_exit.oid, door.oid]=1
                                    #door.arrow=1
                                elif result2 != None:
                                    exit2door[draw_exit.oid, door.oid]= -2
                                    #door.arrow=-2
                                elif result3 != None:
                                    exit2door[draw_exit.oid, door.oid]= -1
                                    #door.arrow=-1
                                elif result4 != None:
                                    exit2door[draw_exit.oid, door.oid]= 2
                                    #door.arrow=2
                    else:
                        print('exit2door is not defined in the input csv file.  Please check!')
                        
            elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_1:
                #    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                if event.key == pygame.K_2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_1:
                    simu.SHOWMESH = not simu.SHOWMESH
                elif event.key == pygame.K_5:
                    simu.SHOWNAME = not simu.SHOWNAME
                elif event.key == pygame.K_SPACE:
                    #updateWallData(simu.walls, 'wallDataRev.csv')
                    #updateDoorData(simu.doors, 'doorDataRev.csv')
                    #updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
                    updateWallData(walls, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    updateDoorData(doors, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    updateExitData(exits, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    print ("Output walls/doors/exits data into bldDataRev.csv in the working example folder! Please check!")
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
                elif event.key == pygame.K_z:
                    if menu_03 or menu_04:
                        if len(walls)>0:
                            walls.pop()
                    if menu_05:
                        if len(doors)>0:
                            doors.pop()
                    if menu_06:
                        if len(exits)>0:
                            exits.pop()
                        



        ####################################
        # Drawing the geometries: walls, doors, exits
        ####################################

        xyShift = np.array([xSpace, ySpace])
        
        drawWalls(screen, walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)
        
        
        if simu.solver!=0 and simu.SHOWMESH:
            simu.buildMesh()
            show_mesh(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, simu.bldmesh, ZOOMFACTOR, xSpace, ySpace)
        
        #####################################
        #### Draw Agents at Initial Positions ###
        #####################################
        for idai, agent in enumerate(agents):
            
            if agent.inComp == 0:
                continue
            
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
            scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
            #pygame.draw.circle(screen, red, scPos, agent.size, LINEWIDTH)
            try:
                pygame.draw.circle(screen, tan, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            except:
                pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)

            myfont=pygame.font.SysFont("arial",14)
            if simu.SHOWNAME:
                text_surface=myfont.render(str(idai)+'/'+str(agent.name), True, (255,0,0), (255,255,255))
            else:
                text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

        if move_agent_state:
            scPos = [0, 0]
            scPos[0] = int(move_agent.pos[0]*ZOOMFACTOR+xSpace)
            scPos[1] = int(move_agent.pos[1]*ZOOMFACTOR+ySpace)
            pygame.draw.circle(screen, white, scPos, agent.size, LINEWIDTH+2)

        if draw_state:

            # Draw Selected Exit
            startPos = np.array([draw_exit.params[0],draw_exit.params[1]])
            endPos = np.array([draw_exit.params[2],draw_exit.params[3]])

            x= ZOOMFACTOR*draw_exit.params[0]+xSpace
            y= ZOOMFACTOR*draw_exit.params[1]+ySpace
            w= ZOOMFACTOR*(draw_exit.params[2] - draw_exit.params[0])
            h= ZOOMFACTOR*(draw_exit.params[3] - draw_exit.params[1])
                
            pygame.draw.rect(screen, orange, [x, y, w, h], LINEWIDTH+2)
            
            print("draw_exit.name", str(draw_exit.name))  #"door.name", door.name
            if exit2door is not None and np.shape(exit2door) == (len(exits), len(doors)):
                for door in doors: #simu.doors:
                    drawDirection(screen, door, exit2door[draw_exit.oid, door.oid], ZOOMFACTOR, xSpace, ySpace)
                
            #if len(draw_lines)>1:
            #    for i in range(len(draw_lines)-1):
            #        #print('i in draw_lines:', i)
            #        pygame.draw.line(screen, red, draw_lines[i]*ZOOMFACTOR, draw_lines[i+1]*ZOOMFACTOR, LINEWIDTH)
        
        else:
            for door in doors:
                drawDirection(screen, door, door.arrow, ZOOMFACTOR, xSpace, ySpace)
        
        if change_arrows:
            if len(draw_arrows)>1:
                pygame.draw.line(screen, red, draw_arrows[0]*ZOOMFACTOR+xyShift, draw_arrows[1]*ZOOMFACTOR+xyShift, LINEWIDTH)

        #if menu_left is True:
        if menu_01 is True:
            #surface.fill(white, (0, 20, 60, 60))
            pygame.draw.rect(screen, tan, [0, 20, 120, 84])
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render('output_doors', True, white, tan)
            screen.blit(text_surface, [0,23])#+[0.0,20.0]) #+xyShift)
            text_surface=myfont.render('output_exits', True, white, tan)
            screen.blit(text_surface, [0,44])#+[0.0,40.0]) #+xyShift)
            text_surface=myfont.render('output_walls', True, white, tan)
            screen.blit(text_surface, [0,65])#+[0.0,60.0]) #+xyShift)
            text_surface=myfont.render('output_exit2door', True, white, tan)
            screen.blit(text_surface, [0,84])#+[0.0,60.0]) #+xyShift)
            #text_surface=myfont.render('show_agentforce', True, red, white)
            #screen.blit(text_surface, mouse_pos+[0.0,60.0]) #+xyShift)

         #if menu_left is True:
        if menu_02 is True:
            #surface.fill(white, (0, 20, 60, 60))
            pygame.draw.rect(screen, tan, [80, 20, 120, 60])
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render('show/hide doors', True, white, tan)
            screen.blit(text_surface, [80,23])#+[0.0,20.0]) #+xyShift)
            text_surface=myfont.render('show/hide exits', True, white, tan)
            screen.blit(text_surface, [80,43])#+[0.0,40.0]) #+xyShift)
            text_surface=myfont.render('show/hide mesh', True, white, tan)
            screen.blit(text_surface, [80,63])#+[0.0,60.0]) #+xyShift)
            #text_surface=myfont.render('show_agentforce', True, red, white)
            #screen.blit(text_surface, mouse_pos+[0.0,60.0]) #+xyShift)

        if menu_03 is True:
            text_surface=myfont.render('Add one wall in line shape by dragging mouse from start point to end point.', True, white, tan)
            screen.blit(text_surface, [150,23]) #+xyShift)
            
        if menu_04 is True:
            text_surface=myfont.render('Add one wall in rectangular shape by dragging mouse from start point to end point.', True, white, tan)
            screen.blit(text_surface, [220,23]) #+xyShift)

        if menu_05 is True:
            text_surface=myfont.render('Add one door in rectangular shape by dragging mouse from start point to end point.', True, white, tan)
            screen.blit(text_surface, [290,23]) #+xyShift)

        if menu_06 is True:
            text_surface=myfont.render('Add one exit in rectangular shape by dragging mouse from start point to end point.', True, white, tan)
            screen.blit(text_surface, [340,23]) #+xyShift)

            
        #--------Menu Bar at Top Left-----------
        #pygame.draw.rect(screen, tan, [720, 3, 60, 20], LINEWIDTH)
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('OutputData', True, white, tan)
        screen.blit(text_surface, [0,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ShowData', True, white, tan)
        screen.blit(text_surface, [80,3]) #+xyShift)

        #myfont=pygame.font.SysFont("arial",14)
        #text_surface=myfont.render('AddData', True, white, tan)
        #screen.blit(text_surface, [150,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('+wall(line)', True, white, tan)
        screen.blit(text_surface, [150,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('+wall(rect)', True, white, tan)
        screen.blit(text_surface, [220,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render(' +door ', True, white, tan)
        screen.blit(text_surface, [290,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render(' +exit  ', True, white, tan)
        screen.blit(text_surface, [340,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('Simulation!', True, white, tan)
        screen.blit(text_surface, [390,3]) #+xyShift)
        
        # Show Mouse Position
        (mouseX3, mouseY3) = pygame.mouse.get_pos()
        mouse_pos3 = np.array([mouseX3, mouseY3])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",16)
        text_surface=myfont.render(str((mouse_pos3-xyShift)*(1/ZOOMFACTOR)), True, tan, black)
        screen.blit(text_surface, mouse_pos3+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos3), True, lightblue, black)
        screen.blit(text_surface, mouse_pos3+[0.0, 36.0])

        # The Zoom and xSpace ySpace Info
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ZOOM:'+str(ZOOMFACTOR), True, white, black)
        screen.blit(text_surface, [500,3]) #+xyShift)
        text_surface=myfont.render('xSpace:'+str(xSpace), True, white, black)
        screen.blit(text_surface, [600,3]) #+xyShift)        
        text_surface=myfont.render('ySpace:'+str(ySpace), True, white, black)
        screen.blit(text_surface, [700,3]) #+xyShift) 
        text_surface=myfont.render('solver:'+str(simu.solver), True, white, black)
        screen.blit(text_surface, [800,3]) #+xyShift) 
                                                                
        pygame.display.flip()
        clock.tick(20)
        
        '''
        (mmm, nnn) = np.shape(agent2exit)
        if len(exits)>nnn:
            agent2exit = np.zeros((mmm, len(exits)))
            agent2exit[:,0:simu.num_exits] = simu.agent2exit
            print("agent2exit:", np.shape(agent2exit))
            input("Please check")
        '''
        
        #print("exit2door:", np.shape(exit2door))
        if exit2door is not None:
            (mmm, nnn) = np.shape(exit2door)
        else:
            mmm=0
            nnn=0
            
        if len(exits)>0 and len(doors)>0:
            '''
            if (len(exits)>=mmm and len(doors)>=nnn):
                exit2door_new = np.zeros((len(exits), len(doors)))
                exit2door_new[0:mmm, 0:nnn] = exit2door
                exit2door=exit2door_new
                print("exit2door:", np.shape(exit2door))
                #input("Please check")
            '''
            
            if (len(exits)>mmm or len(doors)>nnn):
                exit2door_new = np.zeros((len(exits), len(doors)))
                exit2door_new[0:mmm, 0:nnn] = exit2door
                exit2door=exit2door_new
                print("exit2door:", np.shape(exit2door))
                #input("Please check")
                
            if (len(exits)<mmm or len(doors)<nnn):
                exit2door_new = np.zeros((len(exits), len(doors)))
                exit2door_new = exit2door[0:len(exits), 0:len(doors)]
                exit2door=exit2door_new
                print("exit2door:", np.shape(exit2door))
                #input("Please check")

    # The file to record the output data of simulation
    #if debug:
        #print(len(walls), nw, "\n")
        #print(len(doors), nd, "\n")
        #print(len(exits), ne, "\n")
        #input('Plese check')
    
    #if len(walls)>len(simu.walls) or len(doors)>len(simu.doors) or len(exits)>len(simu.exits):
    if len(walls)>nw or len(doors)>nd or len(exits)>ne:
    #   pass
        FN_Temp = simu.outDataName + ".txt"
        f = open(FN_Temp, "a+")
        f.write("\n\nTest Geometry of Compartment: Entities added in TestGeom \n")
        f.write('Display a summary of input data after TestGeom as below.\n')
        f.write('number of walls added: '+str(len(walls)-nw)+ '\n')
        f.write('number of doors added: '+str(len(doors)-nd)+ '\n')
        f.write('number of exits added: '+str(len(exits)-ne)+ '\n')
        f.write('All the objects added are directly included in compuation loop. \n\n')
        
        f.close()
        
        #updateWallData(walls, os.path.join(simu.fpath, 'bldDataRev.csv'))
        #updateDoorData(doors, os.path.join(simu.fpath, 'bldDataRev.csv'))
        #updateExitData(exits, os.path.join(simu.fpath, 'bldDataRev.csv'))
        
        updateWallData(walls, simu.outDataName +'.csv')
        updateDoorData(doors, simu.outDataName +'.csv')
        updateExitData(exits, simu.outDataName +'.csv')

    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    simu.walls = walls
    simu.doors = doors
    simu.exits = exits
    simu.agents = agents
    simu.exit2door = exit2door
    #simu.agent2exit = agent2exit
    
    
    pygame.display.quit()


# Show flow field by pygame
def show_flow(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    f.write("Show flow field here.")
    # f.write('FN_FDS=', simu.FN_FDS)
    # f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print("Input data is not correct!  Please modify input data file!")
        return

    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
    #walls = simu.walls
    #doors = simu.doors
    #exits = simu.exits

    exitIndex=-1
    #if simu.solver=1:
    #    (dimX,dimY)=np.shape(simu.UallExit)

    #if simu.solver=2:
    #    (dimX,dimY)=np.shape(simu.UeachExit)
    
    change_arrows = False
    draw_state = False
    move_agent_state = False
    
    ##########################################
    ### Show flow field here with Pygame
    ##########################################

    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Modified Social Force Model')
    clock = pygame.time.Clock()
    #screen.fill(white)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    simu.t_sim = 0.0
    simu.tt_OtherList = 0.0
    #t_pause=0.0
    running = True
    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.display.quit()
                simu.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                #button = pygame.mouse.get_pressed()      
                mouse_pos = np.array([mouseX, mouseY])
                if not draw_state:
                    for exit in simu.exits:
                        if exit.inside((mouse_pos-xyShift)*(1/ZOOMFACTOR)):
                            draw_state = True
                            draw_exit = exit
                            #draw_lines = []
                else:
                    if draw_exit.inside((mouse_pos-xyShift)*(1/ZOOMFACTOR)):
                        draw_state = False
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                (mouseX2, mouseY2) = pygame.mouse.get_pos()
                mouse_pos2 = np.array([mouseX2, mouseY2])
                
                change_arrows = True
                if not draw_state:
                    draw_arrows = []
                    draw_arrows.append((mouse_pos-xyShift)*(1/ZOOMFACTOR))
                    draw_arrows.append((mouse_pos2-xyShift)*(1/ZOOMFACTOR))
                    for door in simu.doors:
                        if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                            w1=draw_arrows[-2]
                            w2=draw_arrows[-1]
                            result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                            #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                            if result1 != None:
                                #exit2door[draw_exit.oid, door.oid]=1
                                door.arrow=1
                            elif result2 != None:
                                #exit2door[draw_exit.oid, door.oid]= -2
                                door.arrow=-2
                            elif result3 != None:
                                #exit2door[draw_exit.oid, door.oid]= -1
                                door.arrow=-1
                            elif result4 != None:
                                #exit2door[draw_exit.oid, door.oid]= 2
                                door.arrow=2
                else:
                    draw_arrows = []
                    draw_arrows.append((mouse_pos-xyShift)*(1/ZOOMFACTOR))
                    draw_arrows.append((mouse_pos2-xyShift)*(1/ZOOMFACTOR))

                    for door in simu.doors:
                        if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                            w1=draw_arrows[-2]
                            w2=draw_arrows[-1]
                            result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                            #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                            if result1 != None:
                                simu.exit2door[draw_exit.oid, door.oid]=1
                                #door.arrow=1
                            elif result2 != None:
                                simu.exit2door[draw_exit.oid, door.oid]= -2
                                #door.arrow=-2
                            elif result3 != None:
                                simu.exit2door[draw_exit.oid, door.oid]= -1
                                #door.arrow=-1
                            elif result4 != None:
                                simu.exit2door[draw_exit.oid, door.oid]= 2
                                #door.arrow=2

                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                elif event.key == pygame.K_SPACE:
                    #updateWallData(simu.walls, 'wallDataRev.csv')
                    #updateDoorData(simu.doors, 'doorDataRev.csv')
                    updateExit2Doors(simu.exit2door, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    print ("Output exit2door data into bldDataRev.csv in the working example folder! Please check!")
                    #updateWallData(simu.walls, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    #updateDoorData(simu.doors, os.path.join(simu.fpath, 'bldDataRev.csv'))
                    #updateExitData(simu.exits, os.path.join(simu.fpath, 'bldDataRev.csv'))

                #elif event.key == pygame.K_v:
                #    simu.SHOWVELOCITY = not simu.SHOWVELOCITY
                #elif event.key == pygame.K_i:
                #    simu.SHOWINDEX = not simu.SHOWINDEX
                #elif event.key == pygame.K_d:
                #    simu.DRAWDOORFORCE = not simu.DRAWDOORFORCE

                elif event.key == pygame.K_1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10
                elif event.key == pygame.K_o:
                    exitIndex=exitIndex+1
                elif event.key == pygame.K_p:
                    exitIndex=exitIndex-1


        #tt = pygame.time.get_ticks()/1000-simu.t_pause
        #if simu.PAUSE is True:
        #    t_now = pygame.time.get_ticks()/1000
        #    simu.t_pause = t_now-tt
        #    continue

        if draw_state:

            # Draw Selected Exit
            startPos = np.array([draw_exit.params[0],draw_exit.params[1]])
            endPos = np.array([draw_exit.params[2],draw_exit.params[3]])

            x= ZOOMFACTOR*draw_exit.params[0]+xSpace
            y= ZOOMFACTOR*draw_exit.params[1]+ySpace
            w= ZOOMFACTOR*(draw_exit.params[2] - draw_exit.params[0])
            h= ZOOMFACTOR*(draw_exit.params[3] - draw_exit.params[1])
                
            pygame.draw.rect(screen, orange, [x, y, w, h], LINEWIDTH+2)
            
            print("draw_exit.name", str(draw_exit.name))
            #for door in doors: #simu.doors:
            #    drawDirection(screen, door, simu.exit2door[draw_exit.oid, door.oid], ZOOMFACTOR, xSpace, ySpace)
            
            #if len(draw_lines)>1:
            #    for i in range(len(draw_lines)-1):
            #        #print('i in draw_lines:', i)
            #        pygame.draw.line(screen, red, draw_lines[i]*ZOOMFACTOR, draw_lines[i+1]*ZOOMFACTOR, LINEWIDTH)
        
        if change_arrows:
            if len(draw_arrows)>1:
                pygame.draw.line(screen, red, draw_arrows[0]*ZOOMFACTOR+xyShift, draw_arrows[1]*ZOOMFACTOR+xyShift, LINEWIDTH)
        
        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################################
        # Showing flow field parameters
        ####################################
        
        myfont=pygame.font.SysFont("arial",14)
        time_surface=myfont.render("xmin:" + str(simu.xmin), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [20,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("ymin:" + str(simu.ymin), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [20,23]) #[750,350]*ZOOMFACTOR)

        time_surface=myfont.render("xmax:" + str(simu.xmax), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [100,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("ymax:" + str(simu.ymax), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [100,23]) #[750,350]*ZOOMFACTOR)

        time_surface=myfont.render("num of x points:" + str(simu.xpt), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [200,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("num of y points:" + str(simu.ypt), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [200,23]) #[750,350]*ZOOMFACTOR)
        
        show_mesh(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, simu.bldmesh, ZOOMFACTOR, xSpace, ySpace)
        
        # Show flow field in the background
        if simu.solver==1 and exitIndex%2==0: # and exitIndex==-1:
            Ud=simu.UallExit#[1:-1, 1:-1]
            Vd=simu.VallExit#[1:-1, 1:-1]
            show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
            for door in simu.doors:
                drawDirection(screen, door, door.arrow, ZOOMFACTOR, xSpace, ySpace)
                    
        if simu.solver==2:
            #for idexit, exit in enumerate(simu.exits):
            #    if exitIndex%len(simu.exits) == idexit:
            #        Utemp = simu.UeachExit[idexit] 
            #        Vtemp = simu.VeachExit[idexit]
            #        Ud = Utemp#[1:-1, 1:-1]
            #        Vd = Vtemp#[1:-1, 1:-1]
            #show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)

            idexit = exitIndex%(len(simu.exits)+2)
            if idexit < len(simu.exits):
                Utemp = simu.UeachExit[idexit] 
                Vtemp = simu.VeachExit[idexit]
                Ud = Utemp#[1:-1, 1:-1]
                Vd = Vtemp#[1:-1, 1:-1]
                show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
                for door in simu.doors:
                    drawDirection(screen, door, simu.exit2door[idexit, door.oid], ZOOMFACTOR, xSpace, ySpace)
                
                # High light the target exit in pygame display: Trial well, but not that useful
                #targeExit=simu.exits[idexit]
                #x= ZOOMFACTOR*targeExit.params[0]+xSpace
                #y= ZOOMFACTOR*targeExit.params[1]+ySpace
                #w= ZOOMFACTOR*(targeExit.params[2] - targeExit.params[0])
                #h= ZOOMFACTOR*(targeExit.params[3] - targeExit.params[1])
                #pygame.draw.rect(screen, orange, [x, y, w, h], LINEWIDTH+2)
            
            elif idexit == len(simu.exits):
                # Show nearest-exit field
                Ud=simu.UallExit#[1:-1, 1:-1]
                Vd=simu.VallExit#[1:-1, 1:-1]
                show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
                for door in simu.doors:
                    drawDirection(screen, door, door.arrow, ZOOMFACTOR, xSpace, ySpace)
            
        '''
        for i in range(dimX):
            for j in range(dimY):
                if simu.solver==1:
                    vec=np.array([simu.UallExit[i,j],simu.VallExit[i,j]])
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = startPos + VECFACTOR*normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
                if simu.solver==2:
                    vec=np.array([simu.UeachExit[i,j],simu.VeachExit[i,j]])
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = startPos + VECFACTOR*normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
        '''
        
        drawWalls(screen, simu.walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoors(screen, simu.doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, simu.exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)


        '''
        # pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(), agent.size, LINEWIDTH)

        ####################
        # Drawing the agents
        ####################
        
        for idai, agent in enumerate(simu.agents):
            
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
            pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            
            
            if simu.SHOWVELOCITY:
                #endPosV = [0, 0]
                #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
                #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
                endPosV = (agent.pos+agent.actualV)*ZOOMFACTOR+xyShift
            
                #endPosDV = [0, 0]
                #endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR+xSpace)
                #endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR+ySpace)
                endPosDV = (agent.pos+agent.desiredV)*ZOOMFACTOR+xyShift
            
            for idaj, agentOther in enumerate(simu.agents):
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
                
                if person.comm[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, blue, scPos, scPosOther, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)

                if person.talk[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, red, scPos, scPosOther, 3)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)
            
            #print(scPos)
        '''
        
        # Show Mouse Position
        (mouseX2, mouseY2) = pygame.mouse.get_pos()
        mouse_pos2 = np.array([mouseX2, mouseY2])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",16)
        text_surface=myfont.render(str((mouse_pos2-xyShift)*(1/ZOOMFACTOR)), True, tan, white)
        screen.blit(text_surface, mouse_pos2+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos2), True, lightblue, white)
        screen.blit(text_surface, mouse_pos2+[0.0, 36.0])
        
        # The Zoom and xSpace ySpace Info
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ZOOM:'+str(ZOOMFACTOR), True, black, white)
        screen.blit(text_surface, [500,3]) #+xyShift)
        text_surface=myfont.render('xSpace:'+str(xSpace), True, black, white)
        screen.blit(text_surface, [600,3]) #+xyShift)        
        text_surface=myfont.render('ySpace:'+str(ySpace), True, black, white)
        screen.blit(text_surface, [700,3]) #+xyShift) 
        
        time_surface=myfont.render("Help: Press <o> or <p> to show flow field", True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [500,23]) #[750,350]*ZOOMFACTOR)
        
        pygame.display.flip()
        clock.tick(20)

    f.close()
    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    #simu.walls = walls
    #simu.doors = doors
    #simu.exits = exits
    pygame.display.quit()



# Show simulation by pygame
def show_simu(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    f.write("Start and show simulation here.")
    # f.write('FN_FDS=', simu.FN_FDS)
    # f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print("Input data is not correct!  Please modify input data file!")
        return

    # Initialize prt file in draw_func.py
    if simu.dumpBin:
        #fbin = open(simu.fpath + '\\' +simu.outDataName +'.bin', 'wb+')
        fbin = open(simu.outDataName +'.bin', 'wb+')
        intiPrt(fbin, simu.num_agents)
        
        npzTime=[]
        npzSee = np.zeros((1, simu.num_agents, simu.num_agents))
        npzComm = np.zeros((1, simu.num_agents, simu.num_agents))
        npzTalk = np.zeros((1, simu.num_agents, simu.num_agents))
        
        npzP = np.zeros((1, simu.num_agents, simu.num_agents))
        npzD = np.zeros((1, simu.num_agents, simu.num_agents))
        npzA = np.zeros((1, simu.num_agents, simu.num_agents))
        npzB = np.zeros((1, simu.num_agents, simu.num_agents))
        npzC = np.zeros((1, simu.num_agents, simu.num_agents))
        
        #npzComm = [] #np.zeros((simu.num_agents, simu.num_agents, 1))
        #npzTalk = [] #np.zeros((simu.num_agents, simu.num_agents, 1))

        dump_evac(simu.agents, fbin, simu.t_sim)
        npzTime.append(simu.t_sim)

        if len(npzTime)==1:
            npzSee[0,:,:]=person.see_flag

        if len(npzTime)==1:
            npzComm[0,:,:]=person.comm

        if len(npzTime)==1:
            npzTalk[0,:,:]=person.talk

        if len(npzTime)==1:
            npzP[0,:,:]=person.PFactor
            
        if len(npzTime)==1:
            npzD[0,:,:]=person.DFactor

        if len(npzTime)==1:
            npzA[0,:,:]=person.AFactor

        if len(npzTime)==1:
            npzB[0,:,:]=person.BFactor
        
        if len(npzTime)==1:
            npzC[0,:,:]=person.CFactor


    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
    #walls = simu.walls
    #doors = simu.doors
    #exits = simu.exits

    exitIndex=-1
    #if simu.solver=1:
    #    (dimX,dimY)=np.shape(simu.UallExit)

    #if simu.solver=2:
    #    (dimX,dimY)=np.shape(simu.UeachExit)
    
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

    simu.t_sim = 0.0
    simu.tt_OtherList = 0.0
    #t_pause=0.0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.display.quit()
                simu.quit()
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
                    simu.MODETRAJ = not simu.MODETRAJ
                elif event.key == pygame.K_SPACE:
                    simu.PAUSE = not simu.PAUSE
                elif event.key == pygame.K_v:
                    simu.SHOWVELOCITY = not simu.SHOWVELOCITY
                elif event.key == pygame.K_i:
                    simu.SHOWINDEX = not simu.SHOWINDEX
                elif event.key == pygame.K_d:
                    simu.DRAWDOORFORCE = not simu.DRAWDOORFORCE
                elif event.key == pygame.K_r:
                    simu.DRAWSELFREPULSION = not simu.DRAWSELFREPULSION
                elif event.key == pygame.K_1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_s:
                    simu.SHOWSTRESS = not simu.SHOWSTRESS
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10
                elif event.key == pygame.K_o:
                    exitIndex=exitIndex+1
                elif event.key == pygame.K_p:
                    exitIndex=exitIndex-1

        if simu.MODETRAJ == False:
            screen.fill(white)

        tt = pygame.time.get_ticks()/1000-simu.t_pause
        if simu.PAUSE is True:
            t_now = pygame.time.get_ticks()/1000
            simu.t_pause = t_now-tt
            continue

        # Computation Step
        if simu.t_sim > 0.0:
            simu.simulation_update_agent_position()
        simu.simulation_step2022(f)
        #simu.t_sim = simu.t_sim + simu.DT  # Maybe it should be in step()
        #pass

        # Dump agent binary data file
        if simu.dumpBin and simu.t_sim > simu.tt_DumpData:
            dump_evac(simu.agents, fbin, simu.t_sim)
            simu.tt_DumpData = simu.tt_DumpData + simu.DT_DumpData
            npzTime.append(simu.t_sim)
            
            if len(npzTime)==1:
                npzSee[0,:,:]=person.see_flag
            else:
                tempSee=np.zeros((1, simu.num_agents, simu.num_agents))
                tempSee[0,:,:]=person.see_flag
                npzSee = np.concatenate((npzSee, tempSee), axis=0)
            
            if len(npzTime)==1:
                npzComm[0,:,:]=person.comm
            else:
                tempComm=np.zeros((1, simu.num_agents, simu.num_agents))
                tempComm[0,:,:]=person.comm
                npzComm = np.concatenate((npzComm, tempComm), axis=0) 
                
            if len(npzTime)==1:
                npzTalk[0,:,:]=person.talk
            else:
                tempTalk=np.zeros((1, simu.num_agents, simu.num_agents))
                tempTalk[0,:,:]=person.talk
                npzTalk = np.concatenate((npzTalk, tempTalk), axis=0)
                
            if len(npzTime)==1:
                npzP[0,:,:]=person.PFactor
            else:
                tempP=np.zeros((1, simu.num_agents, simu.num_agents))
                tempP[0,:,:] =person.PFactor
                npzP = np.concatenate((npzP, tempP), axis=0)
                
            if len(npzTime)==1:
                npzD[0,:,:]=person.DFactor
            else:
                tempD=np.zeros((1, simu.num_agents, simu.num_agents))
                tempD[0,:,:] =person.DFactor
                npzD = np.concatenate((npzD, tempD), axis=0)

            if len(npzTime)==1:
                npzA[0,:,:]=person.AFactor
            else:
                tempA=np.zeros((1, simu.num_agents, simu.num_agents))
                tempA[0,:,:] =person.AFactor
                npzA = np.concatenate((npzA, tempA), axis=0)

            if len(npzTime)==1:
                npzB[0,:,:]=person.BFactor
            else:
                tempB=np.zeros((1, simu.num_agents, simu.num_agents))
                tempB[0,:,:] =person.BFactor
                npzB = np.concatenate((npzB, tempB), axis=0)
                
            if len(npzTime)==1:
                npzC[0,:,:]=person.CFactor
            else:
                tempC=np.zeros((1, simu.num_agents, simu.num_agents))
                tempC[0,:,:] =person.CFactor
                npzC = np.concatenate((npzC, tempC), axis=0)
                
            #npzComm.append(person.comm)
            #npzTalk.append(person.talk)
            
            #print(npzTime)
            #print(npzSee)
            #UserInput = input("For debug!")
        
        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if simu.SHOWTIME:
            tt = pygame.time.get_ticks()/1000-simu.t_pause
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Physics Time:" + str(tt), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [100,3]) #[750,350]*ZOOMFACTOR)
            time_surface=myfont.render("Simulation Time:" + format(simu.t_sim, ".3f"), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [100,23]) #[750,350]*ZOOMFACTOR)

        if simu.solver!=0:
            show_mesh(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, simu.bldmesh, ZOOMFACTOR, xSpace, ySpace)
            
            # Show flow field in the background
            if simu.solver==1 and exitIndex%2==0: # and exitIndex==-1:
                Ud=simu.UallExit#[1:-1, 1:-1]
                Vd=simu.VallExit#[1:-1, 1:-1]
                show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
                for door in simu.doors:
                        drawDirection(screen, door, door.arrow, ZOOMFACTOR, xSpace, ySpace)
                        
            if simu.solver==2:
                #for idexit, exit in enumerate(simu.exits):
                #    if exitIndex%len(simu.exits) == idexit:
                #        Utemp = simu.UeachExit[idexit] 
                #        Vtemp = simu.VeachExit[idexit]
                #        Ud = Utemp[1:-1, 1:-1]
                #        Vd = Vtemp[1:-1, 1:-1]
                #show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
    
                idexit = exitIndex%(len(simu.exits)+2)
                if idexit < len(simu.exits):
                    Utemp = simu.UeachExit[idexit] 
                    Vtemp = simu.VeachExit[idexit]
                    Ud = Utemp#[1:-1, 1:-1]
                    Vd = Vtemp#[1:-1, 1:-1]
                    show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
                    for door in simu.doors:
                        drawDirection(screen, door, simu.exit2door[idexit, door.oid], ZOOMFACTOR, xSpace, ySpace)
                elif idexit == len(simu.exits):
                    # Show nearest-exit field
                    Ud=simu.UallExit#[1:-1, 1:-1]
                    Vd=simu.VallExit#[1:-1, 1:-1]
                    show_vel(screen, simu.xmin, simu.ymin, simu.xmax, simu.ymax, simu.xpt, simu.ypt, Ud, Vd, ZOOMFACTOR, xSpace, ySpace)
                    for door in simu.doors:
                        drawDirection(screen, door, door.arrow, ZOOMFACTOR, xSpace, ySpace)
                
        '''
        for i in range(dimX):
            for j in range(dimY):
                if simu.solver==1:
                    vec=np.array([simu.UallExit[i,j],simu.VallExit[i,j]])
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = startPos + VECFACTOR*normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
                if simu.solver==2:
                    vec=np.array([simu.UeachExit[i,j],simu.VeachExit[i,j]])
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = startPos + VECFACTOR*normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)

        '''
        
        drawWalls(screen, simu.walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoors(screen, simu.doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, simu.exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)

        # pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(), agent.size, LINEWIDTH)
        
        ####################
        # Drawing the agents
        ####################
        #for agent in agents:
        
        for idai, agent in enumerate(simu.agents):
            
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
            if simu.t_sim < agent.tpre:
                try:
                    pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH+3)
                except:
                    #pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH+3)
                    pygame.draw.circle(screen, color_para, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH+3)
                    #int(agent.radius*ZOOMFACTOR), LINEWIDTH+3)
            else:
                try:
                    pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
                except:
                    pygame.draw.circle(screen, color_para, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
                #int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            
            if simu.THREECIRCLES:
                leftS = [0, 0]
                leftShoulder = agent.shoulders()[0]
                leftS[0] = int(leftShoulder[0]*ZOOMFACTOR+xSpace)
                leftS[1] = int(leftShoulder[1]*ZOOMFACTOR+ySpace)
            
                rightS = [0, 0]
                rightShoulder = agent.shoulders()[1]	
                rightS[0] = int(rightShoulder[0]*ZOOMFACTOR+xSpace)
                rightS[1] = int(rightShoulder[1]*ZOOMFACTOR+ySpace)
                
                #print ('shoulders:', leftS, rightS)
                pygame.draw.circle(screen, color_para, leftS, agent.size/2, 3)
                pygame.draw.circle(screen, color_para, rightS, agent.size/2, 3)
            
            if simu.SHOWVELOCITY:
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

            if simu.DRAWWALLFORCE:
                #endPosV = [0, 0]
                #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
                #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
                endPosWF = (agent.pos+agent.wallrepF)*ZOOMFACTOR+xyShift
            
                #pygame.draw.line(screen, blue, scPos, endPosV, 2)
                #pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
                pygame.draw.line(screen, purple, scPos, endPosWF, 2)
                #khaki = 240,230,140

            if simu.DRAWDOORFORCE:
                endPosDF = (agent.pos+agent.doorF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, green, scPos, endPosDF, 2)

            if simu.DRAWGROUPFORCE:
                endPosGF = (agent.pos+agent.socialF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

            if simu.DRAWSELFREPULSION:
                endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, cyan, scPos, endPosRF, 2)
                
            
            for idaj, agentOther in enumerate(simu.agents):
                scPosOther = [0, 0]
                scPosOther[0] = int(agentOther.pos[0]*ZOOMFACTOR+xSpace)
                scPosOther[1] = int(agentOther.pos[1]*ZOOMFACTOR+ySpace)
                
                agentPer = agent.pos+0.8*normalize(agentOther.pos - agent.pos)
                scPosDir = [0, 0]
                scPosDir[0] = int(agentPer[0]*ZOOMFACTOR+xSpace)
                scPosDir[1] = int(agentPer[1]*ZOOMFACTOR+ySpace)
                
                leftShoulder, rightShoulder = agent.shoulders()
                leftS = [int(leftShoulder[0]*ZOOMFACTOR), int(leftShoulder[1]*ZOOMFACTOR)]
                rightS = [int(rightShoulder[0]*ZOOMFACTOR), int(rightShoulder[1]*ZOOMFACTOR)]

                if person.see_flag[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, lightpink, scPos, scPosOther, 2)
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 2)
                
                if person.comm[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, tan, scPos, scPosOther, 5)
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 5)

                if person.talk[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, magenta, scPos, scPosOther, 6)
                    pygame.draw.line(screen, green, scPos, scPosDir, 6)
                    #pygame.draw.line(screen, green, scPosDir, leftS, 4)
                    #pygame.draw.line(screen, green, scPosDir, rightS, 4)
            
            #print(scPos)
            
            if simu.SHOWINDEX:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",14)
                if simu.t_sim < agent.tpre:
                    text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
                else: 
                    text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

            if simu.SHOWSTRESS:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(format(agent.ratioV, ".3f"), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift+[0,6])
        
        
        # The Zoom and xSpace ySpace Info
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ZOOM:'+str(ZOOMFACTOR), True, black, white)
        screen.blit(text_surface, [500,3]) #+xyShift)
        text_surface=myfont.render('xSpace:'+str(xSpace), True, black, white)
        screen.blit(text_surface, [600,3]) #+xyShift)        
        text_surface=myfont.render('ySpace:'+str(ySpace), True, black, white)
        screen.blit(text_surface, [700,3]) #+xyShift) 
        text_surface=myfont.render('solver:'+str(simu.solver), True, black, white)
        screen.blit(text_surface, [800,3]) #+xyShift) 
        
        pygame.display.flip()
        clock.tick(20)

    f.close()
    
    npzRadius = []
    npzMass = []
    for agent in simu.agents:
        npzRadius.append(agent.radius)
        npzMass.append(agent.mass)
    
    if simu.dumpBin:
        fbin.close()
        np.savez(simu.outDataName +'.npz', npzTime, npzSee, npzComm, npzTalk, npzP, npzD, npzC, npzB, npzA, npzRadius, npzMass)
       
    #np.histogram() ??
    
    #if len(simu.exits)>0:
        #plt.bar(np.arange(len(simu.exits)), simu.exitUsage)
        #plt.title("Exit Usage Histogram:")
        #plt.grid()
        #plt.legend(loc='best')
        #plt.xlabel("Exit_Index")
        #plt.ylabel("Num_of_Agents")
        #plt.show()
    
    visualizeTpre(simu.outDataName +'.bin')
    
    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    #simu.walls = walls
    #simu.doors = doors
    #simu.exits = exits
    pygame.display.quit()




if __name__=="__main__":

    print("=======================")
    print("A Test Case for Draw Geometry")
    from obst import *
    #from passage import *
    #from outlet import *

    # initialize OBST
    obstFeatures = readCSV("./test_case/obstData2018.csv", "string")
    walls = []
    index = 0
    for obstFeature in obstFeatures:
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.mode = obstFeature[4]
        wall.name = str(obstFeature[5])
        wall.inComp = int(obstFeature[6])
        wall.arrow = int(obstFeature[7])
        #wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
        #wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
        wall.oid = index
        index = index+1
        walls.append(wall)


    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Test of This Package')
    clock = pygame.time.Clock()
    #screen.fill(BACKGROUNDCOLOR)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    t_pause=0.0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                
        ####################################
        # Drawing the geometries: walls, doors, exits
        ####################################
        drawWalls(screen, walls)
        #drawDoors(screen, doors)
        #drawExits(screen, exits)
        
        pygame.display.flip()
        clock.tick(20)


def show_agents_npz(filename, evacfile=None, fdsfile=None, ZOOMFACTOR=10.0, xSpace=20.0, ySpace=20.0, Zmin=0.0, Zmax=3.0, debug=True):
    
    # Read in data from filename
    agentdata=np.load(filename)
    npzTime = agentdata["arr_0"]
    npzAgent = agentdata["arr_1"]
    
    if debug:
        print('\n Basic info: \n')
        print('Time points:', np.size(npzTime), '\n')
        print('Time points for agents:', np.size(npzAgent), '\n')

    T_END = len(npzTime)
    if debug:
        print ("Length of time axis in npz data file/T_END:", T_END)
        print ("T_Initial=", npzTime[0])
        print ("T_Final=", npzTime[T_END-1])
    T_INDEX=0

    if evacfile!="" and evacfile!="None" and evacfile is not None:
        walls = readWalls(evacfile)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
        doors = readDoors(evacfile)
        exits = readExits(evacfile)

    if fdsfile!="" and fdsfile!="None" and fdsfile is not None:
        #meshes, evacZmin, evacZmax = readMESH(fdsfile, 'evac')
        #N_meshes = len(meshes)
        #evacZoffset=0.5*(evacZmin+evacZmax)
        
        walls=readOBST(fdsfile, '&OBST', Zmin, Zmax)
        doors=readPATH(fdsfile, '&HOLE', Zmin, Zmax) #+readPATH(fdsfile, '&DOOR', Zmin, Zmax)
        exits=readEXIT(fdsfile, '&EXIT', Zmin, Zmax)
        #doors=doors+readPATH(fdsfile, '&DOOR', Zmin, Zmax)
        #entries=readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
    
    MODETRAJ=False
    SHOWTIME=True

    SHOWVELOCITY=True
    SHOWINDEX=True
    SHOWFORCE=True
    SHOWSTRESS=True
    
    SHOWWALLDATA=True
    SHOWDOORDATA=True
    SHOWEXITDATA=True
    
    PAUSE=True
    REWIND=False
    FORWARD=False
    TimeInterval=20
    
    pygame.init()
    screen = pygame.display.set_mode([800, 550])
    pygame.display.set_caption('Visualize data file for agent-based simulation')
    clock = pygame.time.Clock()
    #screen.fill(white)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
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
                elif event.key == pygame.K_HOME:
                    REWIND = True
                    PAUSE = True
                    #xSpace=xSpace-10
                elif event.key == pygame.K_END:
                    FORWARD = True
                    PAUSE = True
                    #xSpace=xSpace+10
                    
                elif event.key == pygame.K_v:
                    SHOWVELOCITY = not SHOWVELOCITY
                elif event.key == pygame.K_i:
                    SHOWINDEX = not SHOWINDEX
                elif event.key == pygame.K_f:
                    SHOWFORCE = not SHOWFORCE
                #elif event.key == pygame.K_r:
                #    DRAWSELFREPULSION = not DRAWSELFREPULSION
                
                elif event.key == pygame.K_1:
                    SHOWWALLDATA = not SHOWWALLDATA
                elif event.key == pygame.K_2:
                    SHOWDOORDATA = not SHOWDOORDATA
                elif event.key == pygame.K_3:
                    SHOWEXITDATA = not SHOWEXITDATA
                #elif event.key == pygame.K_s:
                #    SHOWSTRESS = not SHOWSTRESS
                
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10

                elif event.key ==pygame.K_PERIOD:
                    TimeInterval = TimeInterval + 10
                elif event.key == pygame.K_COMMA:
                    TimeInterval = TimeInterval - 10                    

        if MODETRAJ == False:
            screen.fill([0,0,0])

        #Time  = readFRec(fin,'f')  # Time index
        if T_INDEX == None or T_INDEX==T_END-1:
            #print("Simulation End!")
            #running=False
            #pygame.display.quit()
            #PAUSE=True
            T_INDEX=0
        else:
            if PAUSE==False:
                T_INDEX = T_INDEX+1
            else:
                if REWIND and T_INDEX>0:
                    T_INDEX = T_INDEX-1
                if FORWARD and T_INDEX<T_END-1:
                    T_INDEX = T_INDEX+1
        #nplim = readFRec(fin,'I')  # Number of particles in the PART class
        
        Time_t = npzTime[T_INDEX]
        agent_t = npzAgent[T_INDEX]

        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if SHOWTIME:
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Simulation Time:" + str(Time_t), True, yellow, black)
            screen.blit(time_surface, [620,300]) #[750,350]*ZOOMFACTOR)

        drawWalls(screen, walls, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
        #drawPATH(screen, holes, green, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, exits, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        #drawPATH(screen, entries, purple, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        #if np.size(TAG_t)==1:
        #    TAG_t = np.array([TAG_t])
            
        #if debug:
        #    print ("Show TAG_t: ", TAG_t)
        
        # Show Mouse Position
        (mouseX3, mouseY3) = pygame.mouse.get_pos()
        mouse_pos3 = np.array([mouseX3, mouseY3])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",16)
        text_surface=myfont.render(str((mouse_pos3-xyShift)*(1/ZOOMFACTOR)), True, black, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos3), True, tan, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 36.0])

        for idai, agent in enumerate(agent_t):
            
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
            if Time_t < agent.tpre:
                pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH+2)
            else:
                pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)

            '''
            if simu.THREECIRCLES:
                leftS = [0, 0]
                leftShoulder = agent.shoulders()[0]
                leftS[0] = int(leftShoulder[0]*ZOOMFACTOR+xSpace)
                leftS[1] = int(leftShoulder[1]*ZOOMFACTOR+ySpace)
            
                rightS = [0, 0]
                rightShoulder = agent.shoulders()[1]	
                rightS[0] = int(rightShoulder[0]*ZOOMFACTOR+xSpace)
                rightS[1] = int(rightShoulder[1]*ZOOMFACTOR+ySpace)
                
                #print ('shoulders:', leftS, rightS)
                pygame.draw.circle(screen, color_para, leftS, agent.size/2, 3)
                pygame.draw.circle(screen, color_para, rightS, agent.size/2, 3)
            '''
            
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
                pygame.draw.line(screen, tan, scPos, endPosV, 2)
                pygame.draw.line(screen, yellow, scPos, endPosDV, 2)

            if SHOWFORCE:
                #endPosV = [0, 0]
                #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
                #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
                endPosWF = (agent.pos+agent.wallrepF)*ZOOMFACTOR+xyShift
            
                #pygame.draw.line(screen, blue, scPos, endPosV, 2)
                #pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
                pygame.draw.line(screen, purple, scPos, endPosWF, 2)
                #khaki = 240,230,140

            #if DRAWDOORFORCE:
                endPosDF = (agent.pos+agent.doorF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, green, scPos, endPosDF, 2)

            #if DRAWGROUPFORCE:
                endPosGF = (agent.pos+agent.socialF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

            #if DRAWSELFREPULSION:
                endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, cyan, scPos, endPosRF, 2)
                
            '''
            for idaj, agentOther in enumerate(agent_t):
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
                
                if person.comm[idai, idaj] == 1: #and SHOWINTELINE: 
                    pygame.draw.line(screen, lightpink, scPos, scPosOther, 2)
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)

                if person.talk[idai, idaj] == 1: #and SHOWINTELINE: 
                    pygame.draw.line(screen, magenta, scPos, scPosOther, 3)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)
            '''
            #print(scPos)
            
            if SHOWINDEX:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",14)
                if Time_t < agent.tpre:
                    text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
                else: 
                    text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

            if SHOWSTRESS:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(format(agent.ratioV, "3f"), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift+[0,6])
        
        
        # The Zoom and xSpace ySpace Info
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ZOOM:'+str(ZOOMFACTOR), True, black, white)
        screen.blit(text_surface, [500,3]) #+xyShift)
        text_surface=myfont.render('xSpace:'+str(xSpace), True, black, white)
        screen.blit(text_surface, [600,3]) #+xyShift)        
        text_surface=myfont.render('ySpace:'+str(ySpace), True, black, white)
        screen.blit(text_surface, [700,3]) #+xyShift) 
        
        pygame.display.flip()
        clock.tick(TimeInterval)
        

def visualizeCrowdfluid(filename, debug=True):
    
    temp=os.path.split(filename)
    print(temp)
        
    if temp[1] == 'vel_flow1.npz':
        # Read in data from filename
        flowdata=np.load(filename)
        Ud0 = flowdata["arr_0"]
        Vd0 = flowdata["arr_1"]
        R = flowdata["arr_2"]
        U = flowdata["arr_3"]
        V = flowdata["arr_4"]
        BLDinfo = flowdata["arr_5"]
        [x_min, y_min, x_max, y_max, x_points, y_points] = flowdata["arr_6"]
        
        (dimX,dimY,dimT)=np.shape(R)
        print(np.shape(BLDinfo))
        print(np.shape(Ud0))
        print(np.shape(R))
        flag='flow1'

    if temp[1] == 'vel_flow2.npz':
        flowdata=np.load(filename)
        Ud0 = flowdata["arr_0"]
        Vd0 = flowdata["arr_1"]
        U = flowdata["arr_2"]
        V = flowdata["arr_3"]
        BLDinfo = flowdata["arr_4"]
        [x_min, y_min, x_max, y_max, x_points, y_points] = flowdata["arr_5"]
        (dimX,dimY)=np.shape(Ud0)
        dimT = 1
        print(np.shape(BLDinfo))
        print(np.shape(Ud0))
        flag='flow2'
        
    D_x = (x_max - x_min)/float(x_points-1)
    D_y = (y_max - y_min)/float(y_points-1)

    if debug:
        print('\n Basic mesh info: \n')
        print('x_points:', x_points, '\n')
        print('y_points:', y_points, '\n')
        print('x_min:', x_min, '\n')
        print('x_max:', x_max, '\n')
        print('y_min:', y_min, '\n')
        print('y_max:', y_max, '\n')
        print('dx', D_x, '\n')
        print('dy', D_y, '\n')
        print("(dimX,dimY)", np.shape(BLDinfo), '\n')
        if sys.version_info[0] == 2: 
            raw_input('Please check input data here!')
            #UserInput = raw_input('Check Input Data Here!')
        if sys.version_info[0] == 3:
            UserInput =input('Please check input data here!')


    if dimX!=x_points+2 or dimY!=y_points+2:
        print("Error in dimension of input data!")
        if sys.version_info[0] == 2: 
            raw_input('Please check input data here!')
            #UserInput = raw_input('Check Input Data Here!')
        if sys.version_info[0] == 3:
            UserInput =input('Please check input data here!')

    #x_points=dimX
    #y_points=dimY
    #xDim=np.linspace(0, x_points*D_x, x_points+2) #Should be the same as x
    #yDim=np.linspace(0, y_points*D_y, y_points+2) #Should be the same as y

    xDim=np.linspace(x_min-D_x, x_max+D_x, x_points+2) #Should be the same as x
    yDim=np.linspace(y_min-D_y, y_max+D_y, y_points+2) #Should be the same as y
    
    if debug:
        print("Dim info:\n")
        print(xDim)
        print(yDim)
        
    if sys.version_info[0] == 2: 
        raw_input('Please check input data here!')
        #UserInput = raw_input('Check Input Data Here!')
    if sys.version_info[0] == 3:
        UserInput =input('Please check input data here!')
    #fig = plt.figure()
    #ax = fig.gca(projection = '3d')
    #X,Y = np.meshgrid(xDim,yDim)

    SCREENSIZE = [1600, 1600]
    RESOLUTION = 180
    BACKGROUNDCOLOR = [255,255,255]
    LINECOLOR = [255,0,0]
    ZOOMFACTOR = 90.0
    VECFACTOR = 0.2
    PAUSE=False
    REWIND=False
    FORWARD=False
    xSpace=90.0
    ySpace=90.0
    TimeInterval=60
    
    SHOWGHOSTBLD=True
    SHOWUVDesired=True
    #SHOWSINK=True

    T_END=dimT
    T_INDEX=0 #0...dimT-1

    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Crowd Flow Model')
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # event.type == pygame.MOUSEBUTTONUP:
                
                ### Menu No 1: Show Ghost and BLD Cell ###
                if mouseX<60 and mouseX>0 and mouseY<20 and mouseY>3:
                    SHOWGHOSTBLD = not SHOWGHOSTBLD
                
                if mouseX<125 and mouseX>70 and mouseY<20 and mouseY>3:
                    SHOWUVDesired = not SHOWUVDesired

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                elif event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                elif event.key == pygame.K_HOME:
                    REWIND = True
                    PAUSE = True
                elif event.key == pygame.K_END:
                    FORWARD = True
                    PAUSE = True
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10
                elif event.key ==pygame.K_PERIOD:
                    TimeInterval = TimeInterval + 10
                elif event.key == pygame.K_COMMA:
                    TimeInterval = TimeInterval - 10
                elif event.key == pygame.K_1:
                    SHOWGHOSTBLD = not SHOWGHOSTBLD
                elif event.key == pygame.K_2:
                    SHOWUVDesired = not SHOWUVDesired




        screen.fill(BACKGROUNDCOLOR)
        xyShift = np.array([xSpace, ySpace])
        
        #--------Menu Bar at Top Left-----------
        #pygame.draw.rect(screen, tan, [720, 3, 60, 20], LINEWIDTH)
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('SHOWBLD', True, white, tan)
        screen.blit(text_surface, [0,3]) #+xyShift)

        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ShowVdUd', True, white, tan)
        screen.blit(text_surface, [80,3]) #+xyShift)
        
        myfont=pygame.font.SysFont("arial",14)
        time_surface=myfont.render("xmin:" + str(x_min), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [620,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("xmax:" + str(x_max), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [620,23]) #[750,350]*ZOOMFACTOR)

        time_surface=myfont.render("ymin:" + str(y_min), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [700,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("ymax:" + str(y_max), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [700,23]) #[750,350]*ZOOMFACTOR)

        time_surface=myfont.render("num of x points:" + str(x_points), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [800,3]) #[750,350]*ZOOMFACTOR)
        time_surface=myfont.render("num of y points:" + str(y_points), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [800,23]) #[750,350]*ZOOMFACTOR)

        # Show Mouse Position
        (mouseX3, mouseY3) = pygame.mouse.get_pos()
        mouse_pos3 = np.array([mouseX3, mouseY3])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",16)
        text_surface=myfont.render(str((mouse_pos3-xyShift)*(1/ZOOMFACTOR)), True, black, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos3), True, lightblue, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 36.0])
        
        # Show data in the mesh 
        iii=int(ceil(((mouse_pos3[0]-xSpace)*(1/ZOOMFACTOR)-x_min)/D_x))
        jjj=int(ceil(((mouse_pos3[1]-ySpace)*(1/ZOOMFACTOR)-y_min)/D_y))
        
        if iii>=0 and iii <dimX and jjj>=0 and jjj<dimY:
            myfont=pygame.font.SysFont("arial",20)
            text_surface=myfont.render("R:"+str(R[iii, jjj, T_INDEX]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 56.0])
            text_surface=myfont.render("U:"+str(U[iii, jjj, T_INDEX]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 79.0])
            text_surface=myfont.render("V:"+str(V[iii, jjj, T_INDEX]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 103.0])
            text_surface=myfont.render("Ud:"+str(Ud0[iii, jjj]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 123.0])
            text_surface=myfont.render("Vd:"+str(Vd0[iii, jjj]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 143.0])
            text_surface=myfont.render("BLD:"+str(BLDinfo[iii, jjj]), True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 169.0])
        else: 
            myfont=pygame.font.SysFont("arial",20)
            text_surface=myfont.render("Out of data boundary", True, black, white)
            screen.blit(text_surface, mouse_pos3+[0.0, 56.0])
        
        # The Zoom and xSpace ySpace Info
        myfont=pygame.font.SysFont("arial",14)
        text_surface=myfont.render('ZOOM:'+str(ZOOMFACTOR), True, black, white)
        screen.blit(text_surface, [500,3]) #+xyShift)
        text_surface=myfont.render('xSpace:'+str(xSpace), True, black, white)
        screen.blit(text_surface, [600,3]) #+xyShift)        
        text_surface=myfont.render('ySpace:'+str(ySpace), True, black, white)
        screen.blit(text_surface, [700,3]) #+xyShift) 
        
        time_surface=myfont.render("Help: Press <o> or <p> to show flow field", True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [500,23]) #[750,350]*ZOOMFACTOR)

        if SHOWGHOSTBLD:
            # draw grid and ghost cell
            for i in range(dimX):
                for j in range(dimY):
                    if i==0 or i==dimX-1 or j==0 or j==dimY-1:
                        ghostcellpos=np.array([xDim[i],yDim[j]])
                        pygame.draw.line(screen, tan, ghostcellpos*ZOOMFACTOR-[0,0.6]+xyShift, ghostcellpos*ZOOMFACTOR+[0,0.6]+xyShift, 15)
                        #ghostcellpos=np.array([xDim[i],yDim[j]])
                        pygame.draw.line(screen, tan, ghostcellpos*ZOOMFACTOR-[0.6,0]+xyShift, ghostcellpos*ZOOMFACTOR+[0.6,0]+xyShift, 15)

            # draw build info mesh
            for i in range(dimX):
                for j in range(dimY):
                    if BLDinfo[i,j]==0:
                        ghostcellpos=np.array([xDim[i],yDim[j]])
                        pygame.draw.line(screen, cyan, ghostcellpos*ZOOMFACTOR-[0,0.6]+xyShift, ghostcellpos*ZOOMFACTOR+[0,0.6]+xyShift, 15)
                        #ghostcellpos=np.array([xDim[i],yDim[j]])
                        pygame.draw.line(screen, cyan, ghostcellpos*ZOOMFACTOR-[0.6,0]+xyShift, ghostcellpos*ZOOMFACTOR+[0.6,0]+xyShift, 15)
                    else:
                        fieldcell=np.array([0,0])
                        fieldcell[0]=int(xDim[i]*ZOOMFACTOR+xSpace)
                        fieldcell[1]=int(yDim[j]*ZOOMFACTOR+ySpace)
                        pygame.draw.circle(screen, red, fieldcell, 2, 2)
        
        if REWIND:
            T_INDEX=T_INDEX-1
        if FORWARD:
            T_INDEX=T_INDEX+1
        
        if PAUSE:
            REWIND = False
            FORWARD = False
        else:
            T_INDEX=T_INDEX+1

        #T_INDEX=T_INDEX+1
        t=T_INDEX
        if T_INDEX == dimT-1: #T_END-1:
            T_INDEX = 0 
        for i in range(dimX):
            for j in range(dimY):
                #if i==0 or j==0:
                #    continue
                #else:
                if flag == 'flow1':
                    vec=np.array([U[i,j,t],V[i,j,t]])
                    density=R[i,j,t]
                    if debug:
                        print(t, i, j, vec, density)
                    ds_ratio=int(density*1e+2)#%10
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = np.array([xDim[i],yDim[j]]) + VECFACTOR*vec  # normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
                    #pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, int(3*density))
                    #pygame.draw.circle(screen, [255,200,0], startPos*ZOOMFACTOR, 3, 6)
                    if ds_ratio >=0:
                        pygame.draw.line(screen, black, startPos*ZOOMFACTOR-[0,0.6]+xyShift, startPos*ZOOMFACTOR+[0,0.6]+xyShift, ds_ratio)
                    else:
                        pygame.draw.line(screen, tan, startPos*ZOOMFACTOR-[0,0.6]+xyShift, startPos*ZOOMFACTOR+[0,0.6]+xyShift, -ds_ratio)
                    
                    # In future desired velocity could be time-varying
                    if SHOWUVDesired:
                        # Draw desired velocity vector
                        vecDesired=np.array([Ud0[i,j],Vd0[i,j]])            
                        startPos = np.array([xDim[i],yDim[j]])
                        endPos = np.array([xDim[i],yDim[j]]) + VECFACTOR*vecDesired #normalize(vecDesired)
                        pygame.draw.line(screen, purple, startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)

                if flag == 'flow2':
                    pass
                    
            #scPos = agent.pos*10 #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            #scPos = [0, 0]
            #scPos[0] = int(agent.pos[0]*ZOOMFACTOR) #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            #scPos[1] = int(agent.pos[1]*ZOOMFACTOR)
            #AGENTSIZE = int(agent.radius)
            #pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
            
            #print(scPos)
            
        pygame.display.flip()
        clock.tick(TimeInterval)




def visualizeTpre(fname, evacfile=None, fdsfile=None, Zmin=0.0, Zmax=3.0, showdata=True):
    
    # Plot pre-movement time by using matplotlib
 

    # np.load has some unexpected problem for latest version of numpy in python3.  Thus I will not use this stuff.  
    # If anyone wants to help to debug the following lines, I will appreciate.  
    
    #prtdata = np.load(fname) #load .npz file
    #Time = prtdata["arr_0"]
    #XYZ = prtdata["arr_1"]
    #TAG = prtdata["arr_2"]
    #INFO = prtdata["arr_3"]
    #print("TAG:", TAG)
     
    # Extract data from binary data file
    Time, XYZ, TAG, INFO, n_part, n_agents, n_quant = readPRTfile(fname)
    T_END = len(Time)
    print('T_END:', T_END)

    T_INDEX=0
    arrayTpre = np.zeros((n_agents, T_END))  
             
    for T_INDEX in range(T_END):
        
        Time_t = Time[T_INDEX]
        XYZ_t = XYZ[T_INDEX]
        TAG_t = TAG[T_INDEX]
        INFO_t = INFO[T_INDEX]
        
        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
        print(TAG_t)
        
        for idai in range(np.size(TAG_t)):
            #print(TAG_t[idai])
            arrayTpre[int(TAG_t[idai]), T_INDEX] = INFO_t[14][idai]
    
    print('Shape of arrayTpre:', np.shape(arrayTpre))
    print('arrayTpre:', arrayTpre)
    
    (NRow, NColomn) = np.shape(arrayTpre)  
    if showdata:
        for i in range(NRow):
            plt.plot(Time, arrayTpre[i,:], linewidth=2.0, label=str(i))
            #plt.plot(arrayTpre[i,:], linewidth=3.0, label=str(i))
            plt.text(0, arrayTpre[i,0], str(i), fontsize=18)
        #plt.plot(arrayTpre)
        plt.title("Pre-movement Time")
        plt.grid()
        plt.legend(loc='best')
        plt.show()
    return arrayTpre            


def visualizeEvac(fname, evacfile=None, fdsfile=None, ZOOMFACTOR=10.0, xSpace=20.0, ySpace=20.0, Zmin=0.0, Zmax=3.0, debug=False):
    
    # Because visualizeEvac is a 2D visualizer, we can only show agents in a single floors each time and if there are multiple floors in fds+evac simulation, users should specify which floor they want to visualize.  Otherwise there will be overlap of agents in different floors.  The default values are given by Zmin=0.0 and Zmax=3.0, which means the gound floor approximately.  
 
     # Therefore It is recommended for users to first open .fds input file to see if there are multiple floors.  User should specify Zmin and Zmax and agents are visualized in z axis between Zmin and Zmax.  
        
    #Zmin is the lower bound of z values in a floor (e.g., often z lower bound of an evacuation mesh)
    #Zmax is the upper bound of z values in a floor (e.g., often z upper bound of an evacuation mesh)


    # np.load has some unexpected problem for latest version of numpy in python3.  Thus I will not use this stuff.  
    # If anyone wants to help to debug the following lines, I will appreciate.  
    
    #prtdata = np.load(fname) #load .npz file
    #Time = prtdata["arr_0"]
    #XYZ = prtdata["arr_1"]
    #TAG = prtdata["arr_2"]
    #INFO = prtdata["arr_3"]
    #print("TAG:", TAG)
     
    # Extract data from binary data file
    Time, XYZ, TAG, INFO, n_part, n_agents, n_quant = readPRTfile(fname)

    temp=fname.split('.')
    fnameNPZ = temp[0]+'.npz'
    fnameCSV = temp[0]+'.csv'
    fnameTXT = temp[0]+'.txt' 
    
    
    #if simu.dumpBin:
    #    fbin.close()
    #    np.savez(simu.outDataName +'.npz', npzTime, npzSee, npzComm, npzTalk, npzP, npzD, npzC, npzB, npzA, npzRadius, npzMass)
       
    # Read in data from npz matrix data file
    if os.path.exists(fnameNPZ):
        try:
            agentdata=np.load(fnameNPZ)
            npzTime = agentdata["arr_0"]
            npzSee = agentdata["arr_1"]
            npzComm = agentdata["arr_2"]
            npzTalk = agentdata["arr_3"]
            npzP = agentdata["arr_4"]
            npzD = agentdata["arr_5"]
            npzC = agentdata["arr_6"]
            npzB = agentdata["arr_7"]
            npzA = agentdata["arr_8"]
            npzRadius = agentdata["arr_9"]
            npzMass = agentdata["arr_10"]
        except:
            agentdata=np.load(fnameNPZ)
            npzTime = agentdata["arr_0"]
            npzSee = agentdata["arr_1"]
            npzComm = agentdata["arr_2"]
            npzTalk = agentdata["arr_3"]
            npzP = agentdata["arr_4"]
            npzD = agentdata["arr_5"]
            npzC = agentdata["arr_6"]
            npzB = agentdata["arr_7"]
            npzA = agentdata["arr_8"]
            
        T_END_Check = len(npzTime)
        npzflag=True
    else:
        T_END_Check = len(Time)
        npzflag=False
    
    T_END = len(Time)
    print('T_END_npz:', T_END_Check)
    print('T_END:', T_END)
    
    if T_END != T_END_Check and debug:
        if sys.version_info[0] == 2:
            raw_input('\nWarning: T_END_BIN != T_END_NPZ \n Please check!')
        if sys.version_info[0] == 3:
            input('\nWarning: T_END_BIN != T_END_NPZ \n Please check!')
    
    if debug:
        print ("Length of time axis in prt5 data file", T_END, T_END_Check)
        print ("T_Initial=", Time[0])
        print ("T_Final=", Time[T_END-1])
    T_INDEX=0

    if evacfile!="" and evacfile!="None" and evacfile is not None:
        walls = readWalls(evacfile)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
        doors = readDoors(evacfile)
        exits = readExits(evacfile)

    if fdsfile!="" and fdsfile!="None" and fdsfile is not None:
        #meshes, evacZmin, evacZmax = readMESH(fdsfile, 'evac')
        #N_meshes = len(meshes)
        #evacZoffset=0.5*(evacZmin+evacZmax)
        
        walls=readOBST(fdsfile, '&OBST', Zmin, Zmax)
        doors=readPATH(fdsfile, '&HOLE', Zmin, Zmax) #+readPATH(fdsfile, '&DOOR', Zmin, Zmax)+readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
        exits=readEXIT(fdsfile, '&EXIT', Zmin, Zmax)
        #doors=doors+readPATH(fdsfile, '&DOOR', Zmin, Zmax)
        #entries=readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
    
    if os.path.exists(fnameCSV):
        walls = readWalls(fnameCSV)
        doors = readDoors(fnameCSV)
        exits = readExits(fnameCSV)
        
    
    MODETRAJ=False
    SHOWTIME=True

    SHOWVELOCITY=True
    SHOWINDEX=True
    SHOWFORCE=False
    SHOWTPRE=False
    SHOWRATIOV=False
    SHOWSTRESS=False
    
    SHOWWALLDATA=True
    SHOWDOORDATA=False
    SHOWEXITDATA=True
    
    PAUSE=True
    REWIND=False
    FORWARD=False
    TimeInterval=60
    
    agentIndex=-1
    
    pygame.init()
    screen = pygame.display.set_mode([900, 650])
    pygame.display.set_caption('Visualize data file for evac simulation')
    clock = pygame.time.Clock()
    #screen.fill(white)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
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
                elif event.key == pygame.K_HOME:
                    REWIND = True
                    PAUSE = True
                    #xSpace=xSpace-10
                elif event.key == pygame.K_END:
                    FORWARD = True
                    PAUSE = True
                    #xSpace=xSpace+10
                    
                elif event.key == pygame.K_v:
                    SHOWVELOCITY = not SHOWVELOCITY
                elif event.key == pygame.K_i:
                    SHOWINDEX = not SHOWINDEX
                elif event.key == pygame.K_f:
                    SHOWFORCE = not SHOWFORCE
                elif event.key == pygame.K_r:
                    SHOWTPRE = not SHOWTPRE
                
                elif event.key == pygame.K_1:
                    SHOWWALLDATA = not SHOWWALLDATA
                elif event.key == pygame.K_2:
                    SHOWDOORDATA = not SHOWDOORDATA
                elif event.key == pygame.K_3:
                    SHOWEXITDATA = not SHOWEXITDATA
                #elif event.key == pygame.K_s:
                #    SHOWSTRESS = not SHOWSTRESS
                
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10

                elif event.key ==pygame.K_PERIOD:
                    TimeInterval = TimeInterval + 10
                elif event.key == pygame.K_COMMA:
                    TimeInterval = TimeInterval - 10
                    
                elif event.key == pygame.K_o:
                    agentIndex=agentIndex+1
                elif event.key == pygame.K_p:
                    agentIndex=agentIndex-1
                    

        if MODETRAJ == False:
            screen.fill([0,0,0])

        #Time  = readFRec(fin,'f')  # Time index
        if T_INDEX == None or T_INDEX==T_END-1:
            #print("Simulation End!")
            #running=False
            #pygame.display.quit()
            #PAUSE=True
            T_INDEX=0
        else:
            if PAUSE==False:
                T_INDEX = T_INDEX+1
            else:
                if REWIND and T_INDEX>0:
                    T_INDEX = T_INDEX-1
                if FORWARD and T_INDEX<T_END-1:
                    T_INDEX = T_INDEX+1
        #nplim = readFRec(fin,'I')  # Number of particles in the PART class
        
        Time_t = Time[T_INDEX]
        XYZ_t = XYZ[T_INDEX]
        TAG_t = TAG[T_INDEX]
        INFO_t = INFO[T_INDEX]

        if npzflag:
            npzTime_t = npzTime[T_INDEX]
            npzSee_t = npzSee[T_INDEX,:,:]
            npzComm_t = npzComm[T_INDEX,:,:]
            npzTalk_t = npzTalk[T_INDEX,:,:]
            npzP_t = npzP[T_INDEX,:,:]
            npzD_t = npzD[T_INDEX,:,:]
        #############################
        ######### Drawing Process ######
        
        #print(npzTime_t, '\nnpzComm_t' ,npzComm_t, '\nnpzTalk_t' ,npzTalk_t)
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if SHOWTIME:
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("TimeInterval:" + format(TimeInterval, ".3f"), True, yellow, black)
            screen.blit(time_surface, [620,560]) #[750,350]*ZOOMFACTOR)
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Simulation Time:" + format(Time_t, ".3f"), True, yellow, black)
            screen.blit(time_surface, [620,580]) #[750,350]*ZOOMFACTOR)
            if npzflag:
                time_surface=myfont.render("Simulation Time (npz):" + str(npzTime_t), True, white, black)
                screen.blit(time_surface, [620,600]) #[750,350]*ZOOMFACTOR)
            
        drawWalls(screen, walls, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
        #drawPATH(screen, holes, green, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, exits, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        #drawPATH(screen, entries, purple, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
            
        #if debug:
            #print ("Show TAG_t: ", TAG_t)
        
        # Show Mouse Position
        (mouseX3, mouseY3) = pygame.mouse.get_pos()
        mouse_pos3 = np.array([mouseX3, mouseY3])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",16)
        text_surface=myfont.render(str((mouse_pos3-xyShift)*(1/ZOOMFACTOR)), True, black, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos3), True, tan, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 36.0])

        ################################
        # Next step is drawing agents by using evac data
        ################################  
        for idai in range(np.size(TAG_t)):

            if XYZ_t[2][idai]<Zmin or XYZ_t[2][idai]>Zmax:
                continue
            #scPos = np.array([0, 0])
            scPos = [0, 0]
            scPos[0] = int(XYZ_t[0][idai]*ZOOMFACTOR+xSpace)
            scPos[1] = int(XYZ_t[1][idai]*ZOOMFACTOR+ySpace)

            actualV = [INFO_t[0][idai], INFO_t[1][idai]]
            #actualVPos=(XYZ_t[:,idai]+actualV)*ZOOMFACTOR+xyShift
            actualVPos=[0, 0]
            actualVPos[0]=(XYZ_t[0][idai]+INFO_t[0][idai])*ZOOMFACTOR+xSpace
            actualVPos[1]=(XYZ_t[1][idai]+INFO_t[1][idai])*ZOOMFACTOR+ySpace
            
            desiredV = [INFO_t[2][idai], INFO_t[3][idai]]
            #desiredVPos=(XYZ_t[:,idai]+desiredV)*ZOOMFACTOR+xyShift
            desiredVPos = [0, 0]
            desiredVPos[0]=(XYZ_t[0][idai]+INFO_t[2][idai])*ZOOMFACTOR+xSpace
            desiredVPos[1]=(XYZ_t[1][idai]+INFO_t[3][idai])*ZOOMFACTOR+ySpace

            motiveF = [INFO_t[4][idai], INFO_t[5][idai]]
            motiveFPos = [0, 0]
            motiveFPos[0]=(XYZ_t[0][idai]+INFO_t[4][idai])*ZOOMFACTOR+xSpace
            motiveFPos[1]=(XYZ_t[1][idai]+INFO_t[5][idai])*ZOOMFACTOR+ySpace
    
            groupF = [INFO_t[6][idai], INFO_t[7][idai]]
            groupFPos = [0, 0]
            groupFPos[0]=(XYZ_t[0][idai]+INFO_t[6][idai])*ZOOMFACTOR+xSpace
            groupFPos[1]=(XYZ_t[1][idai]+INFO_t[7][idai])*ZOOMFACTOR+ySpace

            selfrepF = [INFO_t[8][idai], INFO_t[9][idai]]
            selfrepFPos = [0, 0]
            selfrepFPos[0]=(XYZ_t[0][idai]+INFO_t[8][idai])*ZOOMFACTOR+xSpace
            selfrepFPos[1]=(XYZ_t[1][idai]+INFO_t[9][idai])*ZOOMFACTOR+ySpace

            subF = [INFO_t[10][idai], INFO_t[11][idai]]
            subFPos = [0, 0]
            subFPos[0]=(XYZ_t[0][idai]+INFO_t[10][idai])*ZOOMFACTOR+xSpace
            subFPos[1]=(XYZ_t[1][idai]+INFO_t[11][idai])*ZOOMFACTOR+ySpace
            
            objF = [INFO_t[12][idai], INFO_t[13][idai]]
            objFPos = [0, 0]
            objFPos[0]=(XYZ_t[0][idai]+INFO_t[12][idai])*ZOOMFACTOR+xSpace
            objFPos[1]=(XYZ_t[1][idai]+INFO_t[13][idai])*ZOOMFACTOR+ySpace

            tpre = INFO_t[14][idai]
            exitSelected = INFO_t[15][idai]
            
            num_see_others = INFO_t[16][idai]
            num_others = INFO_t[17][idai]
            
            #ratioV = INFO_t[18][idai]
            #stressLevel = INFO_t[19][idai]
            
            #temp = int(100*agent.ratioV)
            #AGENTCOLOR = [0,0,temp]
            #color_para = [0, 0, 0]
            #color_para[0] = int(255*min(1, agent.ratioV))
            
            if tpre > Time_t:
                try:
                    pygame.draw.circle(screen, tan, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH+3)
                except:
                    pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH+3)
            else:
                try:
                    pygame.draw.circle(screen, tan, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH)
                except:
                    pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
                    
            if SHOWINDEX:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render(str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, scPos)

            if SHOWTPRE:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render(str(tpre), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, scPos) #+[0.0, -100*ZOOMFACTOR])
            
            if SHOWVELOCITY:
                pygame.draw.line(screen, orange, scPos, actualVPos, 2)
                pygame.draw.line(screen, yellow, scPos, desiredVPos, 2)            
            

            if SHOWFORCE:
                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)    
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  
            
            if np.linalg.norm(mouse_pos3-scPos)<10.0:
                
                agentIndex=TAG_t[idai]

                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  

                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render("@subF:"+format(np.linalg.norm(subF), ".3f")+str(subF), True, black, white)
                screen.blit(text_surface, mouse_pos3+[0.0, 56.0])
                text_surface=myfont.render("@objF:"+format(np.linalg.norm(objF), ".3f")+str(objF), True, black, white)
                screen.blit(text_surface, mouse_pos3+[0.0, 79.0])
                text_surface=myfont.render("@motiveF:"+format(np.linalg.norm(motiveF), ".3f")+str(motiveF), True, black, white)
                screen.blit(text_surface, mouse_pos3+[0.0, 97.0])
                text_surface=myfont.render("@socialF:"+format(np.linalg.norm(groupF), ".3f")+str(groupF), True, black, white)
                screen.blit(text_surface, mouse_pos3+[0.0, 116.0])
                text_surface=myfont.render("@selfrepF:"+format(np.linalg.norm(selfrepF), ".3f")+str(selfrepF), True, black, white)
                screen.blit(text_surface, mouse_pos3+[0.0, 136.0])

                print(str(TAG_t[idai])+'num_see_others:'+str(INFO_t[16][idai]))
                print(str(TAG_t[idai])+'num_others:'+str(INFO_t[17][idai]))

                if npzflag:
                    print('See List:\n'+str(TAG_t[idai])+str(npzSee_t[TAG_t[idai],:]))
                    print('Communication List:\n'+str(TAG_t[idai])+str(npzComm_t[TAG_t[idai],:])) #[TAG_t[idai],:]))
                    print('Talk List:\n'+str(TAG_t[idai])+str(npzTalk_t[TAG_t[idai],:]))
                
                    text_surface=myfont.render("See List:    "+str(npzSee_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, mouse_pos3+[0.0, 155.0])
                    text_surface=myfont.render("Comm List:"+str(npzComm_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, mouse_pos3+[0.0, 176.0])
                    #text_surface=myfont.render("Talk List :"+str(npzTalk_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, mouse_pos3+[0.0, 196.0])
                                    
                #text_surface=myfont.render("V:"+str(V[iii, jjj, T_INDEX]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 103.0])
                #text_surface=myfont.render("Ud:"+str(Ud0[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 123.0])
                #text_surface=myfont.render("Vd:"+str(Vd0[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 143.0])
                #text_surface=myfont.render("BLD:"+str(BLDinfo[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 169.0])

            #tempID = agentIndex%(np.size(TAG_t)+1)
            if agentIndex == TAG_t[idai]:
                #try:
                #    pygame.draw.circle(screen, tan, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH)
                #except:
                #    pygame.draw.circle(screen, tan, scPos, int(0.8*ZOOMFACTOR), LINEWIDTH)
                #pygame.draw.circle(screen, IndianRed, scPos, int(0.3*ZOOMFACTOR), 6)
                #pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
                myfont=pygame.font.SysFont("arial",20)
                text_surface=myfont.render(str(TAG_t[idai]), True, (0,0,0), orange)
                screen.blit(text_surface, scPos)
                
                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  
                
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render('agentID:'+str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [26.0, 500.0])
                text_surface=myfont.render('agent position:' \
                 + format(XYZ_t[0,idai], ".3f") + "   " \
                 + format(XYZ_t[1,idai], ".3f") + "   " \
                 + format(XYZ_t[2,idai], ".3f"), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [206.0, 500.0])
                
                if npzflag:
                    #text_surface=myfont.render("See List:"+str(npzSee_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, [206.0, 500.0])
                    text_surface=myfont.render("Comm List:"+str(npzComm_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, [206.0, 519.0])
                    text_surface=myfont.render("Talk List:    "+str(npzTalk_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, [206.0, 539.0])
                    text_surface=myfont.render("P Array:      "+str(np.round(npzP_t[TAG_t[idai],:], 2)), True, black, white)
                    screen.blit(text_surface, [206.0, 559.0])
        
                myfont=pygame.font.SysFont("arial",16)        
                text_surface=myfont.render("@subF:"+format(np.linalg.norm(subF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 519.0])
                text_surface=myfont.render("@objF:"+format(np.linalg.norm(objF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 539.0])
                
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render('agentID:'+str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [26.0, 560.0])
                    
                text_surface=myfont.render("@motiveF:"+format(np.linalg.norm(motiveF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 580.0])
                text_surface=myfont.render("@socialF:"+format(np.linalg.norm(groupF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 600.0])
                text_surface=myfont.render("@selfrepF:"+format(np.linalg.norm(selfrepF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 620.0])
                text_surface=myfont.render("exit:"+str(exitSelected), True, black, white)
                screen.blit(text_surface, [126.0, 560.0])
                text_surface=myfont.render("tpre:"+format(tpre, ".3f"), True, black, white)
                screen.blit(text_surface, [126.0, 500.0])
                #text_surface=myfont.render("objF:"+str(int(np.linalg.norm(objF))), True, black, white)
                #screen.blit(text_surface, [206.0, 560.0])
            

        REWIND=False
        FORWARD=False
        pygame.display.flip()
        clock.tick(TimeInterval)


