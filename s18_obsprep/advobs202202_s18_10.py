#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 11:54:29 (CST) daisuke>
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
desc   = "finding position of the Moon in equatorial, ecliptic, and altaz"
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

# using DE430
astropy.coordinates.solar_system_ephemeris.set ('de430')

# position of the Moon
moon = astropy.coordinates.get_body ('moon', datetime, location)
(moon_ra, moon_dec) = moon.to_string ('hmsdms').split ()

# conversion from equatorial into ecliptic
moon_ecliptic = moon.transform_to \
    (astropy.coordinates.GeocentricMeanEcliptic (obstime=datetime) )
moon_lambda = moon_ecliptic.lon
moon_beta   = moon_ecliptic.lat

# conversion from equatorial into horizontal
moon_altaz = moon.transform_to \
    (astropy.coordinates.AltAz (obstime=datetime, location=location) )
moon_alt = moon_altaz.alt
moon_az  = moon_altaz.az

# printing position of the Moon
print ("Moon:")
print ("  Equatorial: RA=%s, Dec=%s" % (moon_ra, moon_dec) )
print ("  Ecliptic:   lambda=%s, beta=%s" % (moon_lambda, moon_beta) )
print ("  AltAz:      Az=%s, Alt=%s" % (moon_az, moon_alt) )
