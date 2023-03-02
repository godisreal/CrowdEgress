
# -*-coding:utf-8-*-
# Author: WP and ??
# Email: wp2204@gmail.com

import numpy as np
from math_func import *
from math import *

class obst(object):
    
    """
    screen: (Not used)
        Obstacles exists on a screen element 
    id:
        obstacle id 
    mode: 
        obstacle type (Line, Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Line -> [x1,y1,x2,y2]
        Rect -> [x1,y1] [x1,y2] [x2,y2] [x2,y1] 
        Circle -> [x,y,r,None]
    """
    
    def __init__(self, oid=0, mode='line', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.id = 0
        self.mode = 'line'
        
        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])
        
        self.attachedDoors=[]
        self.isSingleWall = False
        self.inComp = 1
        self.arrow = 0
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        self.pointer1 = np.array([float('NaN'), float('NaN')])
        self.pointer2 = np.array([float('NaN'), float('NaN')])


    def direction(self, arrow):
        if self.mode=='line':
            # Direction: (StartX, StartY) --> (EndX, EndY)
            direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            if arrow>0:
                return direction
            elif arrow<0:
                return -direction
            elif arrow==0:
                return np.array([0.0, 0.0])
        
        elif self.mode=='rect':
            pass
            # What is a good representation of no direction?  
            direction = None  # np.array([0.0, 0.0])  #NaN

            ### +1: +x
            ###  -1: -x
            ### +2: +y
            ###  -2: -y 
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
            return direction
    

    def wallInBetween(self, p1, p2):

        if self.mode == 'line':
            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[2],self.params[3]])
            result, flag = lineIntersection(p1, p2, w1, w2)
            return result, flag

        elif self.mode == 'rect':
            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[0],self.params[3]])
            result0, flag0 = lineIntersection(p1, p2, w1, w2)
            if flag0==True:
                return  result0, flag0

            w1 = np.array([self.params[2],self.params[1]])
            w2 = np.array([self.params[2],self.params[3]])
            result2, flag2 = lineIntersection(p1, p2, w1, w2)
            if flag2==True:
                return  result2, flag2

            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[2],self.params[1]])
            result1, flag1 = lineIntersection(p1, p2, w1, w2)
            if flag1==True:
                return  result1, flag1

            w1 = np.array([self.params[0],self.params[3]])
            w2 = np.array([self.params[2],self.params[3]])
            result3, flag3 = lineIntersection(p1, p2, w1, w2)
            if flag3==True:
                return  result3, flag3

            result=None
            flag=False
            return result, flag


    def intersecWithLine(self, w1, w2):

        if self.mode == 'line':

            ########################
            ##  p1-----------------p2   ##
            ########################
            
            p1 = np.array([self.params[0], self.params[1]])
            p2 = np.array([self.params[2], self.params[3]])

            result, flag = lineIntersection(p1, p2, w1, w2)
            if flag:
                return True
            else:
                return False

        if self.mode == 'rect':
            
            ########################
            ### p1-----------------p4 ###
            ###  |                              |  ###
            ###  |                              |  ###
            ###  |                              |  ###
            ### p2-----------------p3 ###
            ########################
            
            p1 = np.array([self.params[0], self.params[1]])
            p2 = np.array([self.params[0], self.params[3]])
            p3 = np.array([self.params[2], self.params[3]])
            p4 = np.array([self.params[2], self.params[1]])

            #w1 = np.array([wall.params[0],wall.params[1]])
            #w2 = np.array([wall.params[2],wall.params[3]])
            
            result1, flag1 = lineIntersection(p1, p2, w1, w2)
            result2, flag2 = lineIntersection(p2, p3, w1, w2)
            result3, flag3 = lineIntersection(p3, p4, w1, w2)
            result4, flag4 = lineIntersection(p4, p1, w1, w2)

            if flag1 or flag2 or flag3 or flag4:
                return True
            else:
                return False
        

    # For preprocessing data of doors and walls
    def findAttachedDoors(self, doors):

        # A list used to store walls which the door is attached to
        self.attachedDoors=[]
        
        if self.mode == 'line':
            
            ########################
            ##  w1-----------------w2   ##
            ########################
            
            w1 = np.array([self.params[0], self.params[1]])
            w2 = np.array([self.params[2], self.params[3]])
            
            for door in doors:
                if door.inComp ==0:
                    continue

                ########################
                ### p1-----------------p4 ###
                ###  |                              |  ###
                ###  |                              |  ###
                ###  |                              |  ###
                ### p2-----------------p3 ###
                ########################
                
                p1 = np.array([door.params[0], door.params[1]])
                p2 = np.array([door.params[0], door.params[3]])
                p3 = np.array([door.params[2], door.params[3]])
                p4 = np.array([door.params[2], door.params[1]])

                flag1 = self.intersecWithLine(p1, p2)
                flag2 = self.intersecWithLine(p2, p3)
                flag3 = self.intersecWithLine(p3, p4)
                flag4 = self.intersecWithLine(p4, p1)

               #if flag:
               #    return wall
               # One wall is returned.  Problem exists if a door is attached with two walls

                if flag1 or flag2 or flag3 or flag4:
                    self.attachedDoors.append(door)

        if self.mode == 'rect':
            
            ########################
            ### w1-----------------w4  ##
            ###  |                              |  ###
            ###  |                              |  ###
            ###  |                              |  ###
            ### w2-----------------w3  ##
            ########################
            
            w1 = np.array([self.params[0], self.params[1]])
            w2 = np.array([self.params[0], self.params[3]])
            w3 = np.array([self.params[2], self.params[3]])
            w4 = np.array([self.params[2], self.params[1]])

            for door in doors:
                if door.inComp ==0:
                    continue

                ########################
                ### p1-----------------p4 ###
                ###  |                              |  ###
                ###  |                              |  ###
                ###  |                              |  ###
                ### p2-----------------p3 ###
                ########################
                
                p1 = np.array([door.params[0], door.params[1]])
                p2 = np.array([door.params[0], door.params[3]])
                p3 = np.array([door.params[2], door.params[3]])
                p4 = np.array([door.params[2], door.params[1]])

                flag1 = self.intersecWithLine(p1, p2)
                flag2 = self.intersecWithLine(p2, p3)
                flag3 = self.intersecWithLine(p3, p4)
                flag4 = self.intersecWithLine(p4, p1)

                ###
                # if a door is within a rectangular wall, it is considered to be attached to the wall
                ###
                if door.params[0]>=self.params[0] and door.params[1]>=self.params[1]:
                    flag5 = True
                else:
                    flag5 = False

                if door.params[2]<=self.params[2] and door.params[3]<=self.params[3]:
                    flag6=True
                else:
                    flag5 = False

                flag0 = flag5 and flag6

                if flag1 or flag2 or flag3 or flag4 or flag0:
                    self.attachedDoors.append(door)

        if len(self.attachedDoors) == 0:
            self.isSingleWall = True

        return self.attachedDoors


    def inside(self, pos):
        if self.mode == 'line':
            return False
        if self.mode == 'rect':
            if pos[0]>=self.params[0] and pos[0]<=self.params[2] and pos[1]>=self.params[1] and pos[1]<=self.params[3]:
                return True
            else:
                return False
    

class passage(object):
    
    """
    screen: (Not used)
        Passages exist on a screen element 
    id:
        door id 
    mode: 
        door type (Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
    """
    
    def __init__(self, oid=0, mode='rect', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        #self.mode = 'rect' # All the door are in form of rect
        self.exitSign = 0

        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])

        self.attachedWalls=[]
        self.inComp = 1
        self.isSingleDoor = False
        self.arrow = 0 # The default doorway direction: Using nearest-exit strategy 
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        #self.pointer1 = np.array([0, 0])
        #self.pointer2 = np.array([0, 0])
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def direction(self, arrow):
        ### +1: +x
        ###  -1: -x
        ### +2: +y
        ###  -2: -y 
        if arrow == 1:
            #direction = -np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            #direction = normalize(direction)
            direction = np.array([1.0, 0.0])
        elif arrow == -1:
            #direction = np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            #direction = normalize(direction)
            direction = np.array([-1.0, 0.0])
        elif arrow == 2:
            #direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            #direction = normalize(direction)
            direction = np.array([0.0, 1.0])
        elif arrow == -2:
            #direction = np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            #direction = normalize(direction)
            direction = np.array([0.0, -1.0])
        elif arrow == 0:
            direction = np.array([0.0, 0.0])
        return direction
            

    def edge(self):
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[0], self.params[3]])
        p3 = np.array([self.params[2], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])
        return p1, p2, p3, p4


    def intersecWithLine(self, w1, w2, mode='onlylogic'):
        # x axis: to right
        # y axit: to downside
        ########################
        ### p1-----------------p4 ###
        ###  |                 |  ###
        ###  |                 |  ###
        ###  |                 |  ###
        ### p2-----------------p3 ###
        ########################
        
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[0], self.params[3]])
        p3 = np.array([self.params[2], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])

        #w1 = np.array([wall.params[0],wall.params[1]])
        #w2 = np.array([wall.params[2],wall.params[3]])

        result1, flag1 = lineIntersection(p1, p2, w1, w2)
        result2, flag2 = lineIntersection(p2, p3, w1, w2)
        result3, flag3 = lineIntersection(p3, p4, w1, w2)
        result4, flag4 = lineIntersection(p4, p1, w1, w2)

        if mode=='onlylogic':
            if flag1 or flag2 or flag3 or flag4:
                return True
            else:
                return False
        else:
            return result1, result2, result3, result4
        

        #if wall.mode == 'line':
            #pass
        #if wall.mode == 'rect':
            #pass
        #return np.array([0.0, 0.0])

        
    def doorForce(self, agent):
        if self.insideDoor(agent.pos)==False:
            doordir = self.direction()
            agentdir = self.pos-agent.pos
            if np.dot(doordir, agentdir)>=0:
                ri = agent.radius
                #mid= (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))/2.0
                dist=np.linalg.norm(self.pos - agent.pos)
                dire = normalize(self.pos-agent.pos)

                first = 1.6*agent.A_WF*np.exp((ri-dist)/agent.B_WF)*dire
                second = 160*exp((2*ri-dist)/1.8)*dire  #0.2)*dire
                return first + second
            else:
                return np.array([0.0, 0.0])
        else:
            if self.arrow == 1 or self.arrow == -1:
                w1= np.array([self.params[0], self.params[1]])
                w2 = np.array([self.params[2], self.params[1]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                #second = -600*exp((2*ri-diw)/0.2)*niw

                w1= np.array([self.params[0], self.params[3]])
                w2 = np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second
            
            if self.arrow == 2 or self.arrow == -2:
                w1= np.array([self.params[0], self.params[1]])
                w2= np.array([self.params[0], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw

                w1= np.array([self.params[2], self.params[1]])
                w2= np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second


    def inside(self, pos):
        if pos[0]>=self.params[0] and pos[0]<=self.params[2] and pos[1]>=self.params[1] and pos[1]<=self.params[3]:
            return True
        else:
            return False


    def visiblePx(self, agent, walls):

        edge1, edge2, edge3, edge4 = self.edge()
        doorEdge=[edge1, edge2, edge3, edge4]
        if self.inside(agent.pos):
            pass

            if np.dot(agent.actualV, doorEdge[0]-agent.pos)<0:
                doorEdge[0]=np.array([0.0, 0.0])
            if np.dot(agent.actualV, doorEdge[1]-agent.pos)<0:
                doorEdge[1]=np.array([0.0, 0.0])
            if np.dot(agent.actualV, doorEdge[2]-agent.pos)<0:
                doorEdge[2]=np.array([0.0, 0.0])
            if np.dot(agent.actualV, doorEdge[3]-agent.pos)<0:
                doorEdge[3]=np.array([0.0, 0.0])

            result=(doorEdge[0]+doorEdge[1]+doorEdge[2]+doorEdge[3])*0.25
            return result
        
        isVisiblePassage=True
        for wall in walls:
            if wall.inComp ==0:
                continue
            result1, flag1 = wall.wallInBetween(agent.pos, edge1)
            result2, flag2 = wall.wallInBetween(agent.pos, edge2)
            result3, flag3 = wall.wallInBetween(agent.pos, edge3)
            result4, flag4 = wall.wallInBetween(agent.pos, edge4)
            result5, flag5 = wall.wallInBetween(agent.pos, self.pos)
            if flag1 and flag2 and flag3 and flag4 and flag5:
                isVisiblePassage=False
                return None
            
            if flag1:
                doorEdge[0]=np.array([0.0, 0.0])
            if flag2:
                doorEdge[1]=np.array([0.0, 0.0])
            if flag3:
                doorEdge[2]=np.array([0.0, 0.0])
            if flag4:
                doorEdge[3]=np.array([0.0, 0.0])
            
        result=(doorEdge[0]+doorEdge[1]+doorEdge[2]+doorEdge[3])*0.25
        return result


    # For preprocessing the data of geom
    def computePos(self):
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5
        return self.pos
    
    # For preprocessing data of doors and walls
    def findAttachedWalls(self, walls, mode='onlyFindWalls'):

        ########################
        ### p1-----------------p4 ###
        ###  |                 |  ###
        ###  |                 |  ###
        ###  |                 |  ###
        ### p2-----------------p3 ###
        ########################

        # A list used to store walls which the door is attached to
        self.attachedWalls=[]
        
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[0], self.params[3]])
        p3 = np.array([self.params[2], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])

        for wall in walls:
            if wall.inComp ==0:
                continue
            if wall.mode == 'line':
                
                ########################
                ##  w1-----------------w2   ##
                ########################
                
                w1 = np.array([wall.params[0], wall.params[1]])
                w2 = np.array([wall.params[2], wall.params[3]])

                flag = self.intersecWithLine(w1, w2)

               #if flag:
               #    return wall
               # One wall is returned.  Problem exists if a door is attached with two walls

                if flag:
                    self.attachedWalls.append(wall)
                
            if wall.mode == 'rect':
                
                ########################
                ### w1-----------------w4  ###
                ###  |                 |   ###
                ###  |                 |   ###
                ###  |                 |   ###
                ### w2-----------------w3  ###
                ########################
                
                w1 = np.array([wall.params[0], wall.params[1]])
                w2 = np.array([wall.params[0], wall.params[3]])
                w3 = np.array([wall.params[2], wall.params[3]])
                w4 = np.array([wall.params[2], wall.params[1]])

                flag1 = self.intersecWithLine(w1, w2)
                flag2 = self.intersecWithLine(w2, w3)
                flag3 = self.intersecWithLine(w3, w4)
                flag4 = self.intersecWithLine(w4, w1)

                ###
                # if a door is within a rectangular wall, it is considered to be attached to the wall
                ###
                if self.params[0]>=wall.params[0] and self.params[1]>=wall.params[1]:
                    flag5 = True
                else:
                    flag5 = False

                if self.params[2]<=wall.params[2] and self.params[3]<=wall.params[3]:
                    flag6 = True
                else:
                    flag6 = False

                flag0 = flag5 and flag6

                if flag1 or flag2 or flag3 or flag4 or flag0:
                    self.attachedWalls.append(wall)

        if len(self.attachedWalls) == 0:
            self.isSingleDoor = True                    
                            
        return self.attachedWalls


    # Test if the attached walls intersect with any edge of the door
    # Return the average positions of the intersection points if any
        ##############################
        ### p1--------z4--------p4 ###
        ###  |                  |  ###
        ### z1                  z3 ###
        ###  |                  |  ###
        ### p2--------z2--------p3 ###
        ##############################
    def dirWithAttachedWalls(self, mode='average'):
        if len(self.attachedWalls) == 0:
            self.arrow = 0
        else:
            #z1=np.array([0.0, 0.0])
            #z2=np.array([0.0, 0.0])
            #z3=np.array([0.0, 0.0])
            #z4=np.array([0.0, 0.0])
            z1 = []
            z2 = []
            z3 = []
            z4 = []
            for wall in self.attachedWalls:
                if wall.mode == 'line':
                    w1 = np.array([wall.params[0], wall.params[1]])
                    w2 = np.array([wall.params[2], wall.params[3]])
                    pt1, pt2, pt3, pt4 = self.intersecWithLine(w1, w2, 'findCrossPoint')
                    
                    #intersecPt = []
                    #if pt1 is None:
                    #    pt1=np.array([0.0, 0.0])
                    #if pt2 is None:
                    #    pt2=np.array([0.0, 0.0])
                    #if pt3 is None:
                    #    pt3=np.array([0.0, 0.0])
                    #if pt4 is None:
                    #    pt4=np.array([0.0, 0.0])

                    if pt1 is None:
                        pass
                    else:
                        z1.append(pt1[1])

                    if pt2 is None:
                        pass
                    else:
                        z2.append(pt2[0])

                    if pt3 is None:
                        pass
                    else:
                        z3.append(pt3[1])

                    if pt4 is None:
                        pass
                    else:                    
                        z4.append(pt4[0])

                if wall.mode == 'rect':
                    
                    w1 = np.array([wall.params[0], wall.params[1]])
                    w2 = np.array([wall.params[0], wall.params[3]])
                    w3 = np.array([wall.params[2], wall.params[3]])
                    w4 = np.array([wall.params[2], wall.params[1]])

                    pt1, pt2, pt3, pt4 = self.intersecWithLine(w1, w2, 'findCrossPoint')

                    if pt1 is None:
                        pass
                    else:
                        z1.append(pt1[1])

                    if pt2 is None:
                        pass
                    else:
                        z2.append(pt2[0])

                    if pt3 is None:
                        pass
                    else:
                        z3.append(pt3[1])

                    if pt4 is None:
                        pass
                    else:                    
                        z4.append(pt4[0])
                        
                    pt1, pt2, pt3, pt4 = self.intersecWithLine(w2, w3, 'findCrossPoint')

                    if pt1 is None:
                        pass
                    else:
                        z1.append(pt1[1])

                    if pt2 is None:
                        pass
                    else:
                        z2.append(pt2[0])

                    if pt3 is None:
                        pass
                    else:
                        z3.append(pt3[1])

                    if pt4 is None:
                        pass
                    else:                    
                        z4.append(pt4[0])
                        
                    pt1, pt2, pt3, pt4 = self.intersecWithLine(w3, w4, 'findCrossPoint')

                    if pt1 is None:
                        pass
                    else:
                        z1.append(pt1[1])

                    if pt2 is None:
                        pass
                    else:
                        z2.append(pt2[0])

                    if pt3 is None:
                        pass
                    else:
                        z3.append(pt3[1])

                    if pt4 is None:
                        pass
                    else:                    
                        z4.append(pt4[0])
                    
                    pt1, pt2, pt3, pt4 = self.intersecWithLine(w4, w1, 'findCrossPoint')

                    if pt1 is None:
                        pass
                    else:
                        z1.append(pt1[1])

                    if pt2 is None:
                        pass
                    else:
                        z2.append(pt2[0])

                    if pt3 is None:
                        pass
                    else:
                        z3.append(pt3[1])

                    if pt4 is None:
                        pass
                    else:                    
                        z4.append(pt4[0])
                        
        #if len(z1)==0 and len(z3)==0 and len(z2)>0 and len(z4)>0:
        #    self.arrow = 1

        #if z1 is not None and z3 is not None and z2 is None and z4 is None:
        #if len(z1)>0 and len(z3)>0 and len(z2)==0 and len(z4)==0:
        #    self.arrow = 2
        if mode == 'average':
            r1 = None
            r2 = None
            r3 = None
            r4 = None

            if len(z1)>0:
                r1 = sum(z1)/len(z1)
            if len(z2)>0:
                r2 = sum(z2)/len(z2)
            if len(z3)>0:
                r3 = sum(z3)/len(z3)
            if len(z4)>0:
                r4 = sum(z4)/len(z4)
            return r1, r2, r3, r4
        
        elif mode == 'maxmin':
            r1 = None
            r2 = None
            r3 = None
            r4 = None
            
            if len(z1)>0:
                r1 = np.sort(z1)
            if len(z2)>0:
                r2 = np.sort(z2)
            if len(z3)>0:
                r3 = np.sort(z3)
            if len(z4)>0:
                r4 = np.sort(z4)                                        
            return r1, r2, r3, r4
        else:
            return z1, z2, z3, z4
            

        '''
            if not flag1 and not flag2:
                return (edge1+edge2)*0.5
            if not flag2 and not flag3:
                return (edge2+edge3)*0.5
            if not flag4 and not flag3:
                return (edge4+edge3)*0.5
            if not flag1 and not flag4:
                return (edge1+edge4)*0.5
        '''


if __name__ == '__main__':
    obst = obst()
    print ('OBST Test OK')
    
    doorTest2 = passage()
    doorTest2.params = np.array([60.3, 3.0, 66.0, 6.0])
    doorTest2.arrow = -2
    #doorTest2.visiblePx(pos, walls):
    print (doorTest2.direction(-2))
    print (doorTest2.edge())

    doorTest3 = passage()
    doorTest3.params = np.array([18.9, 16, 23, 20])
    doorTest3.arrow = 1
    print (doorTest3.direction(doorTest3.arrow))
    print ('DOOR Test OK')
