# imports
from matplotlib import pyplot as plt
import numpy as np

# function to create frames
def plot_frame(i,a):
    ''' Plots a single frame of the fault rupture, at position a.
    
        i = frame number
        a = position of rupture front
        
        Stress changes are computed according to linear elastic fracture mechanics.
        s = s0 for x>>a         (far field stress)
        s = s0-ds for x<a       (stress drop inside rupture)
        s ~ K/sqrt(x) for x>a   (decaying stresses with singularity at crack tip)
    '''
    f,ax = plt.subplots(1,1)
    x = np.linspace(0,10.,1001)
    
    # calculate the stress field
    s0 = 25.                      # pre-earthquake stress
    ds = 3.                       # stress drop
    K = s0*np.sqrt(np.pi*a)       # stress intensity factor
    y = s0*np.ones(len(x))        # background stress vector
    y[np.where(x<a)] = s0-ds      # stress behind the rupture
    # stress increase in front of the rupture
    y[np.where(x>=a)] = s0+K/np.sqrt(2*np.pi*(x[np.where(x>=a)]-a)*1.e3) 
    
    # plot the stress changes
    ax.plot(x,y,'k-')                  # plot stress changes
    ax.plot([a,a], [s0-ds, 30], 'k:')  # stress singularity
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([21, 30])
    ax.set_xlabel('position along fault / km')
    ax.set_ylabel('stress / MPa')
    
    # save the frame in a separate folder and name it using the index i
    plt.savefig('all_frames/frame{:04d}.png'.format(i), dpi=300)
    plt.close(f)                   # it will be important to close all these figures when we're looping
    
# this part should be familiar!
import os
if not os.path.isdir('all_frames'):
    os.makedirs('all_frames')

# details of movie
FPS = 10           # ten frames per second, let's not be greedy
secs = 5           # total seconds
Nframes = secs*FPS  # total frames

# each frame has a different value a, lets create a vector of a values
avals = np.linspace(0.25, 3.0, Nframes)

# then loop over each avalue and create the frame
for i,a in enumerate(avals):               # enumerate is a handy function that both loops over the values in an array
    plot_frame(i,a)                        # AND gives you a corresponding index
	
# we'll use os.system - a handy command that let's us implement command line calls without returning to the command line
os.system('ffmpeg -framerate {:d} -i all_frames/frame%04d.png earthquake_movie.mp4'.format(FPS))

# tidy up the frames
from glob import glob
fls = glob('all_frames/*.png')
for fl in fls: os.remove(fl)
os.rmdir('all_frames')