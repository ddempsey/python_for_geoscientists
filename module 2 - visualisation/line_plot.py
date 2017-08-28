# imports
from matplotlib import pyplot as plt    
import numpy as np 

# we'll add a second subplot (1 row, 2 columns) and 'unpack' the axes as 'ax1' and 'ax2'
f,(ax1,ax2) = plt.subplots(1,2)                    
f.set_size_inches(10,4)

x = np.linspace(0, 2*np.pi, 21)				# this function creates an array of 21 evenly spaced points, between 0 and 2*pi
y = np.sin(x)                               # generate some y data to plot against x

ax1.plot(x,y,'r--s', label = 'some data')                    
ax1.plot(x, 1.5*y-0.5,'g:p', label = 'transformed data')       # transform and plot the data on the first axis    

ax2.plot(2*x, -y, 'k-')       # plot a different transformation on the second axis

# let's set the labels for all axes simultaneously using a FOR loop
for ax in [ax1,ax2]:
    ax.set_xlabel('x')                                
    ax.set_ylabel('y', size = 12)            

# add a legend for the first axis 
ax1.legend(loc = 1)       
# add a text annotation in the two plots
ax1.text(0.05, 0.05, "A", ha = 'left', va = 'bottom', transform=ax1.transAxes, size = 15)
ax2.text(0.05, 0.05, "B", ha = 'left', va = 'bottom', transform=ax2.transAxes, size = 15)

# save the figure to a file
plt.savefig('line_plot.png', dpi = 300)      # dpi is the resolution, 300 is good for many applications