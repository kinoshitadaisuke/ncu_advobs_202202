#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 11:10:57 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.units
import astropy.time
import astropy.coordinates

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# units
unit_m = astropy.units.m

# constructing parser object
desc   = "position of the Sun in (az, alt) at given location and time"
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

# time object
datetime = astropy.time.Time (datetime_str, scale='utc')

# using DE430
astropy.coordinates.solar_system_ephemeris.set ('de430')

# position of the Sun
sun = astropy.coordinates.get_body ('sun', datetime, location)
(sun_ra, sun_dec) = sun.to_string ('hmsdms').split ()

# conversion from equatorial into ecliptic
sun_ecliptic = sun.transform_to \
    (astropy.coordinates.GeocentricMeanEcliptic (obstime=datetime) )
sun_lambda = sun_ecliptic.lon
sun_beta   = sun_ecliptic.lat

# conversion from equatorial into horizontal
sun_altaz = sun.transform_to \
    (astropy.coordinates.AltAz (obstime=datetime, location=location) )
sun_alt = sun_altaz.alt
sun_az  = sun_altaz.az

# printing position of the Sun
print ("Sun:")
print ("  Equatorial: RA=%s, Dec=%s" % (sun_ra, sun_dec) )
print ("  Ecliptic:   lambda=%s, beta=%s" % (sun_lambda, sun_beta) )
print ("  AltAz:      Az=%s, Alt=%s" % (sun_az, sun_alt) )
