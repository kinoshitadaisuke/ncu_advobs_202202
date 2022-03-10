#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 22:00:08 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Calculating statistical values using SciPy'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
list_rejection = ['none', 'sigclip']
parser.add_argument ('-r', '--rejection', choices=list_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files = args.files
rejection  = args.rejection
threshold  = args.threshold

# printing header
print ("%s" % '-' * 78)
print ("%-24s %8s %8s %8s %8s %8s %8s" \
       % ("file name", "n_pix", "mean", "median", "stddev", "min", "max") )
print ("%s" % '=' * 78)

# processing files
for file_fits in list_files:
    # if the extension of the file is not '.fits', then skip
    if (file_fits[-5:] != '.fits'):
        continue

    # if the file does not exist, then skip
    path_fits = pathlib.Path (file_fits)
    if not (path_fits.exists ()):
        continue

    # file name
    filename = path_fits.name

    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # image data of primary HDU
    data0 = hdu0.data

    # closing FITS file
    hdu_list.close ()

    # flattening data (2-dim. data --> 1-dim. data)
    data_1d = data0.flatten ()

    # if rejection algorithm is used, then do rejection check
    if (rejection == 'sigclip'):
        clipped, lower, upper \
            = scipy.stats.sigmaclip (data_1d, low=threshold, high=threshold)
    elif (rejection == 'none'):
        clipped = data_1d

    # calculation of statistical values
    n_pix  = len (clipped)
    mean   = numpy.nanmean (clipped)
    median = numpy.nanmedian (clipped)
    stddev = numpy.nanstd (clipped)
    vmin   = numpy.nanmin (clipped)
    vmax   = numpy.nanmax (clipped)
    
    # printing results
    print ("%-24s %8d %8.2f %8.2f %8.2f %8.2f %8.2f" \
           % (filename, n_pix, mean, median, stddev, vmin, vmax) )

# printing footer
print ("%s" % '-' * 78)
