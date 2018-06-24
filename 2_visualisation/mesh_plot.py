# import tools for 3D axes
from matplotlib import pyplot as plt   
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm 
import numpy as np 

# create a grid
xg = np.linspace(0,1,31)              # evenly spaced grid points
yg = np.linspace(0,1,31)
ymin,ymax = [0.15,0.85]               # create a smaller subgrid in the y-dir for coloring
i1 = np.argmin(abs(yg-ymin))
i2 = np.argmin(abs(yg-ymax))
yg2 = yg[i1:i2+1]                     # subsample y coords
[X,Y] = np.meshgrid(xg,yg)            # create the two mesh grids
[X2,Y2] = np.meshgrid(xg,yg2)

# create a custom surface
    # parameters
xm = np.mean(xg)*0.8
ym = np.mean(yg)*1.2
sx = 0.02*3.
sy = 0.04*3.
    # function defining the surface in terms of x, y and parameters
def r(X,Y): 
    return (5-np.exp(-((X-xm)**2/sx+(Y-ym)**2/sy)))*(1-(X/4)**2)*(1+(Y/4)**2)

# create a figure with a 3D projection
fig = plt.figure(figsize=[15,8])
ax = fig.add_subplot(111, projection='3d')

# plot the function as a wireframe over the large grid
ax.plot_wireframe(X, Y, r(X,Y), lw = 0.5, color = 'k')
    # shade part of the wireframe according to the function value
CS = ax.plot_surface(X2, Y2, r(X2,Y2), rstride=1, cstride=1,cmap=cm.Oranges, lw = 0.5)
plt.colorbar(CS, ax=ax)

# display the interactive figure to the screen
plt.show()