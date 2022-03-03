#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/04 01:07:51 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing math module
import math

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc = 'estimating readout noise from two bias frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-b1', '--bias1', default='bias1.fits', \
                     help='bias frame 1')
parser.add_argument ('-b2', '--bias2', default='bias2.fits', \
                     help='bias frame 2')
parser.add_argument ('-s', '--sigma', type=float, default=5.0, \
                     help='factor for sigma clipping')
parser.add_argument ('-n', '--nmaxiter', type=int, default=10, \
                     help='maximum number of iterations')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_bias1 = args.bias1
file_bias2 = args.bias2
nsigma     = args.sigma
nmaxiter   = args.nmaxiter

# if input file is not a FITS file, then skip
if not ( (file_bias1[-5:] == '.fits') and (file_bias2[-5:] == '.fits') ):
    # printing a message
    print ("Error: input file must be a FITS file!")
    # exit
    sys.exit ()

# file existence check using pathlib module
path_file_bias1 = pathlib.Path (file_bias1)
if not (path_file_bias1.exists ()):
    # printing a message
    print ("Error: input file \"%s\" does not exist!" % file_bias1)
    # exit
    sys.exit ()
path_file_bias2 = pathlib.Path (file_bias2)
if not (path_file_bias2.exists ()):
    # printing a message
    print ("Error: input file \"%s\" does not exist!" % file_bias2)
    # exit
    sys.exit ()

# file names
filename1 = path_file_bias1.name
filename2 = path_file_bias2.name

# opening FITS file
hdu_list1 = astropy.io.fits.open (file_bias1)
hdu_list2 = astropy.io.fits.open (file_bias2)

# primary HDU
hdu1 = hdu_list1[0]
hdu2 = hdu_list2[0]

# reading header
header1 = hdu1.header
header2 = hdu2.header

# reading data and conversion from uint16 into float64
bias1 = hdu1.data.astype (numpy.float64)
bias2 = hdu2.data.astype (numpy.float64)

# closing FITS file
hdu_list1.close ()
hdu_list2.close ()

# calculation of (bias1 - bias2)
diff_b1_b2 = bias1 - bias2

# sigma clipped mean and stddev
diff_sigclip  = astropy.stats.sigma_clip (diff_b1_b2, sigma=nsigma, \
                                          maxiters=nmaxiter, masked=False)
mean_sigclip   = numpy.mean (diff_sigclip)
stddev_sigclip = numpy.std  (diff_sigclip)
v_min_sigclip  = numpy.amin (diff_sigclip)
v_max_sigclip  = numpy.amax (diff_sigclip)

# printing result
print ("selected bias frames: %s and %s" % (filename1, filename2) )
print ("mean of bias1           = %f" % numpy.mean (bias1) )
print ("mean of bias2           = %f" % numpy.mean (bias2) )
print ("mean of diff            = %f" % numpy.mean (diff_b1_b2) )
print ("mean_sigclip            = %f" % mean_sigclip)
print ("stddev of diff          = %f ADU" % stddev_sigclip)
print ("estimated readout noise = %f ADU" % (stddev_sigclip / math.sqrt(2.0) ) )
