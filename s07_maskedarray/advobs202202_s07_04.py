#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:19:33 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# creating a masked array
data = numpy.array ([ [1, 2, 3], \
                      [4, 5, 6], \
                      [7, 8, 9] ])
mask = numpy.array ([ [0, 0, 0], \
                      [0, 0, 1], \
                      [1, 0, 0] ])
masked_data = numpy.ma.masked_array (data, mask=mask)

# masked array?
is_masked_data = numpy.ma.is_masked (data)
print ("Is \"data\" masked? ==> %s" % is_masked_data)
is_masked_masked_data = numpy.ma.is_masked (masked_data)
print ("Is \"masked_data\" masked? ==> %s" % is_masked_masked_data)

# printing original data and masked array
print ("original data:")
print (data)
print ("mask:")
print (mask)
print ("masked_data:")
print (masked_data)
