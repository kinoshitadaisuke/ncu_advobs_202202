#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 21:02:57 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Calculating average value of pixel values of images'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files = args.files

# printing header
print ("%-32s %8s %8s %8s %8s %8s" \
       % ('file', 'max', 'min', 'mean', 'median', 'stddev') )
print ("%s" % '-' * 77)

# processing files
for file in list_files:
    # if the extension of the file is not '.fits', then skip
    if (file[-5:] != '.fits'):
        continue

    # file name
    path = file.split ('/')
    filename = path[-1]

    # opening FITS file
    hdu_list = astropy.io.fits.open (file)

    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # data of primary HDU
    data0 = hdu0.data
    
    # closing FITS file
    hdu_list.close ()

    # calculations of statistical values using numpy
    data_max      = numpy.amax (data0)
    data_min      = numpy.amin (data0)
    data_mean     = numpy.mean (data0)
    data_median   = numpy.median (data0)
    data_variance = numpy.var (data0)
    data_stddev   = numpy.std (data0)

    # printing results
    print ("%-32s %8.2f %8.2f %8.2f %8.2f %8.2f" \
           % (filename, data_max, data_min, \
              data_mean, data_median, data_stddev) )
