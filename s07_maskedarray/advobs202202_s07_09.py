#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:30:27 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# creating a numpy arrays
data = numpy.array ([100.0, 100.1, 99.9, 100.2, 99.8, \
                     100.3, 99.7, 100.4, 99.6, 300.0])
mask = numpy.array ([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

# creating a masked array
mdata = numpy.ma.array (data, mask=mask)

# printing data
print ("original data:", data)
print ("masked data:  ", mdata)

# calculation of average
average_data  = numpy.average (data)
average_mdata = numpy.ma.average (mdata)

# printing average
print ("average of original data:", average_data)
print ("average of masked data:  ", average_mdata)

# calculation of standard deviation
stddev_data  = numpy.std (data)
stddev_mdata = numpy.ma.std (mdata)

# printing stddev
print ("stddev of original data:", stddev_data)
print ("stddev of masked data:  ", stddev_mdata)
