#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:11:57 (CST) daisuke>
#

# importing numpy module
import numpy

# creating a numpy array
data = numpy.array ([ 100.0, 99.5, 100.5, 99.0, 101.0, \
                      98.5, 101.5, 98.0, 102.0, 200.0 ])

# creating a numpy array for error
error = numpy.array ([ 1.0, 1.0, 1.0, 1.0, 1.0, \
                       1.0, 1.0, 1.0, 1.0, 100.0 ])

# calculation of a mean
mean = numpy.mean (data)

# printing data and errors
print ("data  =", data)
print ("error =", error)

# printing mean
print ("mean =", mean)

# the other way to calculate a mean
average = numpy.average (data)

# printing mean
print ("average =", average)

# weighted average
weighted_average = numpy.average (data, weights=1.0/error)

# printing weighted average
print ("weighted average =", weighted_average)
