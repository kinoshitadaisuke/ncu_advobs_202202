#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/04 00:39:40 (CST) daisuke>
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

# construction of parser object
desc = 'Calculating statistical values using sigma clipping with iterations'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS files')
parser.add_argument ('-s', '--sigma', type=float, default=5.0, \
                     help='factor for sigma clipping (default: 5.0)')
parser.add_argument ('-n', '--nmaxiter', type=int, default=10, \
                     help='number of maximum iterations (default: 10)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.sigma
nmaxiter   = args.nmaxiter

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
    # initial value for minimum value
    v_min         = +9.99 * 10**10
    # a variable for a sum of all the pixel values
    total         = 0.0
    # a variable for a square of sum of all the pixel values
    total_sq         = 0.0
    # total number of pixels
    n = data0.size

    # flattening numpy array
    fdata0 = data0.flatten ()
    
    # calculating statistical values
    for x in fdata0:
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
    accepted = fdata0

    # number of iteration
    niter = 0

    # mean and stddev
    mean_clipped   = mean
    stddev_clipped = stddev

    while (niter < nmaxiter):
        # printing status
        print ("# iteration #%03d..." % (niter + 1) )

        # initialising parameters
        total_clipped    = 0.0
        total_sq_clipped = 0.0
        v_max_clipped    = -9.99 * 10**10
        v_min_clipped    = +9.99 * 10**10
        
        # number of rejected pixels before sigma-clipping
        n_rejected_prev = len (rejected)

        # temporary list of accepted pixels
        tmp_accepted = []
        
        # calculating statistical values
        for i in range ( len (accepted) ):
            # if the pixel value is outside of
            # [mean-nsigma*stddev,mean+nsigma*stddev], then reject
            if ( (accepted[i] > mean_clipped + nsigma * stddev_clipped) \
                 or (accepted[i] < mean_clipped - nsigma * stddev_clipped) ):
                # appending the pixel value to the list "rejected"
                rejected.append (accepted[i])
            else:
                # appending the pixel value to the list "tmp_accepted"
                tmp_accepted.append (accepted[i])
                # for calculation of a mean
                total_clipped += accepted[i]
                # for calculation of a variance
                total_sq_clipped += accepted[i]**2
                # for maximum value
                if (accepted[i] > v_max_clipped):
                    v_max_clipped = accepted[i]
                # for minimum value
                if (accepted[i] < v_min_clipped):
                    v_min_clipped = accepted[i]

        # new list of accepted pixels
        accepted = tmp_accepted
                    
        # numbers of accepted and rejected pixels
        n_accepted = len (accepted)
        n_rejected = len (rejected)

        # printing status
        print ("#  n_accepted = %d, n_rejected = %d" \
               % (n_accepted, n_rejected) )
        
        # mean
        mean_clipped   = total_clipped / n_accepted
        # variance
        var_clipped    = total_sq_clipped / n_accepted - mean_clipped**2
        # standard deviation
        stddev_clipped = math.sqrt (var_clipped)

        # checking whether or not leaving from iteration
        if (n_rejected == n_rejected_prev):
            break
        else:
            niter += 1
        
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
