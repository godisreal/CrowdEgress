
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
import sys

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
Cyan = 0, 255, 255
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
            text_surface=myfont.render('ID'+str(door.id)+'/'+str(door.arrow), True, blue, (255,255,255))
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
        text_surface=myfont.render('ID'+str(door.id)+'/'+str(door.arrow), True, blue, (255,255,255))
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
            text_surface=myfont.render('ID'+str(exit.id)+'/'+str(exit.arrow), True, blue, (255,255,255))
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
        text_surface=myfont.render('ID'+str(exit.id)+'/'+str(exit.arrow), True, blue, (255,255,255))
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


def show_mesh(screen, x_min, y_min, x_max, y_max, x_points, y_points, BLDindex, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0, SHOWDATA=False):
    
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
                pygame.draw.line(screen, Cyan, ghostcellpos*ZOOMFACTOR-[0,0.6]+xyShift, ghostcellpos*ZOOMFACTOR+[0,0.6]+xyShift, 15)
                #ghostcellpos=np.array([xDim[i],yDim[j]])
                pygame.draw.line(screen, Cyan, ghostcellpos*ZOOMFACTOR-[0.6,0]+xyShift, ghostcellpos*ZOOMFACTOR+[0.6,0]+xyShift, 15)
            else:
                fieldcell=np.array([0,0])
                fieldcell[0]=int(xDim[i]*ZOOMFACTOR+xSpace)
                fieldcell[1]=int(yDim[j]*ZOOMFACTOR+ySpace)
                pygame.draw.circle(screen, red, fieldcell, 2, 2)
                                
            #vec=np.array([Ud[i,j],Vd[i,j]])
            #startPos = np.array([xDim[i],yDim[j]])
            #endPos = startPos + VECFACTOR*normalize(vec) #
            #pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)
            

def show_vel(screen, x_min, y_min, x_max, y_max, x_points, y_points, Ud, Vd, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0, SHOWDATA=False):

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
        


def show_geom(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    f.write("\n\n")
    f.write("Test Geometry of Compartment. \n")
    # f.write('FN_FDS=', simu.FN_FDS)
    # f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print ("Input data is not correct!  Please modify input data file!")
        return

    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
    walls = simu.walls
    doors = simu.doors
    exits = simu.exits
    agents = simu.agents
    exit2door = simu.exit2door
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
                             print ("Output door data into bldDataRev.csv! Please check!")
                             updateDoorData(doors, 'bldDataRev.csv')
                              #simu.FN_EVAC+simu.FN_FDS) #simu.outDataName+'doorDataRev.csv')
                             menu_01 =False
                         elif mouseX<120 and mouseX>0 and mouseY<60 and mouseY>43:
                             # dump exit2door data
                             #print ("Output exit2door data into Exit2DoorRev.csv! Please check!")
                             #updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
                             print ("Output exit data into bldDataRev.csv! Please check!")
                             updateExitData(exits, 'bldDataRev.csv') #simu.outDataName+'exitDataRev.csv')
                             menu_01 =False
                         elif mouseX<120 and mouseX>0 and mouseY<80 and mouseY>63:
                             # dump wall data
                             print ("Output wall data into bldDataRev.csv! Please check!")
                             #updateWallData(simu.walls, 'wallDataRev.csv')
                             updateWallData(walls, 'bldDataRev.csv') #simu.outDataName+'wallDataRev.csv')
                             menu_01 =False
                          # elif mouseX<120 and mouseX>0 and mouseY<100 and mouseY>83:
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
                             simu.SHOWWALLDATA= not simu.SHOWWALLDATA
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
                        addWall(simu.walls, px1, px2, mode='rect')

                    if menu_05 is True:
                        move_agent_state = False
                        px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                        px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                        x1 = px1[0]
                        y1 = px1[1]
                        x2 = px2[0]
                        y2 = px2[1]
                        #if x1<x2 and y1<y2:
                        #    pass
                        addDoor(simu.doors, px1, px2, mode='rect')

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
                        addExit(simu.exits, px1, px2, mode='rect')

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
                    for door in simu.doors:
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
                    
                    '''
                    for door in simu.doors:
                        if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                            w1=draw_arrows[-2]
                            w2=draw_arrows[-1]
                            result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                            #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                            if result1 != None:
                                simu.exit2door[draw_exit.id, door.id]=1
                                #door.arrow=1
                            elif result2 != None:
                                simu.exit2door[draw_exit.id, door.id]= -2
                                #door.arrow=-2
                            elif result3 != None:
                                simu.exit2door[draw_exit.id, door.id]= -1
                                #door.arrow=-1
                            elif result4 != None:
                                simu.exit2door[draw_exit.id, door.id]= 2
                                #door.arrow=2
                    '''
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_KP3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_SPACE:
                    #updateWallData(simu.walls, 'wallDataRev.csv')
                    #updateDoorData(simu.doors, 'doorDataRev.csv')
                    #updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
                    updateWallData(walls, 'bldDataRev.csv')
                    updateDoorData(doors, 'bldDataRev.csv')
                    updateExitData(exits, 'bldDataRev.csv')
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
        
        drawWalls(screen, walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)

        #####################################
        #### Draw Agents at Initial Positions ###
        #####################################
        for idai, agent in enumerate(agents):
            
            if agent.inComp == 0:
                continue
            
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
            scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
            pygame.draw.circle(screen, red, scPos, agent.size, LINEWIDTH)

            myfont=pygame.font.SysFont("arial",14)
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
            
            print("draw_exit.id", draw_exit.id)  #"door.id", door.id
            #for door in doors: #simu.doors:
            #    drawDirection(screen, door, simu.exit2door[draw_exit.id, door.id], ZOOMFACTOR, xSpace, ySpace)
            
            #if len(draw_lines)>1:
            #    for i in range(len(draw_lines)-1):
            #        #print('i in draw_lines:', i)
            #        pygame.draw.line(screen, red, draw_lines[i]*ZOOMFACTOR, draw_lines[i+1]*ZOOMFACTOR, LINEWIDTH)
        
        if change_arrows:
            if len(draw_arrows)>1:
                pygame.draw.line(screen, red, draw_arrows[0]*ZOOMFACTOR+xyShift, draw_arrows[1]*ZOOMFACTOR+xyShift, LINEWIDTH)

        #if menu_left is True:
        if menu_01 is True:
            #surface.fill(white, (0, 20, 60, 60))
            pygame.draw.rect(screen, tan, [0, 20, 120, 60])
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render('output_doors', True, white, tan)
            screen.blit(text_surface, [0,23])#+[0.0,20.0]) #+xyShift)
            text_surface=myfont.render('output_exits', True, white, tan)
            screen.blit(text_surface, [0,43])#+[0.0,40.0]) #+xyShift)
            text_surface=myfont.render('output_walls', True, white, tan)
            screen.blit(text_surface, [0,63])#+[0.0,60.0]) #+xyShift)
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
            text_surface=myfont.render('show/hide walls', True, white, tan)
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
                                                                
        pygame.display.flip()
        clock.tick(20)
        
    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    simu.walls = walls
    simu.doors = doors
    simu.exits = exits
    simu.agents = agents
    #simu.exit2door = exit2door

    f.write('Display a summary of input data after TestGeom as below.\n')
    f.write('number of walls: '+str(len(simu.walls))+ '\n')
    f.write('number of doors: '+str(len(simu.doors))+ '\n')
    f.write('number of exits: '+str(len(simu.exits))+ '\n\n')
        
    f.close()
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

                    for door in simu.doors:
                        if door.inside((mouse_pos2-xyShift)*(1/ZOOMFACTOR)):
                            w1=draw_arrows[-2]
                            w2=draw_arrows[-1]
                            result1, result2, result3, result4 = door.intersecWithLine(w1, w2, '4arc')
                            #print('result1, result2, result3, result4:', result1, result2, result3, result4)
                            if result1 != None:
                                simu.exit2door[draw_exit.id, door.id]=1
                                #door.arrow=1
                            elif result2 != None:
                                simu.exit2door[draw_exit.id, door.id]= -2
                                #door.arrow=-2
                            elif result3 != None:
                                simu.exit2door[draw_exit.id, door.id]= -1
                                #door.arrow=-1
                            elif result4 != None:
                                simu.exit2door[draw_exit.id, door.id]= 2
                                #door.arrow=2

                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                #elif event.key == pygame.K_SPACE:
                #    simu.PAUSE = not simu.PAUSE
                #elif event.key == pygame.K_v:
                #    simu.SHOWVELOCITY = not simu.SHOWVELOCITY
                #elif event.key == pygame.K_i:
                #    simu.SHOWINDEX = not simu.SHOWINDEX
                #elif event.key == pygame.K_d:
                #    simu.DRAWDOORFORCE = not simu.DRAWDOORFORCE
                #elif event.key == pygame.K_r:
                #    simu.DRAWSELFREPULSION = not simu.DRAWSELFREPULSION
                elif event.key == pygame.K_KP1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_KP3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                #elif event.key == pygame.K_s:
                #    simu.SHOWSTRESS = not simu.SHOWSTRESS
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
            
            print("draw_exit.id", draw_exit.id)
            #for door in doors: #simu.doors:
            #    drawDirection(screen, door, simu.exit2door[draw_exit.id, door.id], ZOOMFACTOR, xSpace, ySpace)
            
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
                    drawDirection(screen, door, simu.exit2door[idexit, door.id], ZOOMFACTOR, xSpace, ySpace)
                
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
                endPosGF = (agent.pos+agent.groupF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

            if simu.DRAWSELFREPULSION:
                endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosRF, 2)
                
            
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
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
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
        intiPrt(fbin)

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
                elif event.key == pygame.K_KP1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_KP3:
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
        simu.simulation_step2022()
        #simu.t_sim = simu.t_sim + simu.DT  # Maybe it should be in step()
        pass

        # Dump agent binary data file
        if simu.dumpBin and simu.t_sim > simu.tt_DumpData:
            dump_evac(simu.agents, fbin, simu.t_sim)
            simu.tt_DumpData = simu.tt_DumpData + simu.DT_DumpData
        
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
            time_surface=myfont.render("Simulation Time:" + str(simu.t_sim), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [100,23]) #[750,350]*ZOOMFACTOR)

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
                    drawDirection(screen, door, simu.exit2door[idexit, door.id], ZOOMFACTOR, xSpace, ySpace)
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
            pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
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
                endPosGF = (agent.pos+agent.groupF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

            if simu.DRAWSELFREPULSION:
                endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosRF, 2)
                
            
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
                    pygame.draw.line(screen, lightpink, scPos, scPosOther, 2)
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)

                if person.talk[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, magenta, scPos, scPosOther, 3)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)
            
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
                text_surface=myfont.render(str(agent.ratioV), True, (0,0,0), (255,255,255))
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
        clock.tick(20)

    f.close()
    if simu.dumpBin:
        fbin.close()
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
    for obstFeature in obstFeatures:
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.mode = obstFeature[4]
        wall.id = int(obstFeature[5])
        wall.inComp = int(obstFeature[6])
        wall.arrow = int(obstFeature[7])
        #wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
        #wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
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



def show_crowdfluid(filename, debug=True):

    # Read in data from filename
    flowdata=np.load(filename)
    Ud0 = flowdata["arr_0"]
    Vd0 = flowdata["arr_1"]
    R = flowdata["arr_2"]
    U = flowdata["arr_3"]
    V = flowdata["arr_4"]
    BLDinfo = flowdata["arr_5"]
    [x_min, y_min, x_max, y_max, x_points, y_points] = flowdata["arr_6"]

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
        print("(dimX,dimY,dimT)", np.shape(R), '\n')
        if sys.version_info[0] == 2: 
            raw_input('Please check input data here!')
            #UserInput = raw_input('Check Input Data Here!')
        if sys.version_info[0] == 3:
            UserInput =input('Please check input data here!')

    (dimX,dimY,dimT)=np.shape(R)
    print(np.shape(BLDinfo))
    print(np.shape(Ud0))
    print(np.shape(R))

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

    SCREENSIZE = [1000, 900]
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
    SHOWGHOSTBLD=True
    SHOWUVDesired=True
    #SHOWSINK=True

    T_END=dimT
    T_INDEX=0 #0...dimT-1

    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Modified Social Force Model')
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
                elif event.key == pygame.K_KP1:
                    SHOWGHOSTBLD = not SHOWGHOSTBLD
                elif event.key == pygame.K_KP2:
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
                        pygame.draw.line(screen, Cyan, ghostcellpos*ZOOMFACTOR-[0,0.6]+xyShift, ghostcellpos*ZOOMFACTOR+[0,0.6]+xyShift, 15)
                        #ghostcellpos=np.array([xDim[i],yDim[j]])
                        pygame.draw.line(screen, Cyan, ghostcellpos*ZOOMFACTOR-[0.6,0]+xyShift, ghostcellpos*ZOOMFACTOR+[0.6,0]+xyShift, 15)
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
            running = False
        for i in range(dimX):
            for j in range(dimY):
                #if i==0 or j==0:
                #    continue
                #else:

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

            #scPos = agent.pos*10 #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            #scPos = [0, 0]
            #scPos[0] = int(agent.pos[0]*ZOOMFACTOR) #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            #scPos[1] = int(agent.pos[1]*ZOOMFACTOR)
            
            #endPosV = [0, 0]
            #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR)
            #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR)
            
            #endPosDV = [0, 0]
            #endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR)
            #endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR)
            
            #AGENTSIZE = int(agent.radius)
            #pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
            #pygame.draw.line(screen, AGENTCOLOR, scPos, endPosV, 2)
            #pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
            
            #print(scPos)
            
        pygame.display.flip()
        clock.tick(200)

