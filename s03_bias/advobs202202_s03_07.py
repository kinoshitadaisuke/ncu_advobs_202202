#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 22:07:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# import pathlib module
import pathlib

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Reading FITS files and calculating statistical values using Numpy'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files

# printing header
print ("# file name, mean, median, stddev, min, max")

# processing files one-by-one
for file_input in list_files:
    # if input file is not a FITS file, then skip
    if not (file_input[-5:] == '.fits'):
        # printing a message
        print ("# Error: input file must be a FITS file!")
        # skipping to next file
        continue

    # file existence check using pathlib module
    path_file_input = pathlib.Path (file_input)
    if not (path_file_input.exists ()):
        # printing a message
        print ("# Error: input file \"%s\" does not exist!" % file_input)
        # skipping to next file
        continue

    # file name
    filename = path_file_input.name
    
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

    # calculating statistical values
    mean   = numpy.mean (data0)
    median = numpy.median (data0)
    stddev = numpy.std (data0)
    v_min  = numpy.amin (data0)
    v_max  = numpy.amax (data0)

    # printing result
    print ("%s  %10.3f %10.3f %10.3f %10.3f %10.3f" \
           % (filename, mean, median, stddev, v_min, v_max) )
