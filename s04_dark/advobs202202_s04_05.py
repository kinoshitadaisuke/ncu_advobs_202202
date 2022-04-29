#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 14:59:38 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating Numpy arrays
a = numpy.array ([ [10.0, 11.0, 12.0], \
                   [13.0, 14.0, 15.0], \
                   [16.0, 17.0, 18.0] ], \
                 dtype='float64')
b = numpy.array ([ [1.0, 2.0, 3.0], \
                   [4.0, 5.0, 6.0], \
                   [7.0, 8.0, 9.0] ], \
                 dtype='float64')
c = numpy.array ([ [1.0, 1.1, 0.9], \
                   [1.2, 0.8, 1.3], \
                   [0.7, 1.4, 0.6] ], \
                 dtype='float64')

# arithmetic operations
d = a - b
e = a / c

# printing Numpy arrays
print ("a:")
print (a)
print ("b:")
print (b)
print ("c:")
print (c)
print ("d = a - b:")
print (d)
print ("e = a / c:")
print (e)
