#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 12:43:07 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing numpy module
import numpy

# importing astropy module
import astropy.units
import astropy.time
import astropy.coordinates

# importing astroplan module
import astroplan
import astroplan.plots

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# units
unit_m    = astropy.units.m
unit_rad  = astropy.units.rad
unit_deg  = astropy.units.deg
unit_hour = astropy.units.hour

# constructing parser object
desc   = "making an airmass plot"
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
parser.add_argument ('-o', '--output', default='airmass.png', \
                     help='output file name (EPS, PDF, PNG, or PS file)')
parser.add_argument ('target', nargs='+', default='Vega', \
                     help='names of targets')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
site_lon     = args.longitude
site_lat     = args.latitude
site_alt     = args.altitude * unit_m
datetime_str = args.datetime
file_output  = args.output
list_target  = args.target

# making pathlib object
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing message
    print ("ERROR: output file '%s' exists." % file_output)
    # exit
    sys.exit ()
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("ERROR: output file must be either EPS, PDF, PNG, or PS.")
    # exit
    sys.exit ()

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
datetime = datetime + numpy.linspace (-8, +8, 100) * unit_hour

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# plotting
box = ax.get_position ()
ax.set_position ([box.x0, box.y0, box.width * 0.83, box.height])

# processing each target
for i in range ( len (list_target) ):
    # object
    target = list_target[i]
    obj = astroplan.FixedTarget.from_name (target)
    if (i == len (list_target) - 1):
        astroplan.plots.plot_airmass (obj, observer, datetime, ax=ax, \
                                      brightness_shading=True, max_airmass=2.5)
    else:
        astroplan.plots.plot_airmass (obj, observer, datetime, ax=ax)

# plotting
ax.grid ()
ax.legend (bbox_to_anchor=(1.05, 1.00), loc='upper left', shadow=True)

# saving the plot into a file
fig.savefig (file_output, bbox_inches="tight", dpi=225)
