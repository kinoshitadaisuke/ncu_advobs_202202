#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 16:19:09 (CST) daisuke>
#

# importing Numpy module
import numpy
import numpy.random

# importing Astropy module
import astropy.stats

# number of elements in X-axis, Y-axis, and Z-axis
n_x = 256
n_y = 256
n_z = 100

# mean and stddev for random number generation
mean  = 50.0
sigma = 10.0

# creating a data cube from a set of 2-dim. arrays
for i in range (n_z):
    # creating 2-dim. array
    tmp = numpy.random.normal (mean, sigma, (n_x, n_y) )

    # choosing a pixel for an outlier
    x = int ( numpy.random.uniform (0, n_x) )
    y = int ( numpy.random.uniform (0, n_y) )
    # adding an outlier of value around 10,000
    tmp[x][y] += 10000.0
    
    # concatenating 2-dim. arrays to make a data cube
    if (i == 0):
        # for the first 2-dim. array, copy it to "tmp0"
        tmp0 = tmp
    elif (i == 1):
        # for the second 2-dim. array, make a 3-dim. array "cube"
        # by concatenating "tmp0" and "tmp" using the function concatenate
        cube = numpy.concatenate ( ([tmp0], [tmp]), axis=0 )
    else:
        # for other 2-dim. arrays, concatenate "tmp"
        # to the 3-dim. array "cube"
        cube = numpy.concatenate ( (cube, [tmp]), axis=0 )

# printing information of "cube"
print ("shape of cube =", cube.shape)

# combining 2-dim. arrays using simple average
combined_simple = numpy.mean (cube, axis=0)

# combining 2-dim. arrays using sigma clipping
#   threshold = mean +/- 3.0 times of stddev
#   max number of iterations = 10
#   calculation of average = mean
combined_sigclip, median, stddev \
    = astropy.stats.sigma_clipped_stats (cube, sigma=3.0, maxiters=10, \
                                         cenfunc='mean', stdfunc='std', \
                                         axis=0)

# printing information of "combined"
print ("shape of combined =", combined_sigclip.shape)

# printing "combined"
print (combined_sigclip)

# max and min
print ("min of combined_simple:  %f" % numpy.amin (combined_simple) )
print ("max of combined_simple:  %f" % numpy.amax (combined_simple) )
print ("min of combined_sigclip: %f" % numpy.amin (combined_sigclip) )
print ("max of combined_sigclip: %f" % numpy.amax (combined_sigclip) )
