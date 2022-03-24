#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:28:14 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# masked array
a = numpy.ma.array ([30, 31, 32, 33, 34, 35], mask=[0, 0, 0, 0, 0, 1])

# numpy array
b = numpy.array ([12, 13, 14, 15, 16, 17])

# calculation
c = a - b

# result of calculation
print ("a =", a)
print ("b =", b)
print ("c = a - b =", c)
