#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/18 01:29:56 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# making a numpy array
a_data = numpy.array ([10.0, 10.1, 9.9, 10.2, 9.8, 10.3, 9.7, 100.0])

# printing a_data
print ("a_data =", a_data)

# making a mask
#  0 ==> not masked
#  1 ==> masked
a_mask = numpy.array ([0, 0, 0, 0, 0, 0, 0, 1])

# printing a_mask
print ("a_mask =", a_mask)

# making a masked array
a_maskedarray = numpy.ma.array (a_data, mask=a_mask)

# printing a_maskedarray
print ("a_maskedarray =", a_maskedarray)

# calculating average
average_nomask = numpy.average (a_data)
average_mask   = numpy.ma.average (a_maskedarray)

# printing average
print ("average_nomask =", average_nomask)
print ("average_mask   =", average_mask)
