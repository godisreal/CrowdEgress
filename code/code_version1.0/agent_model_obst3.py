# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@gmail.com


import numpy as np
from math_func import *
from math import *
import random
#from stack import *

class Agent(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        #self.memory = np.array([0.0, 0.0], [0.0, 0.0], [0.0, 0.0])
        #self.sumAdapt = np.array([0.0, 0.0])
        self.ID = 0 #Name or index of agents
        self.inComp = 1
        self.aType = 'MoveToDest'  #{'MoveToDest' 'Follow' 'Talk' 'Search'}
	
        self.tpre = random.uniform(6.0,22.0)
        self.maxSpeed = random.uniform(1.0,2.0)
        self.diss = random.uniform(-1.0,0.0)
	
        self.posX_init = random.uniform(8,24)
        self.posY_init = random.uniform(8,18)
        self.pos = np.array([self.posX_init, self.posY_init])	
        #self.pos = np.array([10.0, 10.0])

        self.actualVX_init = random.uniform(0,1.6)
        self.actualVY_init = random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX_init, self.actualVY_init])
        self.actualSpeed = np.linalg.norm(self.actualV) #np.array([0.0, 0.0])

        self.dest = np.array([60.0,10.0])
        self.exitInMind = None
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])

        self.pathMap = []
        self.others = []
        self.targetDoors = []
        self.targetExits = []
        self.memory = []
        self.route = []     # Record the passing doors
        # in size of number of doors -1, 0,+1
        #self.memory.append(self.dest)
        
        self.desiredSpeed = 2.0 #random.uniform(0.3,2.3) #1.8
        self.desiredV = self.desiredSpeed*self.direction
        self.desiredSpeedMode = 'random' #{'random' 'fixed' 'increase' 'decrease'}
        
        self.tau = random.uniform(8,16) #10.0
        self.drivenAcc =(self.desiredV - self.actualV)/self.tau
              
        self.mass = 60 #random.uniform(40,90) #60.0
        self.radius = 0.35 #1.6 #0.3

        self.wallrepF= np.array([0.0,0.0])
        self.groupF= np.array([0.0,0.0])
        self.selfrepF= np.array([0.0,0.0])
        self.doorF= np.array([0.0,0.0])
	
        self.interactionRange = 3.0 #Distance for communication (talking)
        self.p = 0.2
        self.pMode = 'random' #{'random' 'fixed' 'increase' 'decrease'}
        
        self.bodyFactorA = 12.0
        self.slideFricFactorA = 240000
	
        # /Group Social Force
        self.A_CF = 1 #30/20000 #2
        self.B_CF = 1 #random.uniform(0.8,1.6) #0.8 #0.08
	
        # Social Force
        self.A_SF = 200 #2
        self.B_SF = 0.8 #random.uniform(0.8,1.6) #0.8 #0.08
	
        # Wall Force / Door Force
        self.A_WF = 60 #200 #60 #2
        self.B_WF = 0.3 #0.2 #0.8 #3.2 #2.2 #random.uniform(0.8,1.6) #0.08
        
        self.bodyFactorW = 12.0
        self.slideFricFactorW = 240000
	
        self.Goal = 0
        self.timeOut = 0.0
	
        self.desiredV_old = np.array([0.0, 0.0])
        self.actualV_old = np.array([0.0, 0.0])
	
        self.lamb = random.uniform(0.2,0.4)
        self.diw_desired = 0.6
	
        self.ratioV = 1
        self.stressLevel = 1
	
        self.color = [255, 0, 0] #blue
	
        self.moving_tau = 0.7
        self.tpre_tau = 1.6
        self.talk_tau = 2.6
        self.talk_prob = 0.6
        
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
    
    
    def shoulders(self):
        if np.allclose(self.actualV, np.zeros(2)):
            direction = self.direction
            direction = normalize(direction)
        else: 
            direction = np.array([-self.actualV[1], self.actualV[0]])
            direction = normalize(direction)
	
        leftPx = self.pos + self.radius*direction
        rightPx = self.pos - self.radius*direction	
        return leftPx, rightPx
    

    def adaptDirection(self):
        self.direction = normalize(self.destmemeory[-1]-self.pos)
        if np.allclose(self.direction, np.zeros(2)):
            self.direction = np.zeros(2)
        return self.direction
    
	
    def adaptVel(self):
        deltaV = self.desiredV - self.actualV
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.tau


    def adaptP(self, flag = 'random'):
        if flag == 'random':
            self.p = self.p + random.uniform(-0.3, 0.3)
            self.p = max(-1.0, min(1.0, self.p))
        elif flag == 'increase' and self.p<1.0:
            # Use randome walk or not ???
            self.p = self.p + random.uniform(0.0, 0.3)
            self.p = min(1.0, self.p)
        elif flag == 'decrease' and self.p>-1.0:
            self.p = self.p + random.uniform(-0.3, 0.0)
            self.p = max(-1.0, self.p)
        return None
	
    
    def adaptDesiredSpeed(self, flag = 'random'):
        if flag == 'random':
            self.desiredSpeed = self.desiredSpeed + random.uniform(-0.3, 0.3)
            self.desiredSpeed = max(0.0, min(3.0, self.desiredSpeed))
        elif flag == 'increase' and self.desiredSpeed<3.0:
            self.desiredSpeed = self.desiredSpeed + random.uniform(0.0, 0.3)
            self.desiredSpeed = min(3.0, self.desiredSpeed)
        elif flag == 'decrease' and self.desiredSpeed>0.0:
            self.desiredSpeed = self.desiredSpeed + random.uniform(-0.3, 0.0)
            self.desiredSpeed = max(0.0, self.desiredSpeed)
        return None
	

    def selfRepulsion(self, Dfactor=1, Afactor=1, Bfactor=1):
        first = -self.direction*Afactor*self.A_CF*np.exp((self.radius*Dfactor)/(self.B_CF*Bfactor))*(self.radius*Dfactor)
        return first
	

    def changeAttr(self, x=1, y=1, Vx=1, Vy=1):
        self.posX = x
        self.posY = y
        self.pos = np.array([self.posX, self.posY])
        self.actualVX = Vx
        self.actualVY = Vy
        self.actualV = np.array([self.actualVX, self.actualVY])


    def showAttr(self):
        #print('test')
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
        print('self.velocity:', self.actualV)
        

    def cohesiveForce(self, other, Dfactor=1, Afactor=1, Bfactor=1):

        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        #phiij = vectorAngleCos(self.actualV , (other.pos - self.pos))
        #anisoF = self.lamb + (1-self.lamb)*(1+cos(phiij))/2
	
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = Afactor*self.A_CF*np.exp((rij*Dfactor-dij)/(self.B_CF*Bfactor))*nij*(rij*Dfactor-dij) #*anisoF
        return first
	

    def agentForce(self, other):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = self.A_SF*np.exp((rij-dij)/self.B_SF)*nij
	
        second = self.bodyFactorA*ggg(rij-dij)*nij
	
        #Issue: nij is a vector directing from j to i.  
        #*(rij*Dfactor-dij)/20000+ self.bodyFactor*g(rij-dij)*nij/10000
        tij = np.array([-nij[1],nij[0]])
        deltaVij = (self.actualV - other.actualV)*tij
        third = self.slideFricFactorA*ggg(rij-dij)*deltaVij*tij
        #third = 300*exp(rij-dij)*deltaVij*tij/dij
	
        return first + second #+ third
    

    ############################
    # This is not used any more.  
    def physicalForce(self, other):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = self.bodyFactorA*g(rij-dij)*nij
        #print >> f, "first:", first, "/n"
	
        return first
    # This is not used any more. 
    ############################

    
    def doorForce(self, door, mode='edge', fuzzydir=0.0):
        if door.inside(self.pos)==False:
            doordir = door.direction(door.arrow)
            agentdir = door.pos-self.pos
            if np.dot(doordir, agentdir)>=fuzzydir:
                ri = self.radius
                #mid= (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))/2.0
                if mode=='pos':
                    dist=np.linalg.norm(door.pos - self.pos)
                    dire = normalize(door.pos-self.pos)
                elif mode == 'edge':
                    edge1, edge2, edge3, edge4 = door.edge()
                    dist1 = np.linalg.norm(edge1 - self.pos)
                    dist2 = np.linalg.norm(edge2 - self.pos)
                    dist3 = np.linalg.norm(edge3 - self.pos)
                    dist4 = np.linalg.norm(edge4 - self.pos)
                    dist_list = [dist1, dist2, dist3, dist4]
                    dist = min(dist_list)
                    dist_index =np.argmin(dist_list)
                    dire = normalize(door.pos-self.pos)  #  Need improvement
                    #if dist1<dist2:
                    #    dist=dist1
                    #    dire = normalize(edge1-self.pos)
                    #else:
                    #    dist=dist2
                    #    dire = normalize(edge2-self.pos)
                        
                #first = self.A_WF*np.exp((ri-dist)/self.B_WF)*dire
                second = 760*exp((ri-dist)/0.3)*dire  #1.8)*dire
                return second #first + second
            else:
                return np.array([0.0, 0.0])
        else:
            if door.arrow == 1 or door.arrow == -1:
                w1= np.array([door.params[0], door.params[1]])
                w2 = np.array([door.params[2], door.params[1]])
                diw, niw = distanceP2L(self.pos, w1, w2)
                first = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
                #second = -600*exp((2*ri-diw)/0.2)*niw
                #result1 = self.wall_LineForce(w1, w2)

                w1= np.array([door.params[0], door.params[3]])
                w2 = np.array([door.params[2], door.params[3]])
                diw, niw = distanceP2L(self.pos, w1, w2)
                second = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
                #result2 = self.wall_LineForce(w1, w2)

                return first + second
                #return result1 + result2
            
            if door.arrow == 2 or door.arrow == -2:
                w1= np.array([door.params[0], door.params[1]])
                w2= np.array([door.params[0], door.params[3]])
                diw, niw = distanceP2L(self.pos, w1, w2)
                first = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
                #result1 = self.wall_LineForce(w1, w2)

                w1= np.array([door.params[2], door.params[1]])
                w2= np.array([door.params[2], door.params[3]])
                diw, niw = distanceP2L(self.pos, w1, w2)
                second = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
                #result2 = self.wall_LineForce(w1, w2)

                return first + second
                #return result1 + result2
            
            if door.arrow ==0:
                return np.array([0.0, 0.0])
             #   if abs(self.actualV[0]) > abs(self.actualV[1]):


    def wall_LineForce(self, w1, w2):
        #ftest = open("wallForceTest.txt", "w+")
        ri = self.radius
        #w1 = np.array([wall.params[0],wall.params[1]])
        #w2 = np.array([wall.params[2],wall.params[3]])
        diw, niw = distanceP2L(self.pos, w1, w2)
        if diw>0.6:
            result=np.array([0.0, 0.0])
            return result
        else:
            #first = -260*np.exp((self.diw_desired-diw)/0.6)*niw  #3.2)*niw
            first = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
            #second = -60*exp((2*ri-diw)/0.2)*niw
            #second = -self.bodyFactorW*ggg(2*ri-diw)*niw*200000
            #Issue: the diretion of niw is from the agent to the wall.  Check Needed!
            #print >> ftest, 'first:', first, '\n'
    
            #tiw = np.array([-niw[1],niw[0]])
            #third = self.slideFricFactorW*ggg(ri-diw)*(self.actualV*tiw)*tiw/1000
            #print >> ftest, 'second:', second, '\n'
    
            #ftest.close()
            if diw>=ri:
                second = np.array([0.0, 0.0])
            else:
                second = -self.bodyFactorW*(ri-diw)*niw*200000
            return first + second #+ third

    
    def wallForce(self, wall):
        if wall.mode == 'line':
            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[3]])
            result = self.wall_LineForce(w1, w2)
            return result

        elif wall.mode == 'rect':

            ########################
            ### p1-----------------p4 ###
            ###  |                              |  ###
            ###  |                              |  ###
            ###  |                              |  ###
            ### p2-----------------p3 ###
            ########################
        
            p1 = np.array([wall.params[0], wall.params[1]])
            p2 = np.array([wall.params[0], wall.params[3]])
            p3 = np.array([wall.params[2], wall.params[3]])
            p4 = np.array([wall.params[2], wall.params[1]])

            dist1 =  np.linalg.norm(p1 - p2)
            dist2 =  np.linalg.norm(p2 - p3)

            if dist1<0.3 and dist2/dist1>10.0:
                w1=(p1+p2)/2.0
                w2=(p3+p4)/2.0
                result = self.wall_LineForce(w1, w2)
                return result

            if dist2<0.3 and dist1/dist2>10.0:
                w1=(p1+p4)/2.0
                w2=(p2+p3)/2.0
                result = self.wall_LineForce(w1, w2)
                return result
            
            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[0],wall.params[3]])
            result0 = self.wall_LineForce(w1, w2)

            w1 = np.array([wall.params[2],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[3]])
            result2 = self.wall_LineForce(w1, w2)

            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[1]])
            result1 = self.wall_LineForce(w1, w2)

            w1 = np.array([wall.params[0],wall.params[3]])
            w2 = np.array([wall.params[2],wall.params[3]])
            result3 = self.wall_LineForce(w1, w2)

            result = result0+result1+result2+result3
            return result


    def wallOnRoute(self, wall, mode=1.0, lookhead=3.0):

        p1 = self.pos
        p2 = self.pos + (mode*self.desiredV+(1-mode)*self.actualV)*lookhead
	
        #if mode=="dv":
        #    p2 = self.pos + self.desiredV
        #elif mode=="av":
        #    p2 = self.pos + self.actualV
        #else:
        #    print 'Error: mode must be either "dv" or "av"!'
        #    return
	
        # The time interval to look ahead is an important issue
        # It is a major issue to use whether actualV or desiredV
        
        if wall.mode == 'line':
            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[3]])
            #dist = self.wallOnRoute_Line(w1, w2, mode, lookhead)
            fuzzyPara = random.uniform(0.0,2.0)
            result, flag = lineIntersection(p1, p2, w1, w2, 0.0, fuzzyPara)
            if result==None:
                dist = None
            else:
                dist = np.linalg.norm(self.pos - result)
            return result, dist, normalize(w2-w1)
        
        if wall.mode =='rect':
            result = None
            dist=None
            arrow=None

            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[0],wall.params[3]])
            fuzzyPara = random.uniform(0.0,2.0)
            result0, flag = lineIntersection(p1, p2, w1, w2, 0.0, fuzzyPara)
            if result0==None:
                dist0 = None
            else:
                dist0 = np.linalg.norm(self.pos - result0)
            #dist0 = self.wallOnRoute_Line(w1, w2, mode, lookhead)
            if dist0!=None:
                if dist==None:
                    result = result0
                    dist=dist0
                    arrow=w2-w1
                elif dist0<dist:
                    result = result0
                    dist=dist0
                    arrow=w2-w1

            w1 = np.array([wall.params[2],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[3]])
            fuzzyPara = random.uniform(0.0,2.0)
            result2, flag = lineIntersection(p1, p2, w1, w2, 0.0, fuzzyPara)
            if result2==None:
                dist2 = None
            else:
                dist2 = np.linalg.norm(self.pos - result2)
            #dist2 = self.wallOnRoute_Line(w1, w2, mode, lookhead)
            if dist2!=None:
                if dist==None:
                    result = result2
                    dist=dist2
                    arrow=w2-w1
                elif dist2<dist:
                    result = result2
                    dist=dist2
                    arrow=w2-w1

            w1 = np.array([wall.params[0],wall.params[1]])
            w2 = np.array([wall.params[2],wall.params[1]])
            fuzzyPara = random.uniform(0.0,2.0)
            result1, flag = lineIntersection(p1, p2, w1, w2, 0.0, fuzzyPara)
            if result1==None:
                dist1 = None
            else:
                dist1 = np.linalg.norm(self.pos - result1)
            
            #dist1 = self.wallOnRoute_Line(w1, w2, mode, lookhead)
            if dist1!=None:
                if dist==None:
                    result=result1
                    dist=dist1
                    arrow=w2-w1
                elif dist1<dist:
                    result=result1
                    dist=dist1
                    arrow=w2-w1

            w1 = np.array([wall.params[0],wall.params[3]])
            w2 = np.array([wall.params[2],wall.params[3]])
            fuzzyPara = random.uniform(0.0,2.0)
            result3, flag = lineIntersection(p1, p2, w1, w2, 0.0, fuzzyPara)
            if result3==None:
                dist3 = None
            else:
                dist3 = np.linalg.norm(self.pos - result3)

            #dist3 = self.wallOnRoute_Line(w1, w2, mode, lookhead)
            if dist3!=None:
                if dist==None:
                    result=result3
                    dist=dist3
                    arrow=w2-w1
                elif dist3<dist:
                    result=result3
                    dist=dist3
                    arrow=w2-w1

            if arrow!=None:
                arrow=normalize(arrow)
            return result, dist, arrow

       
            
    #####################################
    # how an agent interacts with others
    #####################################
     
    def opinionDynamics(self):
	
        # self.D = DMatrix(selfID, otherID)
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        # dij = np.linalg.norm(self.pos - other.pos)
        
        otherMovingDir = np.array([0.0, 0.0])
        otherMovingSpeed = 0.0
        otherMovingNum = 0
	
        for idaj, aj in enumerate(self.others):
            otherMovingDir += normalize(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
            otherMovingSpeed += np.linalg.norm(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
            otherMovingNum += 1
		
        #nij = (self.pos - other.pos)/dij
        
        #if dij < self.interactionRange:
	#    self.dest = self.p*self.dest + (1-self.p)*other.dest

	#otherDirection = np.array([0.0, 0.0])
	#otherSpeed = 0.0
	#num = 0
	#otherV = np.array([0.0, 0.0])

        #if dij < self.interactionRange:
	    #self.desiredV = self.p*self.desiredV + (1-self.p)*other.actualV
	    #otherDirection = normalize(other.actualV)
	    #otherSpeed = np.linalg.norm(other.actualV)
	    #num = 1
	    #otherV = other.actualV
	
        return otherMovingDir, otherMovingSpeed/otherMovingNum
    

    def opinionExchange(self, other, mode=1.0):
        otherV= mode*other.desiredV+(1-mode)*other.actualV
        self.desiredV = self.p*self.desiredV + (1-self.p)*otherV
        return


    def findDoorDir(self, direction):
        if direction == 1:
            return np.array([1.0, 0.0])
        elif direction == -1:
            return np.array([-1.0, 0.0])
        elif direction == 2:
            return np.array([0.0, 1.0])
        elif direction == -2:
            return np.array([0.0, -1.0])
        
        
    def selectTarget(self, exit2door):
        dest = None
        doorOK = None
        exitOK = None

        for exit in self.targetExits:
            #exit.computePos()
            if exit.inside(self.pos):
                return exit
            else:  
                dest_temp = np.linalg.norm(exit.pos - self.pos)
                dir1 = exit.direction(exit.arrow)
                # temp = self.route[exit.id]
                # dir1 = self.findDoorDir(temp)
                dir2 = exit.pos-self.pos
                if dest ==None or dest>dest_temp:
                    if np.dot(dir1, dir2)>=0:
                        dest=dest_temp
                        exitOK = exit

        # Now the nearest exit is found: exitOK
        # Compare it with the exitInMind: Change target exit or not?
        # self.others is to be taken into account.  
        
        if exitOK != None:
            self.pathMap = exit2door[exitOK.id]
            return exitOK
        else:
            self.pathMap = exit2door[self.exitInMind.id]
            
        for door in self.targetDoors:
            #door.computePos()
            if door.inside(self.pos):
                return door
            #if self.pos[0]>=door.params[0] and self.pos[0]<=door.params[2]:
            #    if  self.pos[1]>=door.params[1] and self.pos[1]<=door.params[3]:
            #    return door
            else:
                if len(self.route)>0:
                    if (self.route[len(self.route)-1] is door.pos) and len(self.targetDoors)>1:
                        continue
                dest_temp = np.linalg.norm(door.pos - self.pos)
                dir1 = door.direction(self.pathMap[door.id])    #door.direction(door.arrow)   #
                dir2 = door.pos-self.pos
                if dest ==None or dest>dest_temp:
                    if np.dot(dir1, dir2)>=0:
                        dest=dest_temp
                        doorOK = door
                        
        return doorOK


    def moveToAgent(self):
        dest = None
        someoneOK = None
        for aj in self.others:
            dest_temp = np.linalg.norm(aj.pos - self.pos)
            dir1 = self.direction
            dir2 = aj.pos-self.pos
            if dest ==None or dest>dest_temp:
                #if np.dot(dir1, dir2)>0:
                dest=dest_temp
                someoneOK = aj
        return someoneOK

    
    def findVisibleTarget(self, walls, doors):
        resultDoors=[]
        for iddoor, door in enumerate(doors):
            if door.inComp ==0:
                continue
            if door.inside(self.pos):
                resultDoors.append(door)
                continue
            #edge1 = np.array([door.params[0], door.params[1]])
            #edge2 = np.array([door.params[2], door.params[3]])
            edge1, edge2, edge3, edge4 = door.edge()
            isVisibleDoor=True
            for wall in walls:
                if wall.inComp ==0:
                    continue
                result1, flag1 = wall.wallInBetween(self.pos, edge1)
                result2, flag2 = wall.wallInBetween(self.pos, edge2)
                result3, flag3 = wall.wallInBetween(self.pos, edge3)
                result4, flag4 = wall.wallInBetween(self.pos, edge4)
                result5, flag5 = wall.wallInBetween(self.pos, door.pos)
                if flag1 and flag2 and flag3 and flag4 and flag5:
                    isVisibleDoor=False
                    break
                #elif not flag1:
                #    if np.dot(door.pos-edge1, door.arrow)<0:
                #        isVisibleDoor=False      
            if isVisibleDoor:
                resultDoors.append(door)
        return resultDoors
    

if __name__ == '__main__':
    
    Ped1 = Agent()
    Ped2 = Agent()
    f1 = Ped1.cohesiveForce(Ped2)
    f2 = Ped2.cohesiveForce(Ped1)
    Ped1.opinionExchange(Ped2)
    Ped2.opinionExchange(Ped1)
    print('----------Testing starts here--------')
    print('Other Opinion', f1)
    print('Other Opinion', f2)
    Ped1.showAttr()
    Ped1.showAttr()
    v = Ped1.adaptVel
    Ped1.changeAttr(1,1)
    Ped2.changeAttr(2,2)


	
