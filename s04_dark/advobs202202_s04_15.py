#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 23:57:16 (CST) daisuke>
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

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc = 'Combining images'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='mean', \
                     help='method to estimate centre value (default: mean)')
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

# command name
command = sys.argv[0]

# checking number of intput FITS files
if ( len (list_input) < 2 ):
    # if the number of input files is less than 2, then stop the script
    print ("ERROR: Number of input files must be 2 or more!")
    # exit the script
    sys.exit ()

# checking input files
for file_fits in list_input:
    # if the file is not a FITS file, then stop the script
    if not (file_fits[-5:] == '.fits'):
        # printing error message
        print ("ERROR: Input files must be FITS files!")
        print ("ERROR: The file \"%s\" is not a FITS file!" % file_fits)
        # exit the script
        sys.exit ()
    # existence check
    path_fits = pathlib.Path (file_fits)
    if not (path_fits.exists ()):
        print ("ERROR: file \"%s\" does not exist!")
        # exit the script
        sys.exit ()
        
# checking output file
# if the file is not a FITS file, then stop the script
if not (file_output[-5:] == '.fits'):
    # printing error message
    print ("ERROR: Output file must be FITS files!")
    # exit the script
    sys.exit ()
# existence check of output file
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing error message
    print ("ERROR: output file \"%s\" exists!" % file_output)
    # exit the script
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()

# printing input parameters
print ("#")
print ("# Input parameters:")
print ("#   input FITS files:")
for file_fits in list_input:
    print ("#     %s" % file_fits)
print ("#   output FITS file = %s" % file_fits)
print ("#   rejection method = %s" % rejection)
print ("#   threshold        = %f sigma" % threshold)
print ("#   cenfunc          = %s" % cenfunc)
print ("#   maxiters         = %d" % maxiters)
print ("#")

# reading FITS files and constructing a data cube
for i in range (len (list_input)):
    # file name
    file_fits = list_input[i]

    # printing status
    print ("# now, reading FITS file \"%s\"..." % file_fits)
        
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]

    # reading header only for the first FITS file
    if (i == 0):
        header0 = hdu0.header

    # reading data
    data0 = hdu0.data

    # closing FITS file
    hdu_list.close ()

    # constructing a data cube
    if (i == 0):
        tmp0 = data0
    elif (i == 1):
        cube = numpy.concatenate ( ([tmp0], [data0]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [data0]), axis=0 )

    # printing status
    print ("# finished reading FITS file \"%s\"!" % file_fits)

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
print ("# now, writing FITS file \"%s\"..." % file_output)

# adding comments to the header
header0['history'] = "FITS file created by the command \"%s\"" % (command)
header0['history'] = "Updated on %s" % (now)
header0['comment'] = "List of combined files:"
for fits in list_input:
    header0['comment'] = "  %s" % (fits)
header0['comment'] = "Options given:"
header0['comment'] = "  rejection = %s" % (rejection)
header0['comment'] = "  threshold = %f sigma" % (threshold)
header0['comment'] = "  maxiters  = %d" % (maxiters)
header0['comment'] = "  cenfunc   = %s" % (cenfunc)

# writing a new FITS file
astropy.io.fits.writeto (file_output, combined, header=header0)

# printing status
print ("# finished writing FITS file \"%s\"!" % file_output)
