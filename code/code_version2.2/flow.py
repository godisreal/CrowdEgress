

import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#from mpl_toolkits.mplot3d import Axes3D
import pygame
import pygame.draw
from math_func import*
from draw_func import*
#from data_func import*


def build_single_sink(x_min, y_min, x_max, y_max, x_points, y_points, exit):

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    meshSINK = np.zeros((x_points, y_points))
    
    #pxl=int(exit.params[0]/del_x)
    #pyl=int(exit.params[1]/del_y)
    #pxh=int(exit.params[2]/del_x)
    #pyh=int(exit.params[3]/del_y)
    xIndex=int(((exit.params[0]+exit.params[2])/2-x_min)/del_x)
    yIndex=int(((exit.params[1]+exit.params[3])/2-y_min)/del_y)
    meshSINK[xIndex,yIndex]=-200.0
    
    result = np.zeros((x_points+2, y_points+2))
    result[1:x_points+1, 1:y_points+1] = meshSINK
    return result


def build_sink(x_min, y_min, x_max, y_max, x_points, y_points, exits):

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    meshSINK = np.zeros((x_points, y_points))
    for exit in exits:
        #pxl=int(exit.params[0]/del_x)
        #pyl=int(exit.params[1]/del_y)
        #pxh=int(exit.params[2]/del_x)
        #pyh=int(exit.params[3]/del_y)
        xIndex=int(((exit.params[0]+exit.params[2])/2-x_min)/del_x)
        yIndex=int(((exit.params[1]+exit.params[3])/2-y_min)/del_y)
        meshSINK[xIndex,yIndex]=-200.0
    result = np.zeros((x_points+2, y_points+2))
    result[1:x_points+1, 1:y_points+1] = meshSINK
    return result
    

def build_compartment(x_min, y_min, x_max, y_max, x_points, y_points, walls, doors, exits):

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    meshBLD = np.ones((x_points, y_points))

    #walls = readOBST(FN_FDS, '&OBST', 0.0, 3.0, 'obst_test.csv')
    #doors = readPATH(FN_FDS, '&HOLE', 0.0, 3.0, 'hole_test.csv')
    #exits = readEXIT(FN_FDS, '&EXIT', 0.0, 3.0, 'exit_test.csv')
    for wall in walls:
        if wall.mode=='line':
            pxl=int((wall.params[0]-x_min)/del_x)
            pyl=int((wall.params[1]-y_min)/del_y)
            pxh=int((wall.params[2]-x_min)/del_x)
            pyh=int((wall.params[3]-y_min)/del_y)
            compareWL=fabs(pxh-pxl)-fabs(pyh-pyl)
            width=fabs(pxh-pxl)
            length=fabs(pyh-pyl)
            if compareWL>=0:
                #k=(wall.params[3]-wall.params[1])/(wall.params[2]-wall.params[0])
                #for i in range(pxl, pxh):
                    #xxx=wall.params[0]+i*del_x
                    #j=int(k*i-k*pxl+pyl)
                    #j=int((k*xxx-k*wall.params[0]+wall.params[1])/del_y)
                    #meshBLD[i,j]=0.0
                
                k=(wall.params[3]-wall.params[1])/(wall.params[2]-wall.params[0])
                for i in range(pxl, pxh+1):
                    #xxx=wall.params[0]+i*del_x
                    #j=int(k*i-k*pxl+pyl)
                    xxx=i*del_x+x_min
                    j=int((k*xxx-k*wall.params[0]+wall.params[1]-y_min)/del_y)
                    meshBLD[i,j]=0.0
                    
                for i in range(pxh, pxl+1):
                    #xxx=wall.params[0]+i*del_x
                    #j=int(k*i-k*pxl+pyl)
                    xxx=i*del_x+x_min
                    j=int((k*xxx-k*wall.params[0]+wall.params[1]-y_min)/del_y)
                    meshBLD[i,j]=0.0
                    
            if compareWL<0:
                #k=(wall.params[2]-wall.params[0])/(wall.params[3]-wall.params[1])
                #for j in range(pyl, pyh):
                    #yyy=wall.params[1]+j*del_y
                    #i=int(k*j-k*pyl+pxl)
                    #i=int((k*yyy-k*wall.params[1]+wall.params[0])/del_x)
                    #meshBLD[i,j]=0.0
                
                k=(wall.params[2]-wall.params[0])/(wall.params[3]-wall.params[1])
                for j in range(pyl, pyh+1):
                    #yyy=wall.params[1]+j*del_y
                    #i=int(k*j-k*pyl+pxl)
                    yyy=j*del_y+y_min
                    i=int((k*yyy-k*wall.params[1]+wall.params[0]-x_min)/del_x)
                    meshBLD[i,j]=0.0

                for j in range(pyh, pyl+1):
                    #yyy=wall.params[1]+j*del_y
                    #i=int(k*j-k*pyl+pxl)
                    yyy=j*del_y+y_min
                    i=int((k*yyy-k*wall.params[1]+wall.params[0]-x_min)/del_x)
                    meshBLD[i,j]=0.0                    
                
                
        if wall.mode=='rect':
            pxl=int((wall.params[0]-x_min)/del_x)
            pyl=int((wall.params[1]-y_min)/del_y)
            pxh=int((wall.params[2]-x_min)/del_x)
            pyh=int((wall.params[3]-y_min)/del_y)
            #compareWL=fabs(pxh-pxl)-fabs(pyh-pyl)
            #for i in range(pxl, pxh+1):
            #    for j in range(pyl, pyh+1):
            #        meshBLD[i,j]=0.0
            
            for i in range(pxh, pxl+1):
                for j in range(pyh, pyl+1):
                    meshBLD[i,j]=0.0
            for i in range(pxl, pxh+1):
                for j in range(pyl, pyh+1):
                    meshBLD[i,j]=0.0
            for i in range(pxh, pxl+1):
                for j in range(pyl, pyh+1):
                    meshBLD[i,j]=0.0
            for i in range(pxl, pxh+1):
                for j in range(pyh, pyl+1):
                    meshBLD[i,j]=0.0                 
                    
    for door in doors:
        pxl=int((door.params[0]-x_min)/del_x)
        pyl=int((door.params[1]-y_min)/del_y)
        pxh=int((door.params[2]-x_min)/del_x)
        pyh=int((door.params[3]-y_min)/del_y)
        for i in range(pxl, pxh+1):
            for j in range(pyl, pyh+1):
                meshBLD[i,j]=1.0
        for i in range(pxh, pxl+1):
            for j in range(pyl, pyh+1):
                meshBLD[i,j]=1.0
        for i in range(pxl, pxh+1):
            for j in range(pyh, pyl+1):
                meshBLD[i,j]=1.0
        for i in range(pxh, pxl+1):
            for j in range(pyh, pyl+1):
                meshBLD[i,j]=1.0
                                
                    
    for exit in exits:
        pxl=int((exit.params[0]-x_min)/del_x)
        pyl=int((exit.params[1]-y_min)/del_y)
        pxh=int((exit.params[2]-x_min)/del_x)
        pyh=int((exit.params[3]-y_min)/del_y)
        for i in range(pxl, pxh+1):
            for j in range(pyl, pyh+1):
                meshBLD[i,j]=1.0
        for i in range(pxh, pxl+1):
            for j in range(pyl, pyh+1):
                meshBLD[i,j]=1.0
        for i in range(pxl, pxh+1):
            for j in range(pyh, pyl+1):
                meshBLD[i,j]=1.0
        for i in range(pxh, pxl+1):
            for j in range(pyh, pyl+1):
                meshBLD[i,j]=1.0
                
    # Return the final result
    result = np.zeros((x_points+2, y_points+2))
    result[1:x_points+1, 1:y_points+1] = meshBLD
    return result

    

def possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLD, it_points = 200, saveData=False, showPlot=False, showGrad=True):
    # it_points is the number of iteration points


    #f = open("log.txt", "w+")

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)

    print('xy info')
    print(x)
    print(y)

    p = np.zeros((x_points+2, y_points+2))  # Pressure = 0 at all points except boundary points
    p[0,:] = 0       # Dirichlet boundary condition p = 0 at x = 0
    p[-1,:] = 0      # Dirichlet boundary condition p = 0 at x = 2
    p[:, 0] = 0     # Dirichlet boundary condition p = 0 at y = 0
    p[:, -1] = 0    # Dirichlet boundary condition p = 0 at y = 1

    '''
    b = np.zeros((x_points+2, y_points+2))      # RHS in Poisson's equation
    #b[x_points/4, y_points/4] = 100.0       # Spikes in b_ij
    b[3*x_points/4, 3*y_points/4] = -260.0

    BLD=np.ones((x_points+2, y_points+2))
    # Compartment Boundary
    BLD[0:6,int(y_points/2)]=0.0
    BLD[-6:-1,int(y_points/2)]=0.0
    #BLD[:,int(y_points/2)]=0.0
    '''
    
    if np.shape(b)!= (x_points+2, y_points+2): 
        print('\nError in input data b \n')
        f.write('\nError in input data b \n')
        raw_input('\nError in input data b \n Please check!')

    if np.shape(BLD)!= (x_points+2, y_points+2): 
        print('\nError in input data BLD \n')
        f.write('\nError in input data BLD \n')
        raw_input('\nError in input data BLD \n Please check!')

    p=p*BLD
    # Loop through iterations
    p_new = np.zeros((x_points+2, y_points+2))

    for it in range(0, it_points):
        for ix in range(1, x_points + 1):
            for iy in range(1, y_points + 1):
                if BLD[ix,iy]==0:
                    p_new[ix, iy] = 0.0
                    continue
                p_new[ix, iy] = (del_y ** 2 * (p[ix + 1, iy] + p[ix - 1, iy]) + del_x ** 2 * (
                            p[ix, iy + 1] + p[ix, iy - 1]) - (b[ix, iy] * del_x ** 2 * del_y ** 2)) / (
                                            float(2) * (del_x ** 2 + del_y ** 2))
        p = p_new.copy()
        p[0, :] = 0  # Dirichlet boundary condition p = 0 at x = 0
        p[-1, :] = 0  # Dirichlet boundary condition p = 0 at x = 2
        p[:, 0] = 0  # Dirichlet boundary condition p = 0 at y = 0
        p[:, -1] = 0  # Dirichlet boundary condition p = 0 at y = 1
        p = p*BLD

    # Loop through iterations
    Ud = np.zeros((x_points+2, y_points+2))
    Vd = np.zeros((x_points+2, y_points+2))
    for i in range(1, x_points + 1):
        for j in range(1, y_points + 1):
            if BLD[i,j]==0.0:
                Ud[i,j] = 0.0
                Vd[i,j] = 0.0
                continue
            
            Ud[i,j]=(p[i+1,j]-p[i-1,j])/(2*del_x)
            Vd[i,j]=(p[i,j+1]-p[i,j-1])/(2*del_y)

    if saveData:
        np.save("Ud.npy",Ud[1:-1, 1:-1])
        np.save("Vd.npy",Vd[1:-1, 1:-1])

    if showPlot:
        # Plotting pressure p
        #fig = plt.figure(figsize=(x_points,y_points))
        fig = plt.figure()
        ax = Axes3D(fig)
        #ax = fig.gca(projection = '3d')
        X,Y = np.meshgrid(x,y)
        surf = ax.plot_surface(X, Y, p[1:x_points+1,1:y_points+1], cmap=cm.coolwarm)
        plt.show()
        
    return Ud, Vd



def draw_vel(x_min, y_min, x_max, y_max, Ud, Vd, BLDindex, walls, doors, exits, ZOOMFACTOR=20.0, xSpace=0.0, ySpace=0.0):

#def draw_vel(x_max, y_max, BLDindex, walls, doors, exits):
    #Ud=np.load("Ud.npy")
    #Vd=np.load("Vd.npy")
    print(np.shape(Ud))
    (dimX,dimY)=np.shape(Ud)

    #print(dimX, dimY)
    #dim=np.shape(U)
    print(dimX, dimY)

    #dimX is x_points+2
    #dimY is y_points+2

    del_x = (x_max-x_min)/float(dimX - 3)
    del_y = (y_max-y_min)/float(dimY - 3)
    
    xDim=np.linspace(x_min, x_max+2*del_x, dimX) #Should be the same as x
    yDim=np.linspace(y_min, y_max+2*del_y, dimY) #Should be the same as y
    print("Dim info:\n")
    print(xDim)
    print(yDim)


    # Visualize gradient field by pygame
    SCREENSIZE = [800, 600]
    RESOLUTION = 180
    BACKGROUNDCOLOR = [255,255,255]
    LINECOLOR = [255,0,0]
    VECFACTOR = 0.3
    SHOWDATA=False

    IndianRed=205,92,92
    tan = 210,180,140
    skyblue = 135,206,235
    orange = 255,128,0
    khaki = 240,230,140
    black = 0,0,0

    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Gradient Field')
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
            # elif event.type == pygame.MOUSEBUTTONUP:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
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

        screen.fill(BACKGROUNDCOLOR)
        xyShift = np.array([xSpace, ySpace])

        for i in range(dimX):
            for j in range(dimY):
                if BLDindex[i,j]==0:
                    startPos = np.array([xDim[i],yDim[j]]) #np.array([int(xDim[i]),int(yDim[j])])
                    endPos = np.array([int(xDim[i]),int(yDim[j])])
                    #pygame.draw.circle(screen, [0,60,0], startPos*ZOOMFACTOR, 6, 2)
                    pygame.draw.line(screen, [0,60,0], startPos*ZOOMFACTOR-[0,0.8]+xyShift, startPos*ZOOMFACTOR+[0,0.8]+xyShift, 2)
                else:
                    vec=np.array([Ud[i,j],Vd[i,j]])
                    startPos = np.array([xDim[i],yDim[j]])
                    endPos = startPos + VECFACTOR*normalize(vec) #
                    pygame.draw.line(screen, [255,60,0], startPos*ZOOMFACTOR+xyShift, endPos*ZOOMFACTOR+xyShift, 2)

        drawWalls(screen, walls, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        drawExits(screen, exits, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        
        pygame.display.flip()
        clock.tick(20)


	
if __name__=="__main__":

    x_min = -2.0
    y_min = -2.0 
    x_max = 35.0           # Max domain in X
    y_max = 35.0           # Max domain in Y
    x_points = 90       # Number of grid points in X
    y_points = 90       # Number of grid points in Y

    from data_func import*
    #FN_FDS='E:\gitwork\CrowdEgress\examples\evac_memory_test\evac_memory_test0.fds'
    #FN_FDS='E:\gitwork\CrowdEgress\examples\crowdFlow\DoorFlowExample.fds'
    FN_FDS='E:\gitwork\CrowdEgress\examples\Compartment_4Exits_2020\TPRE_DET2.fds'
    walls = readOBST(FN_FDS, '&OBST', 0.0, 3.0, 'obst_test.csv')
    doors = readPATH(FN_FDS, '&HOLE', 0.0, 3.0, 'hole_test.csv')
    exits = readEXIT(FN_FDS, '&EXIT', 0.0, 3.0, 'exit_test.csv')

    b = build_single_sink(x_min, y_min, x_max, y_max, x_points, y_points, exits[0])
    #b = np.zeros((x_points+2, y_points+2))      # RHS in Poisson's equation
    #b[x_points/4, y_points/4] = 100.0       # Spikes in b_ij
    #b[3*x_points/4, 3*y_points/4] = -260.0

    BLDinfo=build_compartment(x_min, y_min, x_max, y_max, x_points, y_points, walls, doors, exits)
    #BLD=np.ones((x_points+2, y_points+2))
    # Compartment Boundary
    #BLD[0:6,int(y_points/2)]=0.0
    #BLD[-6:-1,int(y_points/2)]=0.0
    #BLD[:,int(y_points/2)]=0.0
    
    Ud, Vd = possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLDinfo, 200, True, True)
    draw_vel(x_min, y_min, x_max, y_max, Ud, Vd, BLDinfo, walls, doors, exits)
    
    
