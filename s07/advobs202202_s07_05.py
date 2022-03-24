#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:24:35 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# creating a masked array
data = numpy.array ([ [1, 2, 3], \
                      [4, 5, 6], \
                      [7, 8, 9] ])
mask = numpy.array ([ [False, False, False], \
                      [False, False, True], \
                      [True, False, False] ])
masked_data = numpy.ma.array (data, mask=mask)

# printing masked array
print ("data:")
print (data)

# printing masked array
print ("mask:")
print (mask)

# printing masked array
print ("masked_data:")
print (masked_data)
