#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/17 23:43:11 (CST) daisuke>
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

# importing datetime module
import datetime

# construction of parser object
desc = 'Combining flatfields'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--datatype', choices=choices_datatype, \
                     default='LIGHT', \
                     help='accepted data type (default: LIGHT)')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=5.0, help='accepted exposure time (default: 5)')
parser.add_argument ('-f', '--filter', choices=choices_filter, \
                     default='__NONE__', help='accepted filter name')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', help='outlier rejection algorithm')
parser.add_argument ('-t', '--threshold', type=float, default=5.0, \
                     help='rejection threshold in sigma')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='median', help='method to estimate centre value')
parser.add_argument ('-o', '--output', default='combined.fits', \
                     help='output FITS file')
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
list_input  = args.files
file_output = args.output
rejection   = args.rejection
threshold   = args.threshold
cenfunc     = args.cenfunc
maxiters    = args.maxiters
datatype    = args.datatype
exptime     = args.exptime
filter_name = args.filter

# command name
command = sys.argv[0]

# checking number of intput FITS files
if ( len (list_input) < 2 ):
    # if the number of input files is less than 2, then stop the script
    print ("ERROR: Number of input files must be 2 or larger!")
    print ("ERROR: input files =", list_input)
    # exit the script
    sys.exit ()

# checking input files
for file_fits in list_input:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    # if the file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print ("ERROR: Input files must be FITS files!")
        print ("ERROR: The file \"%s\" is not a FITS file!" % file_fits)
        # exit the script
        sys.exit ()
    # if the file does not exist, then stop the script
    if not (path_fits.exists ()):
        # printing error message
        print ("ERROR: Input files does not exist!")
        print ("ERROR: The file \"%s\" does not exist!" % file_fits)
        # exit the script
        sys.exit ()
        
# checking output file
# making pathlib object
path_output = pathlib.Path (file_output)
# if the file is not a FITS file, then stop the script
if not (path_output.suffix == '.fits'):
    # printing error message
    print ("ERROR: Output file must be FITS files!")
    print ("ERROR: output file = \"%s\"" % file_output)
    # exit the script
    sys.exit ()
# if the file exist, then stop the script
if (path_output.exists ()):
    # printing error message
    print ("ERROR: Output file exists!")
    print ("ERROR: output file = \"%s\"" % file_output)
    # exit the script
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()
    
# parameter for counting
i = 0

# printing information
print ("# Data criteria:")
print ("#   data type     = %s" % datatype)
print ("#   exposure time = %f sec" % exptime)
print ("#   filter name   = %s" % filter_name)
print ("#")

# a list for file names to be combined
file_selected = []

# printing information
print ("# List of files to be combined:")

# reading FITS files and constructing a data cube
for file_fits in list_input:
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]

        # reading header
        header0 = hdu0.header

        # if the FITS file is not what you want, then skip
        if ('FILTER' in header0):
            if not ( (header0['IMAGETYP'] == datatype) \
                     and (header0['EXPTIME'] == exptime) \
                     and (header0['FILTER'] == filter_name) ):
                # closing FITS file
                hdu_list.close ()
                continue
        else:
            if not ( (header0['IMAGETYP'] == datatype) \
                     and (header0['EXPTIME'] == exptime) ):
                # closing FITS file
                hdu_list.close ()
                continue

        # appending file name to the list "file_selected"
        file_selected.append (file_fits)
        
        # copying header only for the first FITS file
        if (i == 0):
            header = header0

        # reading data
        data0 = hdu0.data

    # calculation of sigma-clipped mean
    mean, median, stddev \
        = astropy.stats.sigma_clipped_stats (data0, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std')

    # normalisation of pixel data
    normalised0 = data0 / mean
    
    # constructing a data cube
    if (i == 0):
        tmp0 = normalised0
    elif (i == 1):
        cube = numpy.concatenate ( ([tmp0], [normalised0]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [normalised0]), axis=0 )
    
    # incrementing the parameter "i"
    i += 1

    # printing information
    print ("#   %s (mean = %8.2f)" % (file_fits, mean))

# printing information
print ("# Output file name: %s" % file_output)
print ("# Parameters:")
print ("#   rejection = %s" % rejection)
print ("#   threshold = %f" % threshold)
print ("#   maxiters  = %d" % maxiters)
print ("#   cenfunc   = %s" % cenfunc)

# printing status
print ("# now, combining FITS files...")

# combining images into a single co-added image
if (rejection == 'sigclip'):
    # combining using sigma clipping
    combined, median, stddev \
        = astropy.stats.sigma_clipped_stats (cube, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std', \
                                             axis=0)
elif (rejection == 'none'):
    # combining using simple mean
    combined = numpy.nanmean (cube, axis=0)

# printing status
print ("# finished combining FITS files!")

# printing status
print ("# now, writing output FITS file...")
    
# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "List of combined files:"
for fits in file_selected:
    header['comment'] = "  %s" % (fits)
header['comment'] = "Options given:"
header['comment'] = "  rejection = %s" % (rejection)
header['comment'] = "  threshold = %f sigma" % (threshold)
header['comment'] = "  maxiters  = %d" % (maxiters)
header['comment'] = "  cenfunc   = %s" % (cenfunc)

# writing a new FITS file
astropy.io.fits.writeto (file_output, combined, header=header)

# printing status
print ("# finished writing output FITS file!")
