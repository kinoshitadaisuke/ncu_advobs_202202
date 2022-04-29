#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 21:41:42 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# import pathlib module
import pathlib

# importing math module
import math

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Reading a FITS file and calculating statistical values'
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

# initial value for maximum value
v_max = -9.99 * 10**10
# initial value for minimum value
v_min = +9.99 * 10**10
# a variable for a sum of all the pixel values
total = 0.0
# a variable for a square of sum of all the pixel values
total_sq = 0.0
# total number of pixels
n = data0.size
# a 1-dim. list for data
data0_1d = []

# calculating statistical values
for i in range (len (data0) ):
    for j in range (len (data0[i]) ):
        # for calculation of a mean
        total += data0[i][j]
        # for calculation of a variance
        total_sq += data0[i][j]**2
        # for maximum value
        if (data0[i][j] > v_max):
            v_max = data0[i][j]
        # for minimum value
        if (data0[i][j] < v_min):
            v_min = data0[i][j]
        # making 1-dim. list
        data0_1d.append (data0[i][j])

# mean
mean   = total / n
# variance
var    = total_sq / n - mean**2
# standard deviation
stddev = math.sqrt (var)

# sorting
data0_1d_sorted = sorted (data0_1d)
# median
if (n % 2 == 0):
    median = (data0_1d_sorted[int (n / 2) - 1] \
              + data0_1d_sorted[int (n / 2)]) / 2.0
else:
    median = data0_1d_sorted[int (n / 2)]

# printing result
print ("# file name, mean, median, stddev, min, max")
print ("%s    %f %f %f %f %f" \
       % (filename, mean, median, stddev, v_min, v_max) )
