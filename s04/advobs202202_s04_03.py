#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 14:54:06 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating a Numpy array
a = numpy.array ([1.2, 3.4, 5.6, 7.8, 9.0, 12.3], dtype='float64')

# printing Numpy array information
print ("Information of Numpy array:")
print ("  object type        = %s" % type (a) )
print ("  dimensions of data = %s" % a.ndim)
print ("  shape of data      = %s" % str (a.shape) )
print ("  number of elements = %s" % a.size)
print ("  data type          = %s" % a.dtype)
