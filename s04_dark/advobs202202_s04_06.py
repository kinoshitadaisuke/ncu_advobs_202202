#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 15:04:38 (CST) daisuke>
#

# importing Numpy module
import numpy
import numpy.random

#
# parameters
#

# number of elements in X-axis and Y-axis
n_x   = 5
n_y   = 5

# mean and stddev for random number generation
mean  = 50.0
sigma = 10.0

# creating Numpy arrays
a = numpy.random.normal (mean, sigma, (n_x, n_y))
b = numpy.random.normal (mean, sigma, (n_x, n_y))
c = numpy.random.normal (mean, sigma, (n_x, n_y))
d = numpy.random.normal (mean, sigma, (n_x, n_y))
e = numpy.random.normal (mean, sigma, (n_x, n_y))

# printing information of Numpy arrays
print ("shape of a =", a.shape)
print ("shape of b =", b.shape)
print ("shape of c =", c.shape)
print ("shape of d =", d.shape)
print ("shape of e =", e.shape)

# concatenating arrays
cube = numpy.concatenate ( ([a], [b]), axis=0 )

# printing information of Numpy array "cube"
print ("shape of cube =", cube.shape)

# concatenating one more array
cube = numpy.concatenate ( (cube, [c]), axis=0 )

# printing information of Numpy array "cube"
print ("shape of cube =", cube.shape)

# printing cube
print ("cube =")
print (cube)

# concatenating 5 arrays
cube2 = numpy.concatenate ( ([a], [b], [c], [d], [e]), axis=0 )

# printing information of Numpy array "cube"
print ("shape of cube2 =", cube2.shape)

# printing cube2
print ("cube2 =")
print (cube2)
