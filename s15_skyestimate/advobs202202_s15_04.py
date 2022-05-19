#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/19 21:24:51 (CST) daisuke>
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
import numpy.ma

# importing astropy module
import astropy.io.fits

# importing photutils module
import photutils.segmentation

# constructing parser object
desc   = 'detecting and masking sources'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input-file', default='', \
                     help='input file name')
parser.add_argument ('-o', '--output-file', default='', \
                     help='output file name')
parser.add_argument ('-t', '--threshold', type=float, default=2.0, \
                     help='detection threshold in sigma (default: 2)')
parser.add_argument ('-n', '--npixels', type=int, default=5, \
                     help='minimum number of pixels for detection (default: 5)')
parser.add_argument ('-s', '--dilate-size', type=int, default=21, \
                     help='dilate size (default: 21)')
parser.add_argument ('-m', '--maxiters', type=int, default=30, \
                     help='maximum number of iterations (default: 30)')

# command-line argument analysis
args = parser.parse_args ()

# file names
file_input  = args.input_file
file_output = args.output_file

# input parameters
threshold   = args.threshold
npixels     = args.npixels
dilate_size = args.dilate_size
maxiters    = args.maxiters

# making pathlib objects
path_input  = pathlib.Path (file_input)
path_output = pathlib.Path (file_output)

# check of input file name
if not (path_input.suffix == '.fits'):
    # printing message
    print ("ERROR: Input file must be a FITS file!")
    # exit
    sys.exit ()

# check of output file name
if not (path_output.suffix == '.fits'):
    # printing message
    print ("ERROR: Output file must be a FITS file!")
    # exit
    sys.exit ()

# existence check of input file
if not (path_input.exists ()):
    # printing message
    print ("ERROR: input file does not exist!")
    # exit
    sys.exit ()

# now
datetime_now = datetime.datetime.now ()

# command name
command = sys.argv[0]

# existence check of output file
if (path_output.exists ()):
    # printing message
    print ("ERROR: output file exists!")
    # exit
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu:
    # reading header and image
    header = hdu[0].header
    image  = hdu[0].data
    # if no image in PrimaryHDU, then read next HDU
    if (header['NAXIS'] == 0):
        header = hdu[1].header
        image  = hdu[1].data

# making source mask
source_mask \
    = photutils.segmentation.make_source_mask (image, threshold, npixels, \
                                               sigclip_iters=maxiters, \
                                               dilate_size=dilate_size)

# making masked array
image_masked = numpy.ma.array (image, mask=source_mask)

# adding comments in header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['comment'] = "Updated on %s" % (datetime_now)
header['comment'] = "Detecting and masking sources"
header['comment'] = "Original file = %s" % (file_input)
header['comment'] = "Options:"
header['comment'] = "  threshold   = %f sigma" % (threshold)
header['comment'] = "  npixels     = %d pixels" % (npixels)
header['comment'] = "  dilate_size = %d pixels" % (dilate_size)
header['comment'] = "  maxiters    = %d" % (maxiters)

# writing a FITS file
astropy.io.fits.writeto (file_output, \
                         numpy.ma.filled (image_masked, fill_value=0.0), \
                         header=header)
