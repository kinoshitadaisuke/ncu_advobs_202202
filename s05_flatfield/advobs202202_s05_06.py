#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/17 21:41:31 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Printing FITS header'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', default='input.fits', help='input fits file')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
file_input  = args.file

# making a pathlib object for input file
path_input = pathlib.Path (file_input)

# checking input file
# if the file is not a FITS file, then stop the script
if not (path_input.suffix == '.fits'):
    # printing error message
    print ("ERROR: input file must be FITS files!")
    print ("ERROR: input file = %s" % file_input)
    # exit the script
    sys.exit ()
# if the file does not exist, then stop the script
if not (path_input.exists ()):
    # printing error message
    print ("ERROR: input file does not exist!")
    print ("ERROR: input file = %s" % file_input)
    # exit the script
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

# printing header
print (repr (header0))
