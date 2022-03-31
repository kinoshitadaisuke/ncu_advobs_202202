#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 22:29:19 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'normalising FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('file_input', nargs=1, help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_output = args.output
file_input  = args.file_input[0]

# making pathlib objects
path_input  = pathlib.Path (file_input)
path_output = pathlib.Path (file_output)

# checking input file name
if not (path_input.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()
if not (path_input.exists ()):
    # printing message
    print ("file '%s' does not exist." % file_input)
    # exit
    sys.exit ()

# checking output file name
if (file_output == ''):
    # printing message
    print ("Output file name has to be given.")
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # printing message
    print ("Output file must be a FITS file.")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("file '%s' exists." % file_output)
    # exit
    sys.exit ()

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# printing status
print ("#")
print ("# input file  = %s" % file_input)
print ("# output file = %s" % file_output)
print ("#")

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # header of primary HDU
    header = hdu_list[0].header

    # image of primary HDU
    # reading the data as float64
    data = hdu_list[0].data.astype (numpy.float64)

# mean of pixel values
mean = numpy.mean (data)

# printing status
print ("# mean value of input file = %f" % mean)

# normalisation
data_normalised = data / mean

# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "normalisation of a FITS file"
header['comment'] = "Input file: %s" % (file_input)
header['comment'] = "Mean of pixel values of input file = %f" % (mean)

# writing a new FITS file
astropy.io.fits.writeto (file_output, data_normalised, header=header)
