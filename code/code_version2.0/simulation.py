
import os, sys
from random import randint, choice, normalvariate
from math import sin, cos, radians
#from math import *
import numpy as np
import re
import random
#from random import *

from agent import *
from obst import *
from math_func import *
from data_func import *
from draw_func import *
from startPage import*

class simulation(object):

    # basic defaults

    # Below are variables for users to set up pygame features
    ################################################################

    ZOOMFACTOR = 20.0    	
    xSpace=10.0
    ySpace=10.0
    #self.xyShift = np.array([xSpace, ySpace])

    #SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
    #GRID_SIZE = 20, 20
    #FIELD_SIZE = 500, 500
    #FIELD_LIMITS = 0, 0, 600, 600
    #field_bgcolor = white

    # Some variables for visualization of the simulation by pygame
    # They should be packed up into visControl class
    THREECIRCLES = False  	# Use 3 circles to draw agents
    SHOWVELOCITY = True	# Show velocity and desired velocity of agents
    SHOWINDEX = True        # Show index of agents
    SHOWTIME = True         # Show a clock on the screen
    SHOWINTELINE = True     # Draw a line between interacting agents
    MODETRAJ = False        # Draw trajectory of agents' movement
    PAUSE = False
    SHOWWALLDATA = True
    SHOWDOORDATA = True
    SHOWEXITDATA = True
    SHOWSTRESS = False
    DRAWWALLFORCE = True
    DRAWDOORFORCE = True
    DRAWGROUPFORCE = False
    DRAWSELFREPULSION = False
    
        
    def __init__(self, outputFileName=None, params=None):

        self.DT = 0.3
        self.t_sim=0.0
        self.t_end=0.0
        self.t_pause=0.0
        
        self.DT_OtherList = 3.0
        self.tt_OtherList = 0.0

        self.DT_ChangeDoor = 3.0
        self.tt_ChangeDoor = 0.0

        # Below are variables to set up the simulation
        ################################################################
        self.TIMECOUNT = True
        self.SELFREPULSION = False	# Enable self repulsion
        self.WALLBLOCKHERDING = True
        self.TPREMODE = 3        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 
        self.TESTFORCE = True
        self.GROUPBEHAVIOR = True     # Enable the group social force
        self.TESTMODE = False #True
        #self.GUI = True
        #self.STARTPAGE = False
        #self.COHESION = False

        # Entities in simulation: Agnets Walls Doors Exits
        self.agents=[]
        self.walls=[]
        self.doors=[]
        self.exits=[]

        self.num_agents=0
        self.num_walls=0
        self.num_doors=0
        self.num_exits=0
        
        self.inputDataCorrect = True
        self.FN_FDS=None
        self.FN_EVAC = None
        self.outDataName =outputFileName
		
        if self.outDataName is None:
            self.outDataName ="outData"

        #self.t_now =0.0
        #self.t_pause = 0.0
        

    def select_file(self, FN_EVAC=None, FN_FDS=None, mode='GUI'):
		
        FN_Temp = self.outDataName + ".txt"
        
        if os.path.exists(FN_Temp) and self.FN_EVAC is None and mode=='GUI':
            for line in open(FN_Temp, "r"):
                if re.match('FN_FDS', line):
                    temp =  line.split('=')
                    FN_FDS = temp[1].strip()
                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    FN_EVAC = temp[1].strip()

        # This is used for debug mode
        if self.TESTMODE: 
            print FN_FDS
            print FN_EVAC
            print "As above is the input file selected in your last run!"
            raw_input('Input File Selection from Last Run.')

        # This is a simple user interface to select input files
        if mode=="GUI":
            [FN_FDS, FN_EVAC] = startPage(FN_FDS, FN_EVAC)

        # Update the data in simulation class
        self.FN_FDS = FN_FDS
        self.FN_EVAC = FN_EVAC

        # The file to record the output data of simulation
        FN_Temp = self.outDataName + ".txt"
        f = open(FN_Temp, "w+")
        #self.outFileName=f

        print >> f, 'FN_FDS=', self.FN_FDS
        print >> f, 'FN_EVAC=', self.FN_EVAC #,'\n'

        #FN_FDS=self.FN_FDS
        #FN_EVAC=self.FN_EVAC

        ###  Read in Data from .CSV File ###
        self.agents = readAgents(FN_EVAC)
        self.exits = readExits(FN_EVAC)

        self.num_agents = len(self.agents)
        self.num_exits = len(self.exits)

        if FN_FDS!="" and FN_FDS!="None" and FN_FDS is not None:
            self.walls = readOBST(FN_FDS, 'obst_test.csv')
            self.doors = readHOLE(FN_FDS, 'hole_test.csv')
            #exits = readEXIT(FN_FDS, 'exit_test.csv')
            self.num_walls = len(self.walls)
            self.num_doors = len(self.doors)
            #num_exits = len(exits)
        else:
            self.walls = readWalls(FN_EVAC)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
            self.doors = readDoors(FN_EVAC)
            self.num_walls = len(self.walls)
            self.num_doors = len(self.doors)

        ###=== Probablity of Knowing Exit ========
        tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&Ped2Exit')
        self.agent2exit = readFloatArray(tableFeatures, len(self.agents), len(self.exits))
        #agent2exit = readCSV("Agent2Exit2018.csv", "float")

        ###=== Door Direction for Each Exit ========
        tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&Exit2Door')
        self.exit2door = readFloatArray(tableFeatures, len(self.exits), len(self.doors))
        #exit2door = readCSV("Exit2Door2018.csv", "float")

        if np.shape(self.agent2exit)!= (self.num_agents, self.num_exits): #or np.shape(agent2exit)[1]!=
            print('\nError on input data: exits or agent2exit \n')
            print >>f, '\nError on input data: exits or agent2exit \n'
            raw_input('Error on input data: exits or agent2exit!  Please check')
            self.inputDataCorrect = False

        if np.shape(self.exit2door)!= (self.num_exits, self.num_doors): 
            print '\nError on input data: exits or exit2door \n'
            print >>f, '\nError on input data: exits or exit2door \n'
            raw_input('Error on input data: exits or exit2door!  Please check')
            self.inputDataCorrect = False

        if self.GROUPBEHAVIOR: 
            # Initialize Desired Interpersonal Distance
            tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupD')
            person.DFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #DFactor_Init = readCSV("D_Data2018.csv", 'float')

            tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupA')
            person.AFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #AFactor_Init = readCSV("A_Data2018.csv", 'float')

            tableFeatures, LowerIndex, UpperIndex = getData(FN_EVAC, '&groupB')
            person.BFactor_Init = readFloatArray(tableFeatures, len(self.agents), len(self.agents))
            #BFactor_Init = readCSV("B_Data2018.csv", 'float')

            #print >> f, "Wall Matrix\n", walls, "\n"
            print >> f, "D Matrix\n", person.DFactor_Init, "\n"
            print >> f, "A Matrix\n", person.AFactor_Init, "\n"
            print >> f, "B Matrix\n", person.BFactor_Init, "\n"

            if np.shape(person.DFactor_Init)!= (self.num_agents, self.num_agents):
                print '\nError on input data: DFactor_Init\n'
                print >>f, '\nError on input data: DFactor_Init\n'
                raw_input('Error on input data: DFactor_Init!  Please check')
                self.inputDataCorrect = False
                
            if np.shape(person.AFactor_Init)!= (self.num_agents, self.num_agents): 
                print '\nError on input data: AFactor_Init\n'
                print >>f, '\nError on input data: AFactor_Init\n'
                raw_input('Error on input data: AFactor_Init!  Please check')
                self.inputDataCorrect = False

            if np.shape(person.BFactor_Init)!= (self.num_agents, self.num_agents): 
                print '\nError on input data: BFactor_Init\n'
                print >>f, '\nError on input data: BFactor_Init\n'
                raw_input('Error on input data: BFactor_Init!  Please check')
                self.inputDataCorrect = False
            
            person.DFactor = person.DFactor_Init
            person.AFactor = person.AFactor_Init
            person.BFactor = person.BFactor_Init
        else:
            person.DFactor = np.ones((self.num_agents, self.num_agents))
            person.AFactor = np.ones((self.num_agents, self.num_agents))
            person.BFactor = np.ones((self.num_agents, self.num_agents))
            person.PFactor = np.ones((self.num_agents, self.num_agents))

        person.comm = np.zeros((self.num_agents, self.num_agents))
        person.talk = np.zeros((self.num_agents, self.num_agents))

        if self.inputDataCorrect:
            print("Input data format is correct!")
        else:
            print("Input data format is wrong! Please check and modify!")

        ### Display a summary of input data
        print 'Display a summary of input data as below. '
        print 'number of agents: ', self.num_agents
        print 'number of walls: ', self.num_walls
        print 'number of doors: ', self.num_doors
        print 'number of exits: ', self.num_exits
        print '\n'

        if self.TESTMODE:
            print "Now you can check if the input data is correct or not!"
            print "If everything is OK, please press ENTER to continue!"
            UserInput = raw_input('Check Input Data Here!')

        f.close()
        return self.inputDataCorrect
        # Return a boolean variable to check if the input data format is correct or not


    def simulation_step(self):
        
        # Compute the agents in single step
        for idai,ai in enumerate(self.agents):
            
            # Whether ai is in computation
            if ai.inComp == 0:
                continue
            
            #Pre-Evacuation Time Effect
            #tt = pygame.time.get_ticks()/1000 - t_pause
            if (self.t_sim < ai.tpre):
                ai.desiredSpeed = random.uniform(0.3,1.6)
            else: 
                ai.desiredSpeed = random.uniform(2.0,3.0)
            
            #ai.dest = ai.memory.peek()
            
            ai.direction = normalize(ai.dest - ai.pos)
            ai.desiredV = ai.desiredSpeed*ai.direction
            #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old
            peopleInter = np.array([0.0, 0.0])
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
                
            if self.t_sim > self.tt_OtherList:
                #ai.updateAttentionList(self.agents, self.walls, self.WALLBLOCKHERDING)
                ai.others=[]
            
                #############################################
                # Compute interaction of agents
                # Group force and herding effect
                # Find the agents who draw ai's attention

                for idaj,aj in enumerate(self.agents):
                    
                    if aj.inComp == 0:
                        person.comm[idai, idaj] = 0
                        person.talk[idai, idaj] = 0
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
                    if self.WALLBLOCKHERDING: 
                        for idwall, wall in enumerate(self.walls):
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
                    #if GROUPBEHAVIOR and no_wall_ij and see_i2j:
                    #    peopleInter += ai.groupForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF
                 
                    #############################################
                    # Traditional Social Force and Physical Force
                    if no_wall_ij: #and see_i2j:
                        peopleInter += ai.agentForce(aj)*anisoF
                                 
                    person.talk[idai, idaj] = 0
                    ###################################################
                    # Interactive Opinion Dynamics Starts here
                    # Including Herding Effect, Group Effect and Talking Behavior
                    # There are several persons around you.  Which draws your attention?  
                    ###################################################
                    if person.DFactor is None or person.AFactor is None or person.BFactor is None: #or person.PFactor is None:
                        print("Group parameters Error: Some of DFactor AFactor BFactor PFactor are None Type!")
                    if dij < ai.B_CF*person.BFactor[idai, idaj] + rij*person.DFactor[idai, idaj] and no_wall_ij and see_i2j:
                    #if dij < ai.interactionRange and no_wall_ij and see_i2j:
                        person.comm[idai, idaj] = 1
                        ai.others.append(aj)
                        
                        #DFactor[idai, idaj] = (1-ai.p)*DFactor[idai, idaj]+ai.p*DFactor[idaj, idai]
                        #AFactor[idai, idaj] = (1-ai.p)*AFactor[idai, idaj]+ai.p*AFactor[idaj, idai]
                        #BFactor[idai, idaj] = (1-ai.p)*BFactor[idai, idaj]+ai.p*BFactor[idaj, idai]
                        #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*aj.desiredV		
                    else: 
                        person.comm[idai, idaj] = 0

                    # Loop of idaj,aj ends here
                    ###########################
                
                print '=== ai id ===::', idai
                print 'ai.others len:', len(ai.others)
                self.tt_OtherList = self.t_sim + self.DT_OtherList

            
            for aj in ai.others:

                idaj=aj.ID
                print 'others ID', idaj
                            
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
                    person.DFactor[idai, idaj]=2.0
                    person.AFactor[idai, idaj]=600
                    person.BFactor[idai, idaj]=300
                    ai.tau = ai.talk_tau
                    person.talk[idai, idaj]=1
                else:
                    person.DFactor[idai, idaj]=person.DFactor_Init[idai, idaj]
                    person.AFactor[idai, idaj]=person.AFactor_Init[idai, idaj]
                    person.BFactor[idai, idaj]=person.BFactor_Init[idai, idaj]
                    ai.tau = ai.moving_tau
                    person.talk[idai, idaj]=0

                #peopleInter += ai.agentForce(aj)*anisoF

                ###############################
                # Turn on or off group social force
                # Also known as cohesive social force
                if self.GROUPBEHAVIOR:
                    peopleInter += ai.groupForce(aj, person.DFactor[idai, idaj], person.AFactor[idai, idaj], person.BFactor[idai, idaj])*anisoF

                #if tt > aj.tpre: 
                #    ai.tpre = (1-ai.p)*ai.tpre + ai.p*aj.tpre
                if dij < ai.interactionRange:
                    ai.tpre = 0.5*ai.tpre + 0.5*aj.tpre

            #ai.others=list(set(ai.others))
            #################################
            # Herding Effect Computed
            # Also known as opinion dynamics
            #################################
            #if otherMovingNum != 0:
                #ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
                #ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + #ai.p*otherMovingSpeed/otherMovingNum
                #ai.desiredV = ai.desiredSpeed*ai.direction

                #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir

            if len(ai.others)!=0: #and tt>ai.tpre:
                otherDir, otherSpeed = ai.opinionDynamics()
                ai.direction = (1-ai.p)*ai.direction + ai.p*otherDir
                ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherSpeed
                ai.desiredV = ai.desiredSpeed*ai.direction
            
            ########################################################
            # Turn on or off self-repulsion by boolean variable SELFREPULSION
            # Also known as sub-consciousness effect in crowd dynamics
            ########################################################
            if self.SELFREPULSION and (len(ai.others) != 0):
                selfRepulsion = ai.selfRepulsion(person.DFactor[idai, idai], person.AFactor[idai, idai], person.BFactor[idai, idai])#*ai.direction
            else: 
                selfRepulsion = 0.0

            outsideDoor = True
            for door in self.doors:
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
                for wall in self.walls:
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
            if (self.t_sim < ai.tpre and self.TPREMODE == 1):
                ai.desiredV = ai.direction*0.0
                ai.desiredSpeed = 0.0
                #ai.dest = ai.pos
                ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
                motiveForce = ai.adaptVel()
            
            #ai.sumAdapt += motiveForce*0.2  #PID: Integration Test Here
            
            if (self.t_sim < ai.tpre and self.TPREMODE == 2):
                motiveForce = np.array([0.0, 0.0])

            if (self.t_sim < ai.tpre and self.TPREMODE == 3):
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
            
            if (self.t_sim >= ai.tpre):
            #################################
            # Wall Effect Computed: 
            # Is There Any Wall Nearby On The Route?
            # If So, Adjust Desired Direction

                #####################################################
                # Check whether there is a wall between agent i and the destination
                no_wall_dest = True
                for idwall, wall in enumerate(self.walls):
                    if wall.inComp ==0:
                        continue
                    result, flag = wall.wallInBetween(ai.pos, ai.dest)
                    if result != None:
                        no_wall_dest = False
                        break
                   
                # Start to search visible doors
                ai.targetDoors=ai.findVisibleTarget(self.walls, self.doors)
                print 'ai:', ai.ID, 'Length of targetDoors:', len(ai.targetDoors)
                
                # Start to search visible exits
                ai.targetExits=ai.findVisibleTarget(self.walls, self.exits)

                #ai.findVisibleTarget(walls, doors)
                #ai.findVisibleTarget(walls, exits)
                
                goDoor = ai.selectTarget(self.exit2door)
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
                closeWall = None #None #walls[0]
                closeWallDist = 10.0 # Define how close the wall is
                for wall in self.walls:
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
            ai.actualV = ai.actualV + accl*self.DT # consider dt = 0.5

            ai.wallrepF = wallInter
            ai.doorF = doorInter
            ai.groupF = peopleInter
            ai.selfrepF = selfRepulsion

            if self.TESTFORCE:
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
            ai.pos = ai.pos + ai.actualV*self.DT
            #print(ai.pos)
            #print(accl,ai.actualV,ai.pos)
        
            ai.desiredV_old = ai.desiredV
            ai.actualV_old = ai.actualV
        
            ###########################################
            ## Output time when agents reach the safety
            #if TIMECOUNT and (ai.pos[0] >= 35.0) and (ai.Goal == 0):
            if self.TIMECOUNT and (np.linalg.norm(ai.pos-ai.dest)<=0.2) and (ai.Goal == 0):
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
            for exit in self.exits:
                if exit.inComp == 0:
                    continue
                if exit.inside(ai.pos):
                    ai.inComp = 0

        # Update simulation time
        self.t_sim = self.t_sim + self.DT


    def quit(self):
        #sys.exit()
        pass


if __name__=="__main__":
    myTest = simulation()
    myTest.select_file()
    #myTest.read_data()
    show_geom(myTest)
    show_simu(myTest)
    #myTest.quit()

