
import pygame
import pygame.draw
import numpy as np
from math_func import *
from agent import *

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
LightCyan = 224, 255, 255
lightgreen = 193, 255, 193

# Some Constant Parameters for Pygame 
SCREENSIZE = [800, 400]
RESOLUTION = 180
#BACKGROUNDCOLOR = [255,255,255]
LINEWIDTH = 2
#AGENTSIZE = 6

####################
# Drawing the walls
####################
def drawWall(screen, walls, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

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
                text_surface=myfont.render(str(startPos), True, (255,0,0), (255,255,255))
                screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
                text_surface=myfont.render(str(endPos), True, (255,0,0), (255,255,255))
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

                #text_surface=myfont.render(str(startPos), True, red, (255,255,255))
                #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

                #text_surface=myfont.render(str(endPos), True, red, (255,255,255))
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
            text_surface=myfont.render(str(startPos), True, (255,0,0), (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
            text_surface=myfont.render(str(endPos), True, (255,0,0), (255,255,255))
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

            #text_surface=myfont.render(str(startPos), True, red, (255,255,255))
            #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, red, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)
    

    ####################
    # Drawing the doors
    ####################

def drawDoor(screen, doors, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

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

def drawExit(screen, exits, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

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
    pygame.draw.line(screen, red, startPx*ZOOMFACTOR+xyShift, endPx*ZOOMFACTOR+xyShift, 2)

    dir = endPx - startPx
    dir2 = np.array([-dir[0], dir[1]])
    #dir2 = normalize(dir2)
    arrowPx = endPx - dir*0.2
    arrowPx1 = arrowPx + 0.6*dir2
    arrowPx2 = arrowPx - 0.6*dir2
    pygame.draw.line(screen, red, endPx*ZOOMFACTOR+xyShift, arrowPx1*ZOOMFACTOR+xyShift, 2)
    pygame.draw.line(screen, red, endPx*ZOOMFACTOR+xyShift, arrowPx2*ZOOMFACTOR+xyShift, 2)


def show_geom(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    print >> f, "Test Geometry of Compartment."
    #print >> f, 'FN_FDS=', simu.FN_FDS
    #print >> f, 'FN_EVAC=', simu.FN_EVAC #,'\n'

    if not simu.inputDataCorrect:
        print "Input data is not correct!  Please modify input data file!"
        return

    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
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
    menu_left = False
    change_arrows = False
    draw_state = False
    running = True
    while running: 
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                             print "Output door direction data into doorDataRev.csv! Please check!"
                             updateDoorData(simu.doors, 'doorDataRev.csv')
                             menu_01 =False
                          elif mouseX<120 and mouseX>0 and mouseY<60 and mouseY>43:
                             # dump exit2door data
                             print "Output exit2door data into Exit2DoorRev.csv! Please check!"
                             updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
                             menu_01 =False
                          #elif mouseX<120 and mouseX>0 and mouseY<80 and mouseY>63:
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
                    running = False
                    simu.t_pause = pygame.time.get_ticks()/1000

                if not draw_state:
                    for exit in simu.exits:
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
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_KP3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_SPACE:
                    updateDoorData(simu.doors, 'doorDataRev.csv')
                    updateExit2Doors(simu.exit2door, 'Exit2DoorRev.csv')
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
        
        drawWall(screen, simu.walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoor(screen, simu.doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExit(screen, simu.exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)

        #####################################
        #### Draw Agents at Initial Positions ###
        #####################################
        for idai, agent in enumerate(simu.agents):
            
            if agent.inComp == 0:
                continue
            
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
            scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
            pygame.draw.circle(screen, red, scPos, agent.size, LINEWIDTH)

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

            for door in simu.doors:
                drawDirection(screen, door, simu.exit2door[draw_exit.id, door.id], ZOOMFACTOR, xSpace, ySpace)
            
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
            text_surface=myfont.render('show/hide doors', True, white, tan)
            screen.blit(text_surface, [80,23])#+[0.0,20.0]) #+xyShift)
            text_surface=myfont.render('show/hide exits', True, white, tan)
            screen.blit(text_surface, [80,43])#+[0.0,40.0]) #+xyShift)
            text_surface=myfont.render('show/hide walls', True, white, tan)
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
        
    f.close()
    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    pygame.display.quit()


# Show simulation by pygame
def show_simu(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    print >> f, "Start and show simulation here."
    #print >> f, 'FN_FDS=', simu.FN_FDS
    #print >> f, 'FN_EVAC=', simu.FN_EVAC #,'\n'

    if not simu.inputDataCorrect:
        print "Input data is not correct!  Please modify input data file!"
        return

    ZOOMFACTOR = simu.ZOOMFACTOR
    xSpace = simu.xSpace
    ySpace = simu.ySpace
    
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

        if simu.MODETRAJ == False:
            screen.fill(white)

        tt = pygame.time.get_ticks()/1000-simu.t_pause
        if simu.PAUSE is True:
            t_now = pygame.time.get_ticks()/1000
            simu.t_pause = t_now-tt
            continue

        # Computation Step
        simu.simulation_step()
        #simu.t_sim = simu.t_sim + simu.DT  # Maybe it should be in step()
        pass
        
        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if simu.SHOWTIME:
            tt = pygame.time.get_ticks()/1000-simu.t_pause
            myfont=pygame.font.SysFont("arial",14)
            #time_surface=myfont.render("Physics Time:" + str(tt), True, (0,0,0), (255,255,255))
            #screen.blit(time_surface, [470,370]) #[750,350]*ZOOMFACTOR)
            time_surface=myfont.render("Simulation Time:" + str(simu.t_sim), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [630,370]) #[750,350]*ZOOMFACTOR)

        drawWall(screen, simu.walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoor(screen, simu.doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExit(screen, simu.exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)

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
                
                #print 'shoulders:', leftS, rightS
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
                pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
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

        pygame.display.flip()
        clock.tick(20)

    f.close()
    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    pygame.display.quit()




if __name__=="__main__":


    from obst import *
    #from passage import *
    #from outlet import *

    # initialize OBST
    obstFeatures = readCSV("obstData2018.csv", "string")
    walls = []
    for obstFeature in obstFeatures:
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.mode = obstFeature[4]
        wall.id = int(obstFeature[5])
        wall.arrow = int(obstFeature[6])
        wall.inComp = int(obstFeature[7])
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
        drawWall(screen, walls)
        #drawDoor(screen, doors)
        #drawExit(screen, exits)
        
        pygame.display.flip()
        clock.tick(20)

