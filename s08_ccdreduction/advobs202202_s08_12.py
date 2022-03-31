#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 16:57:00 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy
import astropy.io.fits
import astropy.stats

# construction pf parser object
desc   = 'combining dark frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
list_datatype  = ['BIAS', 'DARK', 'FLAT', 'LIGHT']
list_rejection = ['NONE', 'sigclip']
list_cenfunc   = ['mean', 'median']
parser.add_argument ('-e', '--exptime', type=float, default=0.0, \
                     help='exposure time')
parser.add_argument ('-f', '--filter', default='', help='filter name')
parser.add_argument ('-d', '--datatype', default='BIAS', \
                     choices=list_datatype, help='data type')
parser.add_argument ('-r', '--rejection', default='NONE', \
                     choices=list_rejection, \
                     help='rejection algorithm (default: NONE)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='threshold for sigma clipping (default: 4.0)')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('-c', '--cenfunc', choices=list_cenfunc, \
                     default='median', \
                     help='method to estimate centre value (default: median)')
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
exptime0    = args.exptime
filter0     = args.filter
datatype0   = args.datatype
rejection   = args.rejection
threshold   = args.threshold
maxiters    = args.maxiters
cenfunc     = args.cenfunc
file_output = args.output
list_files  = args.files

# examination of output file
path_output = pathlib.Path (file_output)
if (file_output == ''):
    # printing message
    print ("Output file name must be given.")
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # printing message
    print ("Output file must be a FITS file.")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("Output file exists.")
    # exit
    sys.exit ()

# command name
command = sys.argv[0]
    
# declaration of list
list_target_files = []

# date/time
now = datetime.datetime.now ().isoformat ()

# printing information
print ("# Data search condition:")
print ("#   data type = %s" % datatype0)
print ("#   exptime   = %.3f sec" % exptime0)
print ("#   filter    = \"%s\"" % filter0)
print ("# Input parameters")
print ("#   rejection algorithm = %s" % rejection)
print ("#   threshold of sigma-clipping = %f" % threshold)
print ("#   maximum number of iterations = %d" % maxiters)

# printing status
print ("#")
print ("# Now scanning data...")

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
    # data type
    if ('IMAGETYP' in header):
        datatype = header['IMAGETYP']
    else:
        datatype = "__NONE__"
    # exposure time
    if ('EXPTIME' in header):
        exptime = header['EXPTIME']
    else:
        exptime = -999.99
    # filter name
    if ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        filter_name = header['FILTER']
    else:
        filter_name = 'NONE'
    
    # check of FITS header
    if ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        if ( (datatype == datatype0) and (exptime == exptime0) \
             and (filter_name == filter0) ):
            # appending file name to the list
            list_target_files.append (file_fits)
    elif ( (datatype == 'BIAS') or (datatype == 'DARK') ):
        if ( (datatype == datatype0) and (exptime == exptime0) ):
            # appending file name to the list
            list_target_files.append (file_fits)

# printing status
print ("#")
print ("# Finished scanning files")
print ("#   %d files are found for combining!" % len (list_target_files) )

# checking number of target files
if ( len (list_target_files) < 2 ):
    # printing message
    print ("number of target files must be greater than 1.")
    # exit
    sys.exit ()

print ("#")
print ("# Target files:")
for file_fits in list_target_files:
    print ("#   %s" % file_fits)

# counter
i = 0

# printing status
print ("#")
print ("# Reading image data...")

# reading dark frames
for file_fits in list_target_files:
    # printing status
    print ("#   %04d: \"%s\"" % (i + 1, file_fits) )
    
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU (only for the first file)
        if (i == 0):
            header = hdu_list[0].header
    
        # image of primary HDU
        # reading the data as float64
        data = hdu_list[0].data.astype (numpy.float64)
    
    # making a mask and masked array

    # for no rejection algorithm
    if (rejection == 'NONE'):
        # making a mask
        mask = numpy.zeros_like (data)
    # for sigma clipping algorithm
    elif (rejection == 'sigclip'):
        # making a masked array
        mdata = numpy.ma.array (data, mask=False)
        # iterations
        for j in range (maxiters):
            # number of usable pixels of previous iterations
            npix_prev = len ( numpy.ma.compressed (mdata) )
            # calculation of median
            median = numpy.ma.median (mdata)
            # calculation of standard deviation
            stddev = numpy.ma.std (mdata)
            # lower threshold
            low = median - threshold * stddev
            # higher threshold
            high = median + threshold * stddev
            # making a mask
            mask = (mdata < low) | (mdata > high)
            # masked array
            mdata = numpy.ma.array (data, mask=mask)
            # number of rejected pixels
            npix_now = len ( numpy.ma.compressed (mdata) )
            # leaving the loop, if number of usable pixels do not change
            if (npix_now == npix_prev):
                break
        
    # constructing a data cube and its mask
    if (i == 0):
        data_tmp = data
        mask_tmp = mask
    elif (i == 1):
        cube      = numpy.concatenate ( ([data_tmp], [data]), axis=0 )
        cube_mask = numpy.concatenate ( ([mask_tmp], [mask]), axis=0 )
    else:
        cube      = numpy.concatenate ( (cube, [data]), axis=0 )
        cube_mask = numpy.concatenate ( (cube_mask, [mask]), axis=0 )

    # incrementing "i" for counting number of files
    i += 1

# printing status
print ("#")
print ("# Finished reading image data")

# printing status
print ("#")
print ("# Combining image...")

# constructing a masked data cube
masked_cube = numpy.ma.array (cube, mask=cube_mask)

# combining dark frames
if (rejection == 'sigclip'):
    # sigma clipping using Astropy
    clipped_masked_cube = \
        astropy.stats.sigma_clip (masked_cube, sigma=threshold, \
                                  maxiters=maxiters, cenfunc=cenfunc, \
                                  axis=0, masked=True)
    # combining using average
    combined = numpy.ma.average (clipped_masked_cube, axis=0)
elif (rejection == 'NONE'):
    # combining using simple average
    combined = numpy.ma.average (masked_cube, axis=0)

# printing status
print ("#")
print ("# Finished combining image")

# printing status
print ("#")
print ("# Writing image into a new FITS file...")
print ("#   output file = %s" % file_output)

# mean of combined image
mean_combined = numpy.ma.mean (combined)
    
# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "multiple FITS files are combined into a single FITS file"
header['comment'] = "List of combined files:"
for file_fits in list_target_files:
    header['comment'] = "  %s" % (file_fits)
header['comment'] = "Options given:"
header['comment'] = "  rejection = %s" % (rejection)
header['comment'] = "  threshold = %f sigma" % (threshold)
header['comment'] = "  maxiters  = %d" % (maxiters)
header['comment'] = "  cenfunc   = %s" % (cenfunc)

# writing a new FITS file
astropy.io.fits.writeto (file_output, \
                         numpy.ma.filled (combined, fill_value=mean_combined), \
                         header=header)

# printing status
print ("#")
print ("# Finished writing image into a new FITS file")
print ("#")
