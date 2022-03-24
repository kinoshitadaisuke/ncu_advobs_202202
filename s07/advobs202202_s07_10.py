#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:31:44 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# masked array
a = numpy.ma.array ([35, 31, 34, 32, 33, 30], mask = [0, 0, 0, 1, 0, 0])

# sorting
b = numpy.ma.sort (a)

# printing result
print ("original data:", a)
print ("sorted data:  ", b)
