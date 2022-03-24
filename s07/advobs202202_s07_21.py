#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:46:36 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# data
data = numpy.array ([100.0, 99.9, 100.1, 99.8, 1500.0, \
                     100.2, 99.7, 3000.0, 100.3, 99.6, \
                     100.4, 99.5, 100.5, 0.0, 99.4, \
                     100.6, 5000.0, 99.3, 100.7, 99.2, \
                     100.8, 99.1, 300.0, 100.9, 99.0, \
                     101.0, 98.9, 101.1, 150.0, 98.8])

# printing data
print ("data:")
print (data)

# a function to carry out sigma-clipping
def sigma_clip (data, sigma, maxiters):
    # making a mask
    mask = numpy.array ([False] * len (data))
    # making a masked data
    mdata  = numpy.ma.array (data, mask=mask)
    # iterations
    for i in range (maxiters):
        # calculation of median
        median = numpy.ma.median (mdata)
        # calculation of standard deviation
        stddev = numpy.ma.std (mdata)
        # if stddev is the same as the value of previous iteration,
        # then stop the iteration
        if ( (i > 0) and (stddev == stddev_prev) ):
            break
        # higher limit
        high   = median + sigma * stddev
        # lower limit
        low    = median - sigma * stddev
        # making a new mask
        mask   = ( (mdata < low) | (mdata > high) )
        # making a new masked data
        mdata  = numpy.ma.array (mdata, mask=mask)
        # copying median and stddev for next iteration
        median_prev = median
        stddev_prev = stddev
        # printing information
        print ("%d-th iteration" % (i + 1) )
        print ("  median = %f" % median)
        print ("  stddev = %f" % stddev)
        print ("  number of rejected data = %d" \
               % ( len (mdata) - len (mdata.compressed () ) ) )
    # returning masked array
    return (mdata)

# carrying out sigma-clipping
mdata = sigma_clip (data, 3.0, 10)

# printing result
print ("mdata:")
print (mdata)
