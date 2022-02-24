#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 14:02:01 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.time

# time "t1"
t1 = astropy.time.Time ('2022-02-25T12:00:00.000', format='isot', scale='utc')

# printing the time "t1"
print ("t1 =", t1)

# JD
t1_jd = t1.jd

# printing JD corresponding to the time "t1"
print ("t1 in JD =", t1_jd)

# time "t2"
t2 = astropy.time.Time ('2000-01-01T12:00:00.000', format='isot', scale='utc')

# printing the time "t2"
print ("t2 =", t2)

# calculating the time difference between "t1" and "t2"
dt = t1 - t2

# printing "dt"
print ("dt = t1 - t2 = ", dt, "day =", dt.sec, "sec")
