#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/14 11:56:57 (CST) daisuke>
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
desc   = 'generating a synthetic image of sky background and stars'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-b', '--background', type=float, default=2500.0, \
                     help='background level (default: 2500)')
parser.add_argument ('-s', '--sigma', type=float, default=50.0, \
                     help='noise level (default: 50)')
parser.add_argument ('-n', '--nstar', type=int, default=5, \
                     help='number of stars to generate (n x n) (default: 5)')
parser.add_argument ('-f1', '--fluxmin', type=float, default=100000.0, \
                     help='min total flux of star (default: 100000)')
parser.add_argument ('-f2', '--fluxmax', type=float, default=200000.0, \
                     help='max total flux of star (default: 200000)')
parser.add_argument ('-p1', '--psfmin', type=float, default=4.0, \
                     help='min FWHM of stellar radial profile (default: 4)')
parser.add_argument ('-p2', '--psfmax', type=float, default=6.0, \
                     help='max FWHM of stellar radial profile (default: 6)')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
sky_background_level = args.background
noise_level          = args.sigma
nstar                = args.nstar
flux_total_min       = args.fluxmin
flux_total_max       = args.fluxmax
psf_fwhm_min         = args.psfmin
psf_fwhm_max         = args.psfmax
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

# image size
image_size_x = 1024
image_size_y = 1024
image_size   = (image_size_x, image_size_y)
coord_min    = 100.0
coord_max    = 900.0

# date/time
now = datetime.datetime.now ().isoformat ()

# command name
command = sys.argv[0]

# printing status
print ("Now, generating synthetic sky background...")

# generating sky background
image_background \
    = photutils.datasets.make_noise_image (image_size, \
                                           distribution='gaussian', \
                                           mean=sky_background_level, \
                                           stddev=noise_level)

# printing status
print ("Finished generating synthetic sky background!")

# printing status
print ("Now, generating synthetic stars...")

# grid of data for generating synthetic stars
#
# x coord ==> [100, 300, 500, 700, 900, 100, 300, 500, 700, 900, 100, ...]
# y coord ==> [100, 100, 100, 100, 100, 300, 300, 300, 300, 300, 500, ...]
#

# initialisation of numpy arrays
list_x    = numpy.array ([])
list_y    = numpy.array ([])
list_flux = numpy.array ([])
list_psf  = numpy.array ([])

# generating X coordinates of synthetic stars
for i in range (nstar):
    list_x \
        = numpy.append (list_x, numpy.linspace (coord_min, coord_max, nstar) )

# generating X coordinates of synthetic stars
for y in numpy.linspace (coord_min, coord_max, nstar):
    list_y = numpy.append (list_y, numpy.repeat (y, nstar) )

# flux of stars
for i in range (nstar):
    list_flux \
        = numpy.append (list_flux, \
                        numpy.linspace (flux_total_min, flux_total_max, nstar) )

# FWHM of PSF of synthetic stars
for psf in numpy.linspace (psf_fwhm_min, psf_fwhm_max, nstar):
    list_psf = numpy.append (list_psf, numpy.repeat (psf, nstar) )

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

# printing status
print ("Finished generating synthetic stars!")

# printing status
print ("Now, making a synthetic image skybg + stars...")

# making synthetic image by adding background and stars
image = image_background + image_star

# printing status
print ("Finished making a synthetic image skybg + stars!")

# printing status
print ("Now, preparing FITS header...")

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
header['comment'] = "  min flux of stars    = %f ADU" % (flux_total_min)
header['comment'] = "  max flux of stars    = %f ADU" % (flux_total_max)
header['comment'] = "  min FWHM of stars    = %f ADU" % (psf_fwhm_min)
header['comment'] = "  max FWHM of stars    = %f ADU" % (psf_fwhm_max)

# printing status
print ("Finished preparing FITS header!")

# printing status
print ("Now, writing data into FITS file \"%s\"..." % file_output)

# writing a FITS file
astropy.io.fits.writeto (file_output, image, header=header)

# printing status
print ("Finished writing data into FITS file \"%s\"!" % file_output)

