#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/25 00:34:08 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy
import astropy.stats

# raw data
raw = numpy.array ([100.0, 100.1, 100.2, 100.3, 100.4, \
                    100.5, 100.6, 100.7, 100.8, 100.9, \
                    500.0, 1000.0, 3000.0])

# printing raw data
print ("raw data:")
print (raw)

# statistical information of raw data
print ("mean   =", numpy.mean (raw) )
print ("median =", numpy.median (raw) )
print ("stddev =", numpy.std (raw) )

# sigma clipping with masked=False
clipped = astropy.stats.sigma_clip (raw, sigma=3.0, maxiters=5, \
                                    cenfunc='median', masked=False)

print ("Is \"clipped\" masked? %s" % numpy.ma.is_masked (clipped) )
print ("clipped data:")
print (clipped)

# sigma clipping with masked=True
mdata = astropy.stats.sigma_clip (raw, sigma=3.0, maxiters=5, \
                                  cenfunc='median', masked=True)

print ("Is \"mdata\" masked? %s" % numpy.ma.is_masked (mdata) )
print ("masked data:")
print (mdata)
