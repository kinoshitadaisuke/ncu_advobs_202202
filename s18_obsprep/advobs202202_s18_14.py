#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 12:22:39 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing astropy module
import astropy.units
import astropy.time
import astropy.coordinates

# importing astroplan module
import astroplan

# units
unit_m = astropy.units.m
unit_rad = astropy.units.rad
unit_deg = astropy.units.deg

# constructing parser object
desc   = "finding rise and set time of targets at given location"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-l', '--longitude', default='+120d52m25s', \
                     help='longitude of observing site in format "+121d11m12s"')
parser.add_argument ('-b', '--latitude', default='+23d28m07s', \
                     help='latitude of observing site in format "+24d58m12s"')
parser.add_argument ('-a', '--altitude', type=float, default=2862.0, \
                     help='altitude above sea-level in metre')
parser.add_argument ('-t', '--datetime', default='2000-01-01T12:00:00.000', \
                     help='date/time in UT in "YYYY-MM-DDThh:mm:ss.sss" format')
parser.add_argument ('target', nargs='+', default='Vega', \
                     help='names of targets')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
site_lon     = args.longitude
site_lat     = args.latitude
site_alt     = args.altitude * unit_m
datetime_str = args.datetime
list_target  = args.target

# printing input parameters
print ("#")
print ("# input parameters")
print ("#")
print ("#  Location:")
print ("#   longitude =", site_lon)
print ("#   latitude  =", site_lat)
print ("#   altitude  =", site_alt)
print ("#  Date/Time:")
print ("#   date/time (UT) =", datetime_str)
print ("#  Targets:")
for target in list_target:
    print ("#   %s" % target)

# location object
location = astropy.coordinates.EarthLocation.from_geodetic \
    (site_lon, site_lat, site_alt)

# observer object
observer = astroplan.Observer (location=location, name="observer", \
                               timezone="UTC")

# time object
datetime = astropy.time.Time (datetime_str, scale='utc')

# processing each target
for target in list_target:
    # object
    obj = astroplan.FixedTarget.from_name (target)
    # rise time
    time_rise = observer.target_rise_time (datetime, obj, which="nearest")
    # set time
    time_set  = observer.target_set_time (datetime, obj, which="nearest")
    # printing results
    print ("rise and set of %s on %s:" % (target, datetime) )
    print ("  rise time: %s" % time_rise.isot)
    print ("  set time:  %s" % time_set.isot)
