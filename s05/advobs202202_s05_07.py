#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/17 22:26:04 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Image subtraction'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('minuend', help='minuend (FITS file)')
parser.add_argument ('subtrahend', help='subtrahend (FITS file)')
parser.add_argument ('output', help='output file (FITS file)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_minuend    = args.minuend
file_subtrahend = args.subtrahend
file_output     = args.output

# command name
command = sys.argv[0]

# printing information
print ("# Arithmetic operation being done:")
print ("#   %s - %s" % (file_minuend, file_subtrahend) )
print ("#     ==> %s" % file_output)

# checking input FITS files
for file_fits in (file_minuend, file_subtrahend):
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    # if input file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print ("ERROR: input file must be FITS files!")
        print ("ERROR: the file \"%s\" is not a FITS file!" % file_fits)
        # exit the script
        sys.exit ()
    # if input FITS file does not exist, then stop the script
    if not (path_fits.exists ()):
        # printing error message
        print ("ERROR: input file does not exist!")
        print ("ERROR: input file = \"%s\"" % file_fits)
        # exit the script
        sys.exit ()

# checking output FITS files
# making pathlib object
path_fits = pathlib.Path (file_output)
# if output file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing error message
    print ("ERROR: output file must be FITS files!")
    print ("ERROR: the file \"%s\" is not a FITS file!" % file_fits)
    # exit the script
    sys.exit ()
# if input FITS file does not exist, then stop the script
if (path_fits.exists ()):
    # printing error message
    print ("ERROR: output file exists!")
    print ("ERROR: output file = \"%s\"" % file_fits)
    # exit the script
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()

#
# reading minuend FITS file
#

# printing status
print ("# now, reading the file \"%s\"..." % file_minuend)

# opening FITS file
with astropy.io.fits.open (file_minuend) as hdu_minuend:
    # primary HDU
    hdu0 = hdu_minuend[0]

    # reading header
    header = hdu0.header

    # reading image
    data_minuend = hdu0.data

# printing status
print ("# finished reading the file \"%s\"!" % file_minuend)

#
# reading subtrahend FITS file
#

# printing status
print ("# now, reading the file \"%s\"..." % file_subtrahend)

# opening FITS file
with astropy.io.fits.open (file_subtrahend) as hdu_subtrahend:
    # primary HDU
    hdu1 = hdu_subtrahend[0]

    # reading image
    data_subtrahend = hdu1.data

# printing status
print ("# finished reading the file \"%s\"!" % file_subtrahend)

#
# image subtraction
#

# printing status
print ("# now, subtracting %s from %s..." % (file_minuend, file_subtrahend) )

# calculation for image subtraction
data_subtracted = data_minuend - data_subtrahend

# printing status
print ("# finished subtracting %s from %s!" % (file_minuend, file_subtrahend) )

#
# writing output FITS file
#

# printing status
print ("# now, writing a FITS file \"%s\"..." % file_output)

# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "Image subtraction:"
header['comment'] = "  minuend    = %s" % (file_minuend)
header['comment'] = "  subtrahend = %s" % (file_subtrahend)
header['comment'] = "  output     = %s" % (file_output)

# writing a new FITS file
astropy.io.fits.writeto (file_output, data_subtracted, header=header)

# printing status
print ("# finished writing a FITS file \"%s\"!" % file_output)
