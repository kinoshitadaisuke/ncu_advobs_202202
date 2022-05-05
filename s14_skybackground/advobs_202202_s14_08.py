#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/05 16:16:22 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = "calculating pixel scale"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input', default='', help='input FITS file name')
parser.add_argument ('-x', '--keyword-pixsize-x', default='XPIXSZ', \
                     help='FITS keyword for pixel width in micron')
parser.add_argument ('-y', '--keyword-pixsize-y', default='YPIXSZ', \
                     help='FITS keyword for pixel height in micron')
parser.add_argument ('-l', '--keyword-focallength', default='FOCALLEN', \
                     help='FITS keyword for focal length in mm')

# parsing arguments
args = parser.parse_args ()

# input parameters
file_input          = args.input
keyword_pixelsize_x = args.keyword_pixsize_x
keyword_pixelsize_y = args.keyword_pixsize_y
keyword_focallength = args.keyword_focallength

# making a pathlib object
path_input  = pathlib.Path (file_input)

# existence checks of file
if not (path_input.exists ()):
    # printing message
    print ("ERROR: input file does not exist.")
    # exit
    sys.exit ()

# check of input FITS file
if not (path_input.suffix == '.fits'):
    # printing message
    print ("ERROR: input file must be a FITS file.")
    print ("ERROR: given input file name = %s" % file_input)
    # exit
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # reading header information
    header = hdu_list[0].header

# pixel size and focal length
pixelsize_x_micron = header[keyword_pixelsize_x]
pixelsize_y_micron = header[keyword_pixelsize_y]
focallength_mm     = header[keyword_focallength]

# calculation of pixel scale
pixelscale_x_rad    = pixelsize_x_micron * 10**-6 / (focallength_mm * 10**-3)
pixelscale_y_rad    = pixelsize_y_micron * 10**-6 / (focallength_mm * 10**-3)
pixelscale_x_arcsec = pixelscale_x_rad * 180.0 / numpy.pi * 3600.0
pixelscale_y_arcsec = pixelscale_y_rad * 180.0 / numpy.pi * 3600.0

# printing result
print ("pixel scale along x-axis = %6.4f arcsec/pix" % pixelscale_x_arcsec)
print ("pixel scale along y-axis = %6.4f arcsec/pix" % pixelscale_y_arcsec)
