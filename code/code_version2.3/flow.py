
import os, sys
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
    xIndex=int(round(((exit.params[0]+exit.params[2])/2-x_min)/del_x))
    yIndex=int(round(((exit.params[1]+exit.params[3])/2-y_min)/del_y))
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
        xIndex=int(round(((exit.params[0]+exit.params[2])/2-x_min)/del_x))
        yIndex=int(round(((exit.params[1]+exit.params[3])/2-y_min)/del_y))
        meshSINK[xIndex,yIndex]=-200.0
    result = np.zeros((x_points+2, y_points+2))
    result[1:x_points+1, 1:y_points+1] = meshSINK
    return result
    

def build_exitpt(x_min, y_min, x_max, y_max, x_points, y_points, exits):

    del_x = (x_max-x_min)/float(x_points - 1)
    del_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    meshSINK = np.ones((x_points, y_points))
    for exit in exits:
        #pxl=int(exit.params[0]/del_x)
        #pyl=int(exit.params[1]/del_y)
        #pxh=int(exit.params[2]/del_x)
        #pyh=int(exit.params[3]/del_y)
        xIndex=int(round(((exit.params[0]+exit.params[2])/2-x_min)/del_x))
        yIndex=int(round(((exit.params[1]+exit.params[3])/2-y_min)/del_y))
        meshSINK[xIndex,yIndex]=0.0
    result = np.ones((x_points+2, y_points+2))
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
            pxl=int(round((wall.params[0]-x_min)/del_x))
            pyl=int(round((wall.params[1]-y_min)/del_y))
            pxh=int(round((wall.params[2]-x_min)/del_x))
            pyh=int(round((wall.params[3]-y_min)/del_y))
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
                    j=int(round((k*xxx-k*wall.params[0]+wall.params[1]-y_min)/del_y))
                    meshBLD[i,j]=0.0
                    
                for i in range(pxh, pxl+1):
                    #xxx=wall.params[0]+i*del_x
                    #j=int(k*i-k*pxl+pyl)
                    xxx=i*del_x+x_min
                    j=int(round((k*xxx-k*wall.params[0]+wall.params[1]-y_min)/del_y))
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
                    i=int(round((k*yyy-k*wall.params[1]+wall.params[0]-x_min)/del_x))
                    meshBLD[i,j]=0.0

                for j in range(pyh, pyl+1):
                    #yyy=wall.params[1]+j*del_y
                    #i=int(k*j-k*pyl+pxl)
                    yyy=j*del_y+y_min
                    i=int(round((k*yyy-k*wall.params[1]+wall.params[0]-x_min)/del_x))
                    meshBLD[i,j]=0.0                    
                
                
        if wall.mode=='rect':
            pxl=int(round((wall.params[0]-x_min)/del_x))
            pyl=int(round((wall.params[1]-y_min)/del_y))
            pxh=int(round((wall.params[2]-x_min)/del_x))
            pyh=int(round((wall.params[3]-y_min)/del_y))
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
        pxl=int(round((door.params[0]-x_min)/del_x))
        pyl=int(round((door.params[1]-y_min)/del_y))
        pxh=int(round((door.params[2]-x_min)/del_x))
        pyh=int(round((door.params[3]-y_min)/del_y))
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
        pxl=int(round((exit.params[0]-x_min)/del_x))
        pyl=int(round((exit.params[1]-y_min)/del_y))
        pxh=int(round((exit.params[2]-x_min)/del_x))
        pyh=int(round((exit.params[3]-y_min)/del_y))
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

    

def possion_func(x_min, y_min, x_max, y_max, x_points, y_points, b, BLD, it_points = 200, saveData=False, showPlot=False, showGrad=True, mode='simple'):
    # it_points is the number of iteration points


    f = open("log_flow.txt", "a")

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
        if sys.version_info[0] == 2:
            raw_input('\nError in input data b \n Please check!')

    if np.shape(BLD)!= (x_points+2, y_points+2):
        print('\nError in input data BLD \n')
        f.write('\nError in input data BLD \n')
        if sys.version_info[0] == 2:
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

        if mode == 'simple':
            p = p*BLD
        
        # None-slip method
        if mode == 'none-slip':
            for ix in range(1, x_points + 1):
                for iy in range(1, y_points + 1):
                    if BLD[ix,iy]!=0.0 and BLD[ix+1,iy]==0:
                        p[ix, iy]= p[ix-1, iy]
                    if BLD[ix,iy]!=0.0 and BLD[ix-1,iy]==0:
                        p[ix, iy]= p[ix+1, iy]
                    if BLD[ix,iy]!=0.0 and BLD[ix,iy+1]==0:
                        p[ix, iy]= p[ix, iy-1]
                    if BLD[ix,iy]!=0.0 and BLD[ix,iy-1]==0:
                        p[ix, iy]= p[ix, iy+1]   

    # Loop through iterations
    Ud = np.zeros((x_points+2, y_points+2))
    Vd = np.zeros((x_points+2, y_points+2))
    for i in range(1, x_points + 1):
        for j in range(1, y_points + 1):
            if BLD[i,j]==0.0:
                Ud[i,j] = 0.0
                Vd[i,j] = 0.0
                continue
            
            # Discuss whether there is wall on left or right
            if BLD[i,j]!=0.0 and BLD[i+1,j]==0:
                Ud[i,j]=(p[i,j]-p[i-1,j])/(del_x)
            elif BLD[i,j]!=0.0 and BLD[i-1,j]==0:
                Ud[i,j]=(p[i+1,j]-p[i,j])/(del_x)
            else:
                Ud[i,j]=(p[i+1,j]-p[i-1,j])/(2*del_x)

            # Discuss whether there is wall on upside or downside
            if BLD[i,j]!=0.0 and BLD[i,j+1]==0:
                Vd[i,j]=(p[i,j]-p[i,j-1])/(del_y)
            elif BLD[i,j]!=0.0 and BLD[i,j-1]==0:
                Vd[i,j]=(p[i,j+1]-p[i,j])/(del_y)
            else:
                Vd[i,j]=(p[i,j+1]-p[i,j-1])/(2*del_y)

            # This is a simple method: No surrounding walls are considered
            #Ud[i,j]=(p[i+1,j]-p[i-1,j])/(2*del_x)
            #Vd[i,j]=(p[i,j+1]-p[i,j-1])/(2*del_y)

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
        
    f.close()
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

        #drawWalls(screen, walls, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x/2.0+xSpace, ZOOMFACTOR*del_y/2.0+ySpace)
        drawWalls(screen, walls, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x+xSpace, ZOOMFACTOR*del_y+ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x+xSpace, ZOOMFACTOR*del_y+ySpace)
        drawExits(screen, exits, ZOOMFACTOR, SHOWDATA, ZOOMFACTOR*del_x+xSpace, ZOOMFACTOR*del_y+ySpace)
        
        pygame.display.flip()
        clock.tick(20)

#def lwr2D()

'''
def convec2D(x_min, y_min, x_max, y_max, x_points, y_points, D_t, t_end, bldInfo, R0, U0, V0, Rdes, Udes, Vdes, mode=1, saveData=True, showPlot=False, debug=True):

    vf=1.36
    rm=1.0

    D_x = (x_max-x_min)/float(x_points - 1)
    D_y = (y_max-y_min)/float(y_points - 1)

    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    Nx=len(x)
    Ny=len(y)
    Nt=int(floor(t_end/D_t))

    Rt=np.zeros((Nx+2,Ny+2,Nt))
    BLD=np.ones((Nx+2,Ny+2))

    # Set Rect Area for Computation
    BLD[0,:]=0.0
    BLD[:,0]=0.0
    BLD[Nx+1,:]=0.0 #BLD[-1,:]=0.0
    BLD[:,Ny+1]=0.0 #BLD[:,-1]=0.0

    if np.shape(bldInfo)!= (Nx+2, Ny+2): 
        print('\nError in input data BLD \n')
        #f.write('\nError in input data BLD \n')
        input('\nError in input data BLD \n Please check!')
    BLD=bldInfo
    print(BLD)
    
    R=np.zeros((Nx+2,Ny+2))
    U=np.zeros((Nx+2,Ny+2))
    V=np.zeros((Nx+2,Ny+2))

    Rd=np.zeros((Nx+2,Ny+2))
    Ud=np.zeros((Nx+2,Ny+2))
    Vd=np.zeros((Nx+2,Ny+2))
        
    if np.shape(R0)!= (Nx+2,Ny+2) or np.shape(U0)!= (Nx+2,Ny+2) or np.shape(V0)!= (Nx+2,Ny+2): 
        print('\nError in input initial data R/U/V \n')
        f.write('\nError in input initial data R/U/V \n')
        input('\nError in input initial data R/U/V \n Please check!')
    if np.shape(Rdes)!= (Nx+2,Ny+2) or np.shape(Udes)!= (Nx+2,Ny+2) or np.shape(Vdes)!= (Nx+2,Ny+2): 
        print('\nError in input desired matrix Rd/Ud/Vd \n')
        f.write('\nError in input desired matrix Rd/Ud/Vd \n')
        input('\nError in input desired matrix Rd/Ud/Vd \n Please check!')

    #Initialize Mesh Data
    R=R0
    U=U0
    V=V0

    # Give the driving force term
    Rd=Rdes  # Only used in mode=2 currently
    Ud=Udes
    Vd=Vdes
    
    if debug:
        input("Please check input data here!")

    for t in np.arange(0,Nt): #1,2...Nt

        f.write("Time Step:"+str(t)+"==========\n")
        R=R*BLD
        U=U*BLD
        V=V*BLD
        U=U*UBLD
        V=V*VBLD
        #V[3:N-3,int(N/2)-1]=0.0
        #V[3:N-3,int(N/2)+1]=0.0
        
        # Write in time index
        Rt[:,:,t]=R
        Ut[:,:,t]=U 
        Vt[:,:,t]=V ##=np.zeros((N+3,N+3,Nt+1))

    #u = np.ones((x_points,y_points))
    #for i in range(0, x_points):    # Specifying the boundary conditions
    #    for j in range(0, y_points):
    #        if (x[i] > 0.5 and x[i] < 1.0):
    #            if (y[j] > 0.5 and y[j] < 1.0):
    #                u[i,j] = 2.0
    
    # Looping for time steps
    u_new = np.ones((x_points, y_points))

    for it in range(0, t_points):
        for ix in range(1, x_points):
            for iy in range(1, y_points):
                u_new[ix,iy] = u[ix,iy] - c*(del_t/float(del_x))*(u[ix,iy] - u[ix-1,iy]) - c*(del_t/float(del_y))*(u[ix,iy] - u[ix,iy-1])
                u_new[0,:] = 1.0
                u_new[:,-1] = 1.0
                u_new[-1,:] = 1.0
                u_new[:,0] = 1.0

        u = u_new.copy()

    if saveData:
        np.save("Rt.npy",Rt)
        np.save("Ut.npy",Ut)
        np.save("Vt.npy",Vt)
        
    # Plotting the 2D surface
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    X,Y = np.meshgrid(x,y)
    surf = ax.plot_surface(X, Y, u[:], cmap=cm.coolwarm)
    plt.show()
'''
    

def lwr2D(x_min, y_min, x_max, y_max, x_points, y_points, t_end, bldInfo, R0, U0, V0, Rdes, Udes, Vdes, exitpt, mode=1, debug=True): #saveData=False, showPlot=False, 

    # Computation Parameters
    #x_points       # Number of grid points in X
    #y_points       # Number of grid points in Y
    # mode=0: Lax0  mode=1: Lax1  mode=2: StandardDiff
    
    f = open("log_flow.txt", "w")
    
    # Model Parameters
    tow=0.2
    vf=1.36
    Rm=1
    c=0.8
    k1=1.0
    k2=1.0

    #D_x = maxl/float(x_points - 1)
    #D_y = maxw/float(y_points - 1)
    D_x = (x_max-x_min)/float(x_points - 1)
    D_y = (y_max-y_min)/float(y_points - 1)
    D_t = 0.1 
    #courant = 0.6
    #D_t = (D_x + D_y)*courant

    f.write("Dx:" + str(D_x))
    f.write("Dy:" + str(D_y))
    f.write("Dt:" + str(D_t))

    #x = np.linspace(0, maxl, x_points)
    #y = np.linspace(0, maxw, y_points)
    x = np.linspace(x_min, x_max, x_points)
    y = np.linspace(y_min, y_max, y_points)
    
    if debug:
        print("Dx:", D_x)
        print("Dy:", D_y)
    
    if debug:
        print('x:', x, '\n', 'y:', y, '\n')

    '''
    maxl=2
    maxw=2
    D_x=0.2
    D_y=0.2
    # np.arrange() does not include the end point
    # The folowing setup: 0 is the start point; maxl is the end point
    x=np.arange(0,maxl+D_x,D_x) #0,1,...maxl
    y=np.arange(0,maxw+D_y,D_y) #0,1,...maxw
    
    '''

    Nx=len(x)
    Ny=len(y)
    Nt=int(floor(t_end/D_t))
    
    #vf=1.06  # Desired Vx^0 in x axis
    #vff=1.36 # Desired Vy^0 in y axis
    #it_points = 100     # Number of iteration points
    #D_t=0.06
    #t_end=10.0
    #t_index=np.arange(0,Nt+1) #0,1,...Nt
    
    Rt=np.zeros((Nx+2,Ny+2,Nt))
    Ut=np.zeros((Nx+2,Ny+2,Nt))
    Vt=np.zeros((Nx+2,Ny+2,Nt))

    BLD=np.ones((Nx+2,Ny+2))
    UBLD=np.ones((Nx+2,Ny+2))
    VBLD=np.ones((Nx+2,Ny+2))

    # Set Rect Area for Computation
    BLD[0,:]=0.0
    BLD[:,0]=0.0
    BLD[Nx+1,:]=0.0 #BLD[-1,:]=0.0
    BLD[:,Ny+1]=0.0 #BLD[:,-1]=0.0

    if np.shape(bldInfo)!= (Nx+2, Ny+2): 
        print('\nError in input data BLD \n')
        #f.write('\nError in input data BLD \n')
        if sys.version_info[0] == 2:
            raw_input('\nError in input data BLD \n Please check!')
        else:
            input('\nError in input data BLD \n Please check!')
            
    BLD=bldInfo

    print(BLD)
    for i in np.arange(1,Nx+1):
        for j in np.arange(1,Ny+1):
            if BLD[i,j]==0.0:
                pass
            else:
                if BLD[i-1,j]==0 or BLD[i+1,j]==0:
                    UBLD[i,j]=0.0
                if BLD[i,j-1]==0 or BLD[i,j+1]==0:
                    VBLD[i,j]=0.0


    R=np.zeros((Nx+2,Ny+2))
    U=np.zeros((Nx+2,Ny+2))
    V=np.zeros((Nx+2,Ny+2))

    Rd=np.zeros((Nx+2,Ny+2))
    Ud=np.zeros((Nx+2,Ny+2))
    Vd=np.zeros((Nx+2,Ny+2))
        
    if np.shape(R0)!= (Nx+2,Ny+2) or np.shape(U0)!= (Nx+2,Ny+2) or np.shape(V0)!= (Nx+2,Ny+2): 
        print('\nError in input initial data R/U/V \n')
        f.write('\nError in input initial data R/U/V \n')
        if sys.version_info[0] == 2:
            raw_input('\nError in input initial data R/U/V \n Please check!')
    if np.shape(Rdes)!= (Nx+2,Ny+2) or np.shape(Udes)!= (Nx+2,Ny+2) or np.shape(Vdes)!= (Nx+2,Ny+2): 
        print('\nError in input desired matrix Rd/Ud/Vd \n')
        f.write('\nError in input desired matrix Rd/Ud/Vd \n')
        if sys.version_info[0] == 2:
            raw_input('\nError in input desired matrix Rd/Ud/Vd \n Please check!')

    #Initialize Mesh Data
    R=R0
    U=U0
    V=V0

    # Give the driving force term
    Rd=Rdes  # Only used in mode=2 currently
    Ud=Udes
    Vd=Vdes
    
    if debug:
        if sys.version_info[0] == 2:
            raw_input("Please check input data here!")
        else:
            input("Please check input data here!")

    for t in np.arange(0,Nt): #1,2...Nt

        f.write("\n=====================Time Step:"+str(t)+"===========================\n\n")
        R=R*BLD
        U=U*BLD
        V=V*BLD
        #U=U*UBLD
        #V=V*VBLD
        #V[3:N-3,int(N/2)-1]=0.0
        #V[3:N-3,int(N/2)+1]=0.0
        
        # Write in time index
        Rt[:,:,t]=R
        Ut[:,:,t]=U 
        Vt[:,:,t]=V ##=np.zeros((N+3,N+3,Nt+1))

        if mode==0: #Lax0: # Currently there is unsteady problem unsolved
            # Computation in area of 1 to N:
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                    #???[FL] [FR]
                    #FL=FORCE(R[j,i],R[j,i-1],U[j,i],U[j,i-1],V[j,i],V[j,i-1],D_t,D_x,c,0)
                    #FR=FORCE(R[j,i+1],R[j,i],U[j,i+1],U[j,i],V[j,i+1],V[j,i],D_t,D_x,c,0)
                    Qold_iL=np.array([R[i-1,j], R[i-1,j]*U[i-1,j], R[i-1,j]*V[i-1,j]])
                    Qold_iR=np.array([R[i+1,j], R[i+1,j]*U[i+1,j], R[i+1,j]*V[i+1,j]])
                    Qold_jL=np.array([R[i,j-1], R[i,j-1]*U[i,j-1], R[i,j-1]*V[i,j-1]])
                    Qold_jR=np.array([R[i,j+1], R[i,j+1]*U[i,j+1], R[i,j+1]*V[i,j+1]])
                    
                    FQ_iL=np.array([R[i-1,j]*U[i-1,j],R[i-1,j]*U[i-1,j]*U[i-1,j]+c*R[i-1,j],R[i-1,j]*U[i-1,j]*V[i-1,j]])
                    FQ_iR=np.array([R[i+1,j]*U[i+1,j],R[i+1,j]*U[i+1,j]*U[i+1,j]+c*R[i+1,j],R[i+1,j]*U[i+1,j]*V[i+1,j]])
                    if debug:
                        f.write("Time Step:"+str(t)+"==========\n")
                        f.write(str(FQ_iL))
                    
                    GQ_jD=np.array([R[i,j-1]*V[i,j-1],R[i,j-1]*U[i,j-1]*V[i,j-1],R[i,j-1]*V[i,j-1]*V[i,j-1]+c*R[i,j-1]])
                    GQ_jU=np.array([R[i,j+1]*V[i,j+1],R[i,j+1]*U[i,j+1]*V[i,j+1],R[i,j+1]*V[i,j+1]*V[i,j+1]+c*R[i,j+1]])
                    
                    q_new_04=(1/4)*(Qold_iL+Qold_iR+Qold_jL+Qold_jR)-D_t/(D_x)/2*(FQ_iR-FQ_iL)-D_t/(D_y)/2*(GQ_jU-GQ_jD)
                    Rr=q_new_04[0]
                    Uu=q_new_04[1]/(q_new_04[0])
                    Vv=q_new_04[2]/(q_new_04[0])
                    Ud=vf*(1-Rr/Rm)  #%*sign(Uu)
                    Vd=vff*(1-Rr/Rm) #%*sign(Vv)
                    f_s=np.array([0, Rr*(Ud-Uu)/tow, Rr*(Vd-Vv)/tow]) # I think this is problemtic
                    #because Uv and Vv is not the solution of velocity field and they should be replaced by U[i,j] and V[i,j]
                    Q_new_04=q_new_04+D_t*f_s
                    
                    if Q_new_04[0] is not 0.0:
                        R[i,j]=Q_new_04[0]
                        U[i,j]=Q_new_04[1]/(Q_new_04[0])
                        V[i,j]=Q_new_04[2]/(Q_new_04[0])
                    else:
                        R[i,j]=0.0
                        U[i,j]=0.0
                        V[i,j]=0.0

        if mode==1: #Lax: # Currently there is unsteady problem unsolved
            
            # For our paper Fluid-Based Analysis of Crowd Movements
            R_temp=np.zeros((Nx+2,Ny+2))
            U_temp=np.zeros((Nx+2,Ny+2))
            V_temp=np.zeros((Nx+2,Ny+2))
            
            # Computation in area of 1 to N:
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                    if R[i,j]<1.0e-10:
                        continue
                        print(str(t),str(i),str(j))
                    #???[FL] [FR]
                    #FL=FORCE(R[j,i],R[j,i-1],U[j,i],U[j,i-1],V[j,i],V[j,i-1],D_t,D_x,c,0)
                    #FR=FORCE(R[j,i+1],R[j,i],U[j,i+1],U[j,i],V[j,i+1],V[j,i],D_t,D_x,c,0)
                    Qold_iL=np.array([R[i-1,j], R[i-1,j]*U[i-1,j], R[i-1,j]*V[i-1,j]])
                    Qold_iR=np.array([R[i+1,j], R[i+1,j]*U[i+1,j], R[i+1,j]*V[i+1,j]])
                    Qold_jL=np.array([R[i,j-1], R[i,j-1]*U[i,j-1], R[i,j-1]*V[i,j-1]])
                    Qold_jR=np.array([R[i,j+1], R[i,j+1]*U[i,j+1], R[i,j+1]*V[i,j+1]])
                    
                    FQ_iL=np.array([R[i-1,j]*U[i-1,j],R[i-1,j]*U[i-1,j]*U[i-1,j]+c*R[i-1,j],R[i-1,j]*U[i-1,j]*V[i-1,j]])
                    FQ_iR=np.array([R[i+1,j]*U[i+1,j],R[i+1,j]*U[i+1,j]*U[i+1,j]+c*R[i+1,j],R[i+1,j]*U[i+1,j]*V[i+1,j]])
                    
                    GQ_jD=np.array([R[i,j-1]*V[i,j-1],R[i,j-1]*U[i,j-1]*V[i,j-1],R[i,j-1]*V[i,j-1]*V[i,j-1]+c*R[i,j-1]])
                    GQ_jU=np.array([R[i,j+1]*V[i,j+1],R[i,j+1]*U[i,j+1]*V[i,j+1],R[i,j+1]*V[i,j+1]*V[i,j+1]+c*R[i,j+1]])
                    if debug:
                        f.write("FiL:"+str(FQ_iL))
                        f.write("FiR:"+str(FQ_iR))
                        f.write("GjD:"+str(GQ_jD))
                    
                    q_new=(1/4)*(Qold_iL+Qold_iR+Qold_jL+Qold_jR)-D_t/(D_x)/2*(FQ_iR-FQ_iL)-D_t/(D_y)/2*(GQ_jU-GQ_jD)
                    
                    #Rr=q_new_04[0]
                    #Uu=q_new_04[1]/(q_new_04[0])
                    #Vv=q_new_04[2]/(q_new_04[0])
                    #Ud=vf*(1-R[i,j]/Rm)  #%*sign(Uu)
                    #Vd=vff*(1-R[i,j]/Rm) #%*sign(Vv)
                    #f_s=np.array([0, Rr*(Ud-Uu)/tow, Rr*(Vd-Vv)/tow]) # I think this is problemtic
                    #because Uv and Vv is not the solution of velocity field and they should be replaced by U[i,j] and V[i,j]
                    
                    #f_s=np.array([0, R[i,j]*(Ud-U[i,j])/tow, R[i,j]*(Vd-V[i,j])/tow])
                    f_s=np.array([0, R[i,j]*(Ud[i,j]-U[i,j])/tow, R[i,j]*(Vd[i,j]-V[i,j])/tow])
                    #f_s=np.array([0, k1*R[i,j]*(Ud[i,j]-U[i,j])+k2*R[i,j]*(Rd[i,j]-R[i,j])*(R[i+1,j]-R[i-1,j])/2/D_x, k1*R[i,j]*(Vd[i,j]-V[i,j])+k2*R[i,j]*(Rd[i,j]-R[i,j])*(R[i,j+1]-R[i,j-1])/2/D_y])                    
                    Q_new_04=q_new+D_t*f_s
                    
                    if Q_new_04[0] is not 0.0:
                        R_temp[i,j]=Q_new_04[0]
                        U_temp[i,j]=Q_new_04[1]/(Q_new_04[0])
                        V_temp[i,j]=Q_new_04[2]/(Q_new_04[0])
                    else:
                        R_temp[i,j]=0.0
                        U_temp[i,j]=0.0
                        V_temp[i,j]=0.0
            R=R_temp
            U=U_temp
            V=V_temp

                    
        if mode==2: #StandardDiff: Vd and Rd both used in the driving force 
            # For our paper Fluid-Based Analysis of Crowd Movements
            R_temp=np.zeros((Nx+2,Ny+2))
            U_temp=np.zeros((Nx+2,Ny+2))
            V_temp=np.zeros((Nx+2,Ny+2))
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                    if R[i,j]<1.0e-10:
                        continue
                        print(str(t),str(i),str(j))
                    # The problem exist in D_t is not small enough
                    Utmp= U[i,j]+D_t*(-U[i,j]*(U[i+1,j]-U[i-1,j])/2/D_x-V[i,j]*(U[i,j+1]-U[i,j-1])/2/D_y)
                    Vtmp= V[i,j]+D_t*(-U[i,j]*(V[i+1,j]-V[i-1,j])/2/D_x-V[i,j]*(V[i,j+1]-V[i,j-1])/2/D_y)
                    Rtmp= R[i,j]-D_t*(R[i+1,j]*U[i+1,j]-R[i-1,j]*U[i-1,j])/2/D_x-D_t*(R[i,j+1]*V[i,j+1]-R[i,j-1]*V[i,j-1])/2/D_y
                    DrvFx= +D_t*k1*(Ud[i,j]-U[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i+1,j]-R[i-1,j])/2/D_x
                    DrvFy= +D_t*k1*(Vd[i,j]-V[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i,j+1]-R[i,j-1])/2/D_y
                    U_temp[i,j]=Utmp+DrvFx
                    V_temp[i,j]=Vtmp+DrvFy
                    R_temp[i,j]=Rtmp
                    if debug:
                        f.write(str(R[i,j]))
            R=R_temp
            U=U_temp
            V=V_temp


        if mode==3: #LWR Model:
            R_temp=np.zeros((Nx+2,Ny+2))
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        U[i,j]=0.0
                        V[i,j]=0.0
                        continue
                    speed = vf*(1-R[i,j]/Rm)
                    temp = normalize(np.array([Ud[i,j], Vd[i,j]]))
                    U[i,j]=speed*temp[0]
                    V[i,j]=speed*temp[1]
                    
                    #if R[i,j]<1.0e-10:
                    #    continue
                    #    print(str(t),str(i),str(j))
            
            # No need to use non-slip boundary condition
            #U=U*UBLD
            #V=V*VBLD
            #f.write('Time:'+str(t))
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue                        
                    #Utmp= U[i,j]+D_t*(-U[i,j]*(U[i+1,j]-U[i-1,j])/2/D_x-V[i,j]*(U[i,j+1]-U[i,j-1])/2/D_y)
                    #Vtmp= V[i,j]+D_t*(-U[i,j]*(V[i+1,j]-V[i-1,j])/2/D_x-V[i,j]*(V[i,j+1]-V[i,j-1])/2/D_y)
                    else:
                        if BLD[i-1,j]==0.0 or BLD[i+1,j]==0.0:
                            if BLD[i-1,j]==0.0 and BLD[i+1,j]!=0.0:
                                Qx=(R[i+1,j]*U[i+1,j]-R[i,j]*U[i,j])/D_x
                            if BLD[i-1,j]!=0.0 and BLD[i+1,j]==0.0:
                                Qx=(R[i,j]*U[i,j]-R[i-1,j]*U[i-1,j])/D_x
                            if BLD[i-1,j]==0.0 and BLD[i+1,j]==0.0:
                                Qx=0.0
                        else:
                            Qx=(R[i+1,j]*U[i+1,j]-R[i-1,j]*U[i-1,j])/2/D_x
                            
                        if BLD[i,j-1]==0.0 or BLD[i,j+1]==0.0:
                            if BLD[i,j-1]==0.0 and BLD[i,j+1]!=0.0:
                                Qy=(R[i,j+1]*V[i,j+1]-R[i,j]*V[i,j])/D_y
                            if BLD[i,j-1]!=0.0 and BLD[i,j+1]==0.0:
                                Qy=(R[i,j]*V[i,j]-R[i,j-1]*V[i,j-1])/D_y
                            if BLD[i,j-1]==0.0 and BLD[i,j+1]==0.0:
                                Qy=0.0
                        else:
                            Qy=(R[i,j+1]*V[i,j+1]-R[i,j-1]*V[i,j-1])/2/D_y
                    R_temp[i,j]= R[i,j]-D_t*Qx-D_t*Qy
                    #DrvFx= +D_t*k1*(Ud[i,j]-U[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i+1,j]-R[i-1,j])/2/D_x
                    #DrvFy= +D_t*k1*(Vd[i,j]-V[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i,j+1]-R[i,j-1])/2/D_y
                    #U[i,j]=Utmp+DrvFx
                    #V[i,j]=Vtmp+DrvFy
                    
                    #Rtmp= R[i,j]-D_t*Qx-D_t*Qy
                    #R[i,j]=Rtmp
                    if debug:
                        f.write(str(R[i,j]))
            #R=R*exitpt
            R=R_temp*exitpt
            

        if mode==6: #LWR Model:
            #R_temp=R0
            R_temp=np.zeros((Nx+2,Ny+2))
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                    speed = vf*(1-R[i,j]/Rm)
                    temp = normalize(np.array([Ud[i,j], Vd[i,j]]))
                    U[i,j]=speed*temp[0]
                    V[i,j]=speed*temp[1]
                    
                    #if R[i,j]<1.0e-10:
                    #    continue
                    #    print(str(t),str(i),str(j))

            #U=U*UBLD
            #V=V*VBLD
            
            QL=np.zeros((Nx+2,Ny+2))
            QR=np.zeros((Nx+2,Ny+2))
            QU=np.zeros((Nx+2,Ny+2))
            QD=np.zeros((Nx+2,Ny+2))
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                        
                    if R[i,j]<=0.0:
                        QL[i,j]=0.0
                        QR[i,j]=0.0
                        QU[i,j]=0.0
                        QD[i,j]=0.0
                    else:
                        if U[i,j]>0:
                            QL[i,j]=0.0
                            QR[i,j]=R[i,j]/D_x*U[i,j]*D_t
                        else:
                            QL[i,j]=-R[i,j]/D_x*U[i,j]*D_t 
                            QR[i,j]=0.0                           
                        if V[i,j]>0:
                            QD[i,j]=0.0
                            QU[i,j]=R[i,j]/D_y*V[i,j]*D_t
                        else:
                            QD[i,j]=-R[i,j]/D_y*V[i,j]*D_t 
                            QU[i,j]=0.0   
                        
                    #Utmp= U[i,j]+D_t*(-U[i,j]*(U[i+1,j]-U[i-1,j])/2/D_x-V[i,j]*(U[i,j+1]-U[i,j-1])/2/D_y)
                    #Vtmp= V[i,j]+D_t*(-U[i,j]*(V[i+1,j]-V[i-1,j])/2/D_x-V[i,j]*(V[i,j+1]-V[i,j-1])/2/D_y)
                    ###R_temp[i,j]= R[i,j]-D_t*(R[i+1,j]*U[i+1,j]-R[i-1,j]*U[i-1,j])/2/D_x-D_t*(R[i,j+1]*V[i,j+1]-R[i,j-1]*V[i,j-1])/2/D_y
                    #DrvFx= +D_t*k1*(Ud[i,j]-U[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i+1,j]-R[i-1,j])/2/D_x
                    #DrvFy= +D_t*k1*(Vd[i,j]-V[i,j])+D_t*k2*(Rd[i,j]-R[i,j])*(R[i,j+1]-R[i,j-1])/2/D_y
                    #U[i,j]=Utmp+DrvFx
                    #V[i,j]=Vtmp+DrvFy
                    #R[i,j]=Rtmp
                    if debug:
                        f.write(str(R[i,j]))
            
            for i in np.arange(1,Nx+1):
                for j in np.arange(1,Ny+1):
                    if BLD[i,j]==0.0:
                        continue
                    R_temp[i,j]= R[i,j]-QL[i,j]-QR[i,j]-QU[i,j]-QD[i,j]+QR[i-1,j]+QL[i+1,j]+QD[i,j+1]+QU[i,j-1]
            R=R_temp

    f.close()
    return Rt, Ut, Vt

'''
                    
    if saveData:
        np.save("Rt.npy",Rt)
        np.save("Ut.npy",Ut)
        np.save("Vt.npy",Vt)
        
    if showPlot:
        #Plotting the 2D surface
        dim=np.shape(U)
        print(dim)
        x_points=dim[0]
        y_points=dim[1]
        xDim=np.linspace(0, (x_points-1)*D_x, x_points)
        yDim=np.linspace(0, (y_points-1)*D_y, y_points)
        print(xDim)
        print(yDim)

        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        X,Y = np.meshgrid(xDim,yDim)
        surf = ax.plot_surface(X, Y, U[:], cmap=cm.coolwarm)
        fig.suptitle("Solution of u ")
        plt.show()

        surf = ax.plot_surface(X, Y, V[:], cmap=cm.coolwarm)
        fig.suptitle("Solution of v ")
        plt.show()

        surf = ax.plot_surface(X, Y, Rt[:,:,1], cmap=cm.coolwarm)
        fig.suptitle("Initial rou ")
        plt.show()

        surf = ax.plot_surface(X, Y, Rt[:,:,int(Nt/2)], cmap=cm.coolwarm)
        fig.suptitle("Halftime rou ")
        plt.show()

        surf = ax.plot_surface(X, Y, Rt[:,:,Nt-1], cmap=cm.coolwarm)
        fig.suptitle("Solution of rou ")
        plt.show()
'''


	
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
    
    
