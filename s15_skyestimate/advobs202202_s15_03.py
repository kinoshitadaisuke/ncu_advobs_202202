#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/19 21:02:23 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy
import numpy.random

# importing astropy module
import astropy.table

# importing photutils module
import photutils.datasets

# constructing parser object
desc   = 'generating a synthetic image with artificial stars and galaxies'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-x', '--size-x', type=int, default=2048, \
                     help='image size in X-axis (default: 2048)')
parser.add_argument ('-y', '--size-y', type=int, default=2048, \
                     help='image size in Y-axis (default: 2048)')
parser.add_argument ('-n', '--nstars', type=int, default=100, \
                     help='number of stars to generate (default: 100)')
parser.add_argument ('-g', '--ngalaxies', type=int, default=10, \
                     help='number of galaxies to generate (default: 10)')
parser.add_argument ('-f', '--flux-min', type=float, default=1000.0, \
                     help='minimum flux of stars (default: 1000)')
parser.add_argument ('-p', '--fwhm-psf', type=float, default=3.5, \
                     help='FWHM of PSF in pixel (default: 3.5)')
parser.add_argument ('-d', '--fwhm-stddev', type=float, default=0.1, \
                     help='stddev of FWHM distribution in pixel (default: 0.1)')
parser.add_argument ('-q', '--fwhm-psf-gal', type=float, default=8.0, \
                     help='FWHM of galaxy PSF in pixel (default: 8)')
parser.add_argument ('-r', '--fwhm-psf-gal-stddev', type=float, default=4.0, \
                     help='stddev of FWHM of galaxy PSF in pixel (default: 4)')
parser.add_argument ('-s', '--sky', type=float, default=1000.0, \
                     help='sky background level in ADU (default: 1000)')
parser.add_argument ('-e', '--sky-stddev', type=float, default=30.0, \
                     help='stddev of sky background in ADU (default: 30)')
parser.add_argument ('-o', '--output-file', default='', \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# image size
image_size_x = args.size_x
image_size_y = args.size_y
image_shape  = (image_size_x, image_size_y)

# number of stars and galaxies to generate
nstars = args.nstars
ngals  = args.ngalaxies

# flux of faintest stars
flux_min = args.flux_min

# FWHM of PSF
fwhm_x            = args.fwhm_psf
fwhm_y            = args.fwhm_psf
fwhm_stddev_x     = args.fwhm_stddev
fwhm_stddev_y     = args.fwhm_stddev
fwhm_gal_x        = args.fwhm_psf_gal
fwhm_gal_y        = args.fwhm_psf_gal
fwhm_gal_stddev_x = args.fwhm_psf_gal_stddev
fwhm_gal_stddev_y = args.fwhm_psf_gal_stddev

# sky background level and stddev
sky_mean   = args.sky
sky_stddev = args.sky_stddev

# output file name
file_output = args.output_file

# making pathlib object
path_output = pathlib.Path (file_output)

# check of output file name
if not (path_output.suffix == '.fits'):
    # printing message
    print ("ERROR: Output file must be a FITS file!")
    # exit
    sys.exit ()

# existence check of output file
if (path_output.exists ()):
    # printing message
    print ("ERROR: Output file '%s' exists!" % (file_output) )
    # exit
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()

# command name
command = sys.argv[0]

# generating a new astropy table
table_stars = astropy.table.Table ()
table_gals  = astropy.table.Table ()

# generating random numbers for stars
rng        = numpy.random.default_rng ()
position_x = rng.uniform (0, image_size_x, nstars)
position_y = rng.uniform (0, image_size_y, nstars)
theta_deg  = rng.uniform (0, 360, nstars)
psf_x      = rng.normal (loc=fwhm_x, scale=fwhm_stddev_x, size=nstars)
psf_y      = rng.normal (loc=fwhm_y, scale=fwhm_stddev_y, size=nstars)
powerlaw   = rng.power (1.5, size=nstars)
flux       = flux_min / powerlaw

# generating random numbers for galaxies
position_gal_x = rng.normal (loc=image_size_x / 2.0, scale=300, size=ngals)
position_gal_y = rng.normal (loc=image_size_y / 2.0, scale=300, size=ngals)
theta_gal_deg  = rng.uniform (0, 360, ngals)
psf_gal_x      = rng.normal (loc=fwhm_gal_x, scale=fwhm_gal_stddev_x, size=ngals)
psf_gal_y      = rng.normal (loc=fwhm_gal_y, scale=fwhm_gal_stddev_y, size=ngals)
powerlaw_gal   = rng.power (2.0, size=ngals)
flux_gal       = flux_min * 3 / powerlaw_gal

# conversion from degree to radian
theta_rad     = numpy.radians (theta_deg)
theta_gal_rad = numpy.radians (theta_gal_deg)

# adding data to the table of stars
table_stars['amplitude'] = flux
table_stars['x_mean']    = position_x
table_stars['y_mean']    = position_y
table_stars['x_stddev']  = psf_x
table_stars['y_stddev']  = psf_y
table_stars['theta']     = theta_rad

# adding data to the table of galaxies
table_gals['amplitude'] = flux_gal
table_gals['x_mean']    = position_gal_x
table_gals['y_mean']    = position_gal_y
table_gals['x_stddev']  = psf_gal_x
table_gals['y_stddev']  = psf_gal_y
table_gals['theta']     = theta_gal_rad

# generating stars
image_stars \
    = photutils.datasets.make_gaussian_sources_image (image_shape, table_stars)

# generating galaxies
image_gals \
    = photutils.datasets.make_gaussian_sources_image (image_shape, table_gals)

# generating sky background
image_sky \
    = photutils.datasets.make_noise_image (image_shape, \
                                           distribution='gaussian', \
                                           mean=sky_mean, stddev=sky_stddev)

# generating synthetic image
image = image_stars + image_gals + image_sky

# making WCS
wcs = photutils.datasets.make_wcs (image_shape)

# making FITS header
header = wcs.to_header ()

# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "image size = %d x %d" % (image_size_x, image_size_y)
header['comment'] = "number of stars = %d" % (nstars)
header['comment'] = "flux_min = %f" % (flux_min)
header['comment'] = "fwhm_x = %f" % (fwhm_x)
header['comment'] = "fwhm_y = %f" % (fwhm_y)
header['comment'] = "fwhm_stddev_x = %f" % (fwhm_stddev_x)
header['comment'] = "fwhm_stddev_y = %f" % (fwhm_stddev_y)
header['comment'] = "number of galaxies = %d" % (ngals)
header['comment'] = "fwhm_gal_x = %f" % (fwhm_gal_x)
header['comment'] = "fwhm_gal_y = %f" % (fwhm_gal_y)
header['comment'] = "fwhm_gal_stddev_x = %f" % (fwhm_gal_stddev_x)
header['comment'] = "fwhm_gal_stddev_y = %f" % (fwhm_gal_stddev_y)
header['comment'] = "sky_mean = %f" % (sky_mean)
header['comment'] = "sky_stddev = %f" % (sky_stddev)
header['comment'] = "file_output = %s" % (file_output)

# writing a FITS file
astropy.io.fits.writeto (file_output, image, header=header)
