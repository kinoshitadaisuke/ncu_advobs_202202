#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 16:34:39 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy
import astropy.io.fits

# construction pf parser object
desc   = 'calculating statistical information of FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_datatype  = ['BIAS', 'DARK', 'FLAT', 'LIGHT']
choices_rejection = ['NONE', 'sigclip']
parser.add_argument ('-e', '--exptime', type=float, default=0.0, \
                     help='exposure time')
parser.add_argument ('-f', '--filter', default='', help='filter name')
parser.add_argument ('-d', '--datatype', default='BIAS', \
                     choices=choices_datatype, help='data type')
parser.add_argument ('-r', '--rejection', default='NONE', \
                     choices=choices_rejection, help='rejection algorithm')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='threshold for sigma clipping')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
exptime0   = args.exptime
filter0    = args.filter
datatype0  = args.datatype
rejection  = args.rejection
threshold  = args.threshold
maxiters   = args.maxiters
list_files = args.files

# printing information
print ("# Data search condition:")
print ("#   data type = %s" % datatype0)
print ("#   exptime   = %.3f sec" % exptime0)
print ("#   filter    = \"%s\"" % filter0)
print ("# Input parameters")
print ("#   rejection algorithm = %s" % rejection)
print ("#   threshold of sigma-clipping = %f" % threshold)

# printing header
print ("#")
print ("# %-22s %8s %8s %8s %8s %8s %8s" \
       % ('file name', 'npix', 'mean', 'median', 'stddev', 'min', 'max') )
print ("#")

# scanning files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the file is not a FITS file, then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print ("### file '%s' is not a FITS file! skipping..." % file_fits)
        # skipping
        continue

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

    # FITS keywords
    datatype = header['IMAGETYP']
    exptime  = header['EXPTIME']
    if ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        filter_name = header['FILTER']
    else:
        filter_name = 'NONE'
    
    # calculate statistical information?
    calc = 0

    # check of FITS header
    # if criteria match, then we do calculate statistical information
    if ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        if ( (datatype == datatype0) and (exptime == exptime0) \
             and (filter_name == filter0) ):
            # we do calculate statistical information
            calc = 1
    elif ( (datatype == 'BIAS') or (datatype == 'DARK') ):
        if ( (datatype == datatype0) and (exptime == exptime0) ):
            # we do calculate statistical information
            calc = 1
            
    # skip, if calc == 0
    if (calc == 0):
        continue

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # image of primary HDU
        data0 = hdu_list[0].data
    
    # calculations

    # for no rejection algorithm
    if (rejection == 'NONE'):
        # making a masked array
        data1 = numpy.ma.array (data0, mask=False)
    # for sigma clipping algorithm
    elif (rejection == 'sigclip'):
        data1 = numpy.ma.array (data0, mask=False)
        # iterations
        for j in range (maxiters):
            # number of usable pixels of previous iterations
            npix_prev = len (numpy.ma.compressed (data1) )
            # calculation of median
            median = numpy.ma.median (data1)
            # calculation of standard deviation
            stddev = numpy.ma.std (data1)
            # lower threshold
            low = median - threshold * stddev
            # higher threshold
            high = median + threshold * stddev
            # making a mask
            mask = (data1 < low) | (data1 > high)
            # making a masked array
            data1 = numpy.ma.array (data0, mask=mask)
            # number of usable pixels
            npix_now = len (numpy.ma.compressed (data1) )
            # leaving the loop, if number of usable pixels do not change
            if (npix_now == npix_prev):
                break
        
    # calculation of mean, median, stddev, min, and max
    mean   = numpy.ma.mean (data1)
    median = numpy.ma.median (data1)
    stddev = numpy.ma.std (data1)
    vmin   = numpy.ma.min (data1)
    vmax   = numpy.ma.max (data1)

    # number of pixels
    npix = len (data1.compressed () )

    # file name
    filename = path_fits.name

    # printing result
    print ("%-24s %8d %8.2f %8.2f %8.2f %8.2f %8.2f" \
           % (filename, npix, mean, median, stddev, vmin, vmax) )
