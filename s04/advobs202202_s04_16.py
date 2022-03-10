#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/11 00:07:37 (CST) daisuke>
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
parser.add_argument ('file', default='', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
file_input  = args.file

# checking input file
# if the file is not a FITS file, then stop the script
if not (file_input[-5:] == '.fits'):
    # printing error message
    print ("Input file must be FITS files!")
    # exit the script
    sys.exit ()
# if the file does not exist, then stop the script
path_input = pathlib.Path (file_input)
if not (path_input.exists ()):
    # printing error message
    print ("Input file FITS file does not exist!")
    # exit the script
    sys.exit ()

# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# primary HDU
hdu0 = hdu_list[0]

# reading header
header0 = hdu0.header

# closing FITS file
hdu_list.close ()

# printing header
print (repr (header0))
