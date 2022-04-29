#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 22:33:23 (CST) daisuke>
#

# importing numpy module
import numpy

# sample data set 1
data1 = numpy.array ([10.0, 10.0, 9.0, 9.0, 11.0, 11.0])

# calculation of simple mean
data1_mean = numpy.mean (data1)

# printing result
print ("data1         =", data1)
print ("data1_mean    = %f" % data1_mean)

# sample data set 2 with NaN value
data2 = numpy.array ([10.0, 10.0, 9.0, 9.0, 11.0, 11.0, numpy.nan])

# calculation of simple mean
data2_mean = numpy.mean (data2)

# printing result
print ("data2         =", data2)
print ("data2_mean    = %f" % data2_mean)

# calculation of simple mean using numpy.nanmean
data2_nanmean = numpy.nanmean (data2)

# printing result
print ("data2_nanmean = %f" % data2_nanmean)
