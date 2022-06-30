#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 11:41:21 (CST) daisuke>
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
desc   = "finding length of observable time on a night"
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

# end of twilight
twilight_civil_end        = observer.twilight_evening_civil \
    (datetime, which="nearest")
twilight_nautical_end     = observer.twilight_evening_nautical \
    (datetime, which="nearest")
twilight_astronomical_end = observer.twilight_evening_astronomical \
    (datetime, which="nearest")

# start of twilight
twilight_civil_start        = observer.twilight_morning_civil \
    (datetime, which="nearest")
twilight_nautical_start     = observer.twilight_morning_nautical \
    (datetime, which="nearest")
twilight_astronomical_start = observer.twilight_morning_astronomical \
    (datetime, which="nearest")

# printing results
print ("end of evening twilight nearest to %s" % datetime)
print ("  civil twilight:        %s" % twilight_civil_end.isot)
print ("  nautical twilight:     %s" % twilight_nautical_end.isot)
print ("  astronomical twilight: %s" % twilight_astronomical_end.isot)
print ("start of morning twilight nearest to %s" % datetime)
print ("  civil twilight:        %s" % twilight_civil_start.isot)
print ("  nautical twilight:     %s" % twilight_nautical_start.isot)
print ("  astronomical twilight: %s" % twilight_astronomical_start.isot)

# calculating observable time
obs_time = twilight_astronomical_start.mjd - twilight_astronomical_end.mjd

print ("length of observable time on %s" % datetime)
print ("  observable time = %6.4f [day]" % obs_time)
print ("                  = %5.2f [hour]" % (obs_time * 24.0) )
