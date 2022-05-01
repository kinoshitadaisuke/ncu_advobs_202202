#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/17 16:39:46 (CST) daisuke>
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
desc = 'Calculating statistical values'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019',
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--datatype', choices=choices_datatype, \
                     default='LIGHT', help='accepted data type')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=5.0, help='accepted exposure time (default: 5.0)')
parser.add_argument ('-f', '--filter', choices=choices_filter, \
                     default='__NONE__', help='accepted data type')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files  = args.files
rejection   = args.rejection
threshold   = args.threshold
datatype    = args.datatype
exptime     = args.exptime
filter_name = args.filter

# printing header
print ("%s" % '-' * 79)
print ("%-25s %8s %8s %8s %8s %8s %8s" \
       % ("file name", "n_pix", "mean", "median", "stddev", "min", "max") )
print ("%s" % '=' * 79)

# processing files
for file_fits in list_files:
    # if the extension of the file is not '.fits', then skip
    if (file_fits[-5:] != '.fits'):
        continue

    # making a pathlib object
    path_fits = pathlib.Path (file_fits)

    # existence check of FITS file
    if not (path_fits.exists ()):
        # if FITS file does not exist, then skip
        continue

    # file name
    filename = path_fits.name

    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # checking image type, exposure time, and filter name
    # if FITS file is not what you want, then skip
    if ('FILTER' in header0):
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) \
                 and (header0['FILTER'] == filter_name) ):
            continue
    else:
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) ):
            continue

    # flattened image data of primary HDU
    data0 = hdu0.data.flatten ()

    # closing FITS file
    hdu_list.close ()

    # if rejection algorithm is used, then do rejection check
    if (rejection == 'sigclip'):
        # sigma clipping using scipy module
        clipped, lower, upper \
            = scipy.stats.sigmaclip (data0, low=threshold, high=threshold)
    # if rejection algorithm is not used, then simply copy data to "clipped"
    elif (rejection == 'none'):
        clipped = data0

    # calculation of statistical values
    n_pix  = len (clipped)
    mean   = numpy.nanmean (clipped)
    median = numpy.nanmedian (clipped)
    stddev = numpy.nanstd (clipped)
    vmin   = numpy.nanmin (clipped)
    vmax   = numpy.nanmax (clipped)
    
    # printing results
    print ("%-25s %8d %8.2f %8.2f %8.2f %8.2f %8.2f" \
           % (filename, n_pix, mean, median, stddev, vmin, vmax) )

# printing footer
print ("%s" % '-' * 79)
