#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 11:34:47 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.units
import astropy.time
import astropy.coordinates

# importing astroplan module
import astroplan

# units
unit_m = astropy.units.m

# constructing parser object
desc   = "finding length of night"
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

# command-line argument analysis
args = parser.parse_args ()

# input parameters
site_lon     = args.longitude
site_lat     = args.latitude
site_alt     = args.altitude * unit_m
datetime_str = args.datetime

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

# location object
location = astropy.coordinates.EarthLocation.from_geodetic \
    (site_lon, site_lat, site_alt)

# observer object
observer = astroplan.Observer (location=location, name="observer", \
                               timezone="UTC")

# time object
datetime = astropy.time.Time (datetime_str, scale='utc')

# sunset
sunset = observer.sun_set_time (datetime, which="nearest")

# sunrise
sunrise = observer.sun_rise_time (datetime, which="nearest")

# length of night
length_night = sunrise.mjd - sunset.mjd

# printing results
print ("sunset time (UT) nearest to %s (UT)" % datetime)
print ("  JD = %s" % sunset)
print ("     = %s" % sunset.isot)
print ("sunrise time (UT) nearest to %s (UT)" % datetime)
print ("  JD = %s" % sunrise)
print ("     = %s" % sunrise.isot)
print ("length of night on %s (UT)" % datetime)
print ("  length = %6.4f [day]" % length_night)
print ("         = %5.2f [hour]" % (length_night * 24.0) )
