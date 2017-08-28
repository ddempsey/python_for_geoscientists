# imports
from matplotlib import pyplot as plt
import numpy as np

N = 100                       # number of data points to create
obs = np.random.randn(N)      # generate normally distributed data
mean, std = [2.5, 0.3]        # mean and standard deviation to transform the data
obs = obs*std + mean          # transform the data
print(obs)

# the basics
print('min =', np.min(obs))
print('max =', np.max(obs))
print('mean =', np.mean(obs))
print('std =', np.std(obs))

# more fancy
print('LQ =', np.percentile(obs,25))
print('median =', np.percentile(obs,50))
print('UQ =', np.percentile(obs,75))
print('count = ', len(obs))
print('sum =', np.sum(obs))

# create the "bin" as a vector of evenly spaced points
Nbins = 8                                                         # alternatively, Nbins = int(np.sqrt(N)/2)
bin_edges = np.linspace(np.min(obs), np.max(obs), Nbins+1)        # create the bins, a vector of bin edges
h,e = np.histogram(obs, bin_edges)                                # sort the data into their bins
print(e)                                                          # bin edges
print(h)                                                          # bin heights

# create the histogram
f,ax = plt.subplots(1,1)
ax.bar(left = e[:-1], height = h, width = e[1]-e[0], color = [0, 0.5, 0], edgecolor = 'k')
# Above, I have specified the bar 'color' as an [r g b] vector - this gives more flexibility in the type of colors that can
# be used. Experiment with changing the three values (make sure your values are between 0 and 1 though!)

# save the figure to a file
plt.savefig('histogram.png', dpi = 300)      # dpi is the resolution, 300 is good for many applications