# imports
import matplotlib
from matplotlib import pyplot as plt    
import numpy as np 
from datetime import datetime
import urllib.request                       # the module we'll need
import shutil

# 1. DOWNLOAD DATA from the web
url = 'http://cdn.knmi.nl/knmi/map/page/seismologie/all_induced.csv'        # the url where the data is located (look it up!)
file_name = 'nd_eqs.txt'                                                    # name of the file to save the data into
with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file: # not super important you understand this line
    shutil.copyfileobj(response, out_file)               # pull down and save the data

# 2. LOAD THE DATA downloaded previously
data = np.genfromtxt('nd_eqs.txt', delimiter = ',', skip_header=1)

# we will pick out four columns: date (col 1), lat (col 4), lon (col 5), magnitude (col 7)
date = data[:,0]                # extract all the rows, first column
lat = data[:,3]/180.*np.pi      # same, fourth column (coverted from degrees to radians)
lon = data[:,4]/180.*np.pi      # etc
mag = data[:,6]

# convert lat-lon to approximate x-y
r = 6371                        # radius of earth (km)
lat_avg = np.mean(lat)
x = r*lon*np.cos(lat_avg)
y = r*lat

# 3. FILTER THE DATA using the 'where' function and conditions to find the data indices we're interested in 
    # (while we're at it, get rid of the events smaller than M 1)
inds = np.where((435 < x) & (x < 475) & (5900 < y) & (y < 5950) & (mag > 1.0))      # & = 'and' but when comparing arrays

# 'slice' the arrays to keep only the values satisfying the conditions above
date = date[inds]
x = x[inds]
y = y[inds]
mag = mag[inds]

# 4. CONVERT THE DATES from float -> integer -> string
t0 = datetime.strptime('19910101', '%Y%m%d')           # reference time 1 Jan 1991
times = []                                             # an empty list for storing each date as it is calculated
for each_date in date:
    # first, convert from float -> integer -> string    (converting straight to a string leaves an awkward decimal point)
    str_date = str(int(each_date))
    # interpret each datestring 
    t = datetime.strptime(str_date, '%Y%m%d')
    # take the difference between the datestring and the reference time
    dt = t - t0
    # find the total seconds and convert the date to decimal years
    times.append(dt.total_seconds()/(3600*24*365.25)+1991)

# 5. CONVERT THE MAGNITUDES to a size between 1 and 100 (largest event is a 100 point circle)
    # first, rescale magnitudes to range between 0 and 1
s = (mag - np.min(mag))/(np.max(mag) - np.min(mag))
    # second, rescale to range between 1 and 100 (this will be the size of the marker)
s = s*(100-2)+1
	
# 6. PLOTTING COMMANDS
f,ax = plt.subplots(1,1)                
f.set_size_inches(10,10)

# use the imread function to read an image file 'im' is a MxNx3 array of image data (each pixel has three components, corresponding to an RGB color) 
im = plt.imread('groningen_reservoir.png')

implot = ax.imshow(im, extent=[430, 475, 5902, 5950])     # plot the image and 'stretch' it to the given x and y limits

# then, let's plot the earthquakes over the top
coolwarm = matplotlib.cm.get_cmap('coolwarm_r')     # import a new colormap - this one is 'coolwarm', reversed it with '_r'
CS = ax.scatter(x,y,s, c= times, cmap=coolwarm)     
ax.set_aspect('equal', adjustable='box')    
plt.colorbar(CS, ax = ax)       

# save the figure to a file
plt.savefig('scatter_plot.png', dpi = 300)      # dpi is the resolution, 300 is good for many applications