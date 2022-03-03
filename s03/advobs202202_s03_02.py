#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 15:26:58 (CST) daisuke>
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
desc = 'Reading image data from a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input', default='test.fits', \
                     help='intput FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input = args.input

# if input file is not a FITS file, then skip
if not (file_input[-5:] == '.fits'):
    # printing a message
    print ("Error: input file must be a FITS file!")
    # exit
    sys.exit ()

# file existence check using pathlib module
path_file_input = pathlib.Path (file_input)
if not (path_file_input.exists ()):
    # printing a message
    print ("Error: input file \"%s\" does not exist!" % file_input)
    # exit
    sys.exit ()
    
# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# primary HDU
hdu0 = hdu_list[0]

# reading header
header0 = hdu0.header

# reading data
data0 = hdu0.data

# closing FITS file
hdu_list.close ()

# printing shape of data
print ("object type        =", type (data0) )
print ("dimensions of data =", data0.ndim)
print ("shape of data      =", data0.shape)
print ("number of pixels   =", data0.size, "pixels")
print ("data type          =", data0.dtype)

# printing data
print ("pixel data:")
print (data0)
