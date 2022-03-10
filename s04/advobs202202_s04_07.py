#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 16:04:14 (CST) daisuke>
#

# importing Numpy module
import numpy
import numpy.random

#
# parameters
#

# numbers of elements in X-axis, Y-axis, and Z-axis
n_x   = 256
n_y   = 256
n_z   = 100

# mean and stddev for random number generation
mean  = 50.0
sigma = 10.0

# creating a data cube from a set of 2-dim. arrays
for i in range (n_z):
    # creating 2-dim. array
    tmp = numpy.random.normal (mean, sigma, (n_x, n_y) )
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
print ("shape of array \"cube\"     =", cube.shape)

# combining 2-dim. arrays using simple average
combined = numpy.mean (cube, axis=0)

# printing information of "combined"
print ("shape of array \"combined\" =", combined.shape)

# printing "combined"
print ("array \"combined\":")
print (combined)
