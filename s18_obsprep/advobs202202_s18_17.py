#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/30 13:05:32 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing astropy module
import astropy.units

# importing astroplan module
import astroplan
import astroplan.plots

# importing matplotlib module
import matplotlib.pyplot

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# units
unit_arcmin = astropy.units.arcmin

# constructing parser object
desc   = "making a finding chart"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-t', '--target', default='M1', help='target name')
parser.add_argument ('-f', '--fov', type=float, default=13.0, \
                     help='field-of-view in arcmin (default: 13 arcmin)')
parser.add_argument ('-o', '--output', default='chart.png', \
                     help='output file name (EPS, PDF, PNG, or PS file)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
target      = args.target
fov         = args.fov * unit_arcmin
file_output = args.output

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

# target
obj = astroplan.FixedTarget.from_name (target)

# image
ax, hdu = astroplan.plots.plot_finder_image (obj, fov_radius=fov)

# saving the image to file
matplotlib.pyplot.savefig (file_output)
