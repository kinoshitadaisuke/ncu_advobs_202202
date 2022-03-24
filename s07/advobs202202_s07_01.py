#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:08:42 (CST) daisuke>
#

# importing numpy module
import numpy

# creating a 2-dim. numpy array
a = numpy.array ([ [100.0, 100.5, 99.0], \
                   [101.0, 99.5, 101.5], \
                   [98.5, 102.0, 99.9] ])

# printing numpy array "a"
print ("a")
print (a)

# creating one more numpy array
b = numpy.array ( [ [50.0, 49.5, 50.5], \
                    [49.0, 51.0, 48.5], \
                    [51.5, 48.0, 49.9] ])

# printing numpy array "b"
print ("b")
print (b)

# calculation
c = a - b

# printing numpy array "c"
print ("c = a - b")
print (c)
