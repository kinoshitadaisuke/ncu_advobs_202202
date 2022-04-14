#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/14 16:36:23 (CST) daisuke>
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

# importing astropy module
import astropy.io.fits
import astropy.table

# importing photutils module
import photutils.datasets

# constructing parser object
desc   = 'generating a synthetic image with stars'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-b', '--background', type=float, default=2500.0, \
                     help='background level (default: 2500)')
parser.add_argument ('-s', '--sigma', type=float, default=50.0, \
                     help='noise level (default: 50)')
parser.add_argument ('-n', '--nstar', type=int, default=5, \
                     help='number of stars to generate (default: 5)')
parser.add_argument ('-f1', '--flux1', type=float, default=300000.0, \
                     help='total flux of bright star (default: 300000)')
parser.add_argument ('-f2', '--flux2', type=float, default=100000.0, \
                     help='total flux of faint star (default: 100000)')
parser.add_argument ('-p', '--psf', type=float, default=5.0, \
                     help='FWHM of stellar radial profile (default: 5)')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
sky_background_level = args.background
noise_level          = args.sigma
nstar                = args.nstar
flux_total_1         = args.flux1
flux_total_2         = args.flux2
psf_fwhm             = args.psf
file_output          = args.output

# making pathlib object
path_output = pathlib.Path (file_output)

# checking output file name
if (file_output == ''):
    # printing message
    print ("You need to specify output file name.")
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # printing message
    print ("Output file must be a FITS file.")
    # exit
    sys.exit ()
# existence check
if (path_output.exists ()):
    # printing message
    print ("Output file exists.")
    # exit
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()

# command name
command = sys.argv[0]

# image size
image_size_x = 1024
image_size_y = 1024
image_size   = (image_size_x, image_size_y)

# location of bright star
x_centre = 500.0
y_centre = 500.0

# region to make stars
half_width = 30.0
x_min = x_centre - half_width
x_max = x_centre + half_width
y_min = y_centre - half_width
y_max = y_centre + half_width

list_x    = numpy.array ([x_centre])
list_y    = numpy.array ([y_centre])
list_flux = numpy.array ([flux_total_1])
list_psf  = numpy.array ([psf_fwhm])

while ( len (list_x) < nstar + 1 ):
    x = numpy.random.uniform (x_min, x_max)
    y = numpy.random.uniform (y_min, y_max)
    dist = numpy.sqrt ( (x - x_centre)**2 + (y - y_centre)**2 )
    if (dist < psf_fwhm * 4.5):
        continue
    list_x    = numpy.append (list_x, x)
    list_y    = numpy.append (list_y, y)
    list_flux = numpy.append (list_flux, flux_total_2)
    list_psf  = numpy.append (list_psf, psf_fwhm)

# generating sky background
image_background \
    = photutils.datasets.make_noise_image (image_size, \
                                           distribution='gaussian', \
                                           mean=sky_background_level, \
                                           stddev=noise_level)

# making a source table
fwhm_sigma = 2.0 * numpy.sqrt (2.0 * numpy.log (2.0) )
source_table = astropy.table.Table ()
source_table['x_0']   = list_x
source_table['y_0']   = list_y
source_table['flux']  = list_flux
source_table['sigma'] = list_psf / fwhm_sigma

# printing source table
print ("source_table:")
print (source_table)

# generating stars
image_star \
    = photutils.datasets.make_gaussian_prf_sources_image (image_size, \
                                                          source_table)

# making synthetic image by adding background and stars
image = image_background + image_star

# preparing a FITS header
header = astropy.io.fits.PrimaryHDU ().header

# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "synthetic astronomical image simulating skybg + stars"
header['comment'] = "Options given:"
header['comment'] = "  image size           = %d x %d" % (image_size)
header['comment'] = "  sky background level = %f ADU" % (sky_background_level)
header['comment'] = "  noise level          = %f ADU" % (noise_level)
header['comment'] = "  number of stars      = %d x %d" % (nstar, nstar)
header['comment'] = "  flux 1 of stars      = %f ADU" % (flux_total_1)
header['comment'] = "  flux 2 of stars      = %f ADU" % (flux_total_2)
header['comment'] = "  FWHM of stars        = %f ADU" % (psf_fwhm)

# writing a FITS file
print ("Now, writing data into FITS file \"%s\"..." % file_output)
astropy.io.fits.writeto (file_output, image, header=header)
print ("Finished writing data!")
