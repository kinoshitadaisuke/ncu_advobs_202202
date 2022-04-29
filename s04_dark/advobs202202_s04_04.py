#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 14:55:46 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating a Numpy array
b = numpy.array ([
    [1.2, 3.4, 5.6],
    [7.8, 9.0, 12.3],
    [1.0, 2.0, 3.0],
], dtype='float64')

# printing Numpy array
print (b)

# printing Numpy array information
print ("Information of Numpy array:")
print ("  object type        = %s" % type (b) )
print ("  dimensions of data = %s" % b.ndim)
print ("  shape of data      = %s" % str (b.shape) )
print ("  number of elements = %s" % b.size)
print ("  data type          = %s" % b.dtype)
