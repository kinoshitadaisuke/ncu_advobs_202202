#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:26:03 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# creating a numpy array
data = numpy.array ([ 100.0, 99.5, 100.5, 99.0, 101.0, \
                      98.5, 101.5, 98.0, 102.0, 200.0 ])

# creating a numpy array for error
error = numpy.array ([ 1.0, 1.0, 1.0, 1.0, 1.0, \
                       1.0, 1.0, 1.0, 1.0, 100.0 ])

# initialisation of a numpy array for a mask
mask = numpy.array ([])

# weighted average
weighted_average = numpy.average (data, weights=1.0/error)

# printing weighted average
print ("weighted average =", weighted_average)

# standard deviation
stddev = numpy.std (data)

# printing standard deviation
print ("stddev =", stddev)

# examining data
for datum in data:
    if ( (datum < weighted_average + 3.0 * stddev) \
         and (datum > weighted_average - 3.0 * stddev) ):
        print ("%5.1f: within average +/- 3.0 * sigma" % datum)
        # appending a value to the array "mask"
        mask = numpy.append (mask, 0)
    else:
        print ("%5.1f: outside of average +/- 3.0 * sigma" % datum)
        # appending a value to the array "mask"
        mask = numpy.append (mask, 1)

# printing the array "data"
print ("data:", data)
        
# printing the array "mask"
print ("mask:", mask)

# creating a masked array
masked_data = numpy.ma.MaskedArray (data, mask=mask)

# printing masked array
print ("masked_data =", masked_data)
print ("masked_data.data =", masked_data.data)
print ("masked_data.mask =", masked_data.mask)
