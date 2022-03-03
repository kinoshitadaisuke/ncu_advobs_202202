#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 23:34:50 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing math module
import math

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Calculating statistical values using sigma clipping'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS files')
parser.add_argument ('-s', '--sigma', type=float, default=5.0, \
                     help='factor for sigma clipping')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.sigma

# processing files one-by-one
for file_input in list_files:
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
    v_max         = -9.99 * 10**10
    v_max_clipped = -9.99 * 10**10
    # initial value for minimum value
    v_min         = +9.99 * 10**10
    v_min_clipped = +9.99 * 10**10
    # a variable for a sum of all the pixel values
    total         = 0.0
    total_clipped = 0.0
    # a variable for a square of sum of all the pixel values
    total_sq         = 0.0
    total_sq_clipped = 0.0
    # total number of pixels
    n = data0.size

    # calculating statistical values
    for row in data0:
        for x in row:
            # for calculation of a mean
            total += x
            # for calculation of a variance
            total_sq += x**2
            # for maximum value
            if (x > v_max):
                v_max = x
            # for minimum value
            if (x < v_min):
                v_min = x

    # mean
    mean   = total / n
    # variance
    var    = total_sq / n - mean**2
    # standard deviation
    stddev = math.sqrt (var)

    # lists for rejected and accepted values
    rejected = []
    accepted = []

    # calculating statistical values
    for row in data0:
        for x in row:
            # if the pixel value is outside of
            # [mean-nsigma*stddev,mean+nsigma*stddev], then reject
            if ( (x > mean + nsigma * stddev) or (x < mean - nsigma * stddev) ):
                # appending the pixel value to the list "rejected"
                rejected.append (x)
            else:
                # appending the pixel value to the list "accepted"
                accepted.append (x)
                # for calculation of a mean
                total_clipped += x
                # for calculation of a variance
                total_sq_clipped += x**2
                # for maximum value
                if (x > v_max_clipped):
                    v_max_clipped = x
                # for minimum value
                if (x < v_min_clipped):
                    v_min_clipped = x

    # numbers of accepted and rejected pixels
    n_accepted = len (accepted)
    n_rejected = len (rejected)

    # mean
    mean_clipped   = total_clipped / n_accepted
    # variance
    var_clipped    = total_sq_clipped / n_accepted - mean_clipped**2
    # standard deviation
    stddev_clipped = math.sqrt (var_clipped)

    # printing result
    print ("before clipping:")
    print ("  %s  %10.3f %10.3f %10.3f %10.3f" \
           % (filename, mean, stddev, v_min, v_max) )
    print ("after clipping:")
    print ("  %s  %10.3f %10.3f %10.3f %10.3f" \
           % (filename, mean_clipped, stddev_clipped, \
              v_min_clipped, v_max_clipped) )
    print ("results of sigma-clipping:")
    print ("  number of accepted pixels = %10d" % n_accepted)
    print ("  number of rejected pixels = %10d" % n_rejected)
    print ("  rejected pixel values     =", sorted (rejected) )
