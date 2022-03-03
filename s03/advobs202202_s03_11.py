#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/04 00:50:33 (CST) daisuke>
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
import astropy.stats

# construction of parser object
desc = 'Calculating statistical values using sigma clipping by Astropy'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS file')
parser.add_argument ('-s', '--sigma', type=float, default=5.0, \
                     help='factor for sigma clipping')
parser.add_argument ('-n', '--nmaxiter', type=int, default=10, \
                     help='maximum number of iterations')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.sigma
nmaxiter   = args.nmaxiter

# processing file one-by-one
for file_input in list_files:
    # if input file is not a FITS file, then skip
    if not (file_input[-5:] == '.fits'):
        # printing a message
        print ("# Error: input file must be a FITS file!")
        # skipping to next
        continue

    # file existence check using pathlib module
    path_file_input = pathlib.Path (file_input)
    if not (path_file_input.exists ()):
        # printing a message
        print ("# Error: input file \"%s\" does not exist!" % file_input)
        # skipping to next
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

    # simple mean
    mean   = numpy.mean (data0)
    stddev = numpy.std (data0)
    v_min  = numpy.amin (data0)
    v_max  = numpy.amax (data0)

    # sigma clipped mean
    data0_sigclip  = astropy.stats.sigma_clip (data0, sigma=nsigma, \
                                               maxiters=nmaxiter, masked=False)
    mean_sigclip   = numpy.mean (data0_sigclip)
    stddev_sigclip = numpy.std (data0_sigclip)
    v_min_sigclip  = numpy.amin (data0_sigclip)
    v_max_sigclip  = numpy.amax (data0_sigclip)

    # printing result
    print ("before clipping:")
    print ("  %s  %10.3f %10.3f %10.3f %10.3f" \
           % (filename, mean, stddev, v_min, v_max) )
    print ("after clipping:")
    print ("  %s  %10.3f %10.3f %10.3f %10.3f" \
           % (filename, mean_sigclip, stddev_sigclip, \
              v_min_sigclip, v_max_sigclip) )
    print ("size of data0             = %d" % data0.size)
    print ("size of data0_sigclip     = %d" % data0_sigclip.size)
    print ("number of rejected pixels = %d" \
           % (data0.size - data0_sigclip.size) )
