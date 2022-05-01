#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/17 23:18:34 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# importing subprocess module
import subprocess

# construction of parser object
desc = 'Dark subtraction for multiple FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_datatype = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter   = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                    'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--datatype', choices=choices_datatype, \
                     default='LIGHT', \
                     help='accepted data type (default: LIGHT)')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=5.0, help='accepted exposure time (default: 5)')
parser.add_argument ('-f', '--filter', choices=choices_filter, \
                     default='__NONE__', help='accepted data type')
parser.add_argument ('-s', '--subtrahend', default='dark.fits', \
                     help='subtrahend FITS file')
parser.add_argument ('files_minuend', nargs='+', help='minuend FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
files_minuend   = args.files_minuend
file_subtrahend = args.subtrahend
datatype        = args.datatype
exptime         = args.exptime
filter_name     = args.filter

# making pathlib object
path_subtrahend = pathlib.Path (file_subtrahend)
# if the file is not a FITS file, then stop the script
if not (path_subtrahend.suffix == '.fits'):
    # printing error message
    print ("ERROR: the file \"%s\" is not a FITS file!" % file_subtrahend)
    # exit
    sys.exit ()
# if the file does not exist, then stop the script
if not (path_subtrahend.exists ()):
    # printing error message
    print ("ERROR: the file \"%s\" does not exist!" % file_subtrahend)
    # exit
    sys.exit ()

# processing each file
for file_minuend in files_minuend:
    # making a pathlib object
    path_minuend = pathlib.Path (file_minuend)
    # if the file is not a FITS file, then skip
    if not (path_minuend.suffix == '.fits'):
        # printing message
        print ("# The file \"%s\" is not a FITS file! Skipping...")
        # skipping
        continue
    # if the file does not exist, then skip
    if not (path_minuend.exists ()):
        # printing message
        print ("# The file \"%s\" does not exist! Skipping...")
        # skipping
        continue

    # opening FITS file
    with astropy.io.fits.open (file_minuend) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]

        # reading header
        header0 = hdu0.header

    # if the FITS file is not what you want, then skip
    if ('FILTER' in header0):
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) \
                 and (header0['FILTER'] == filter_name) ):
            continue
    else:
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) ):
            continue
        
    # output file name
    file_basename = path_minuend.name
    file_output   = path_minuend.stem + '_d.fits'
        
    # printing message
    print ("#")
    print ("# Now subtracting \"%s\"" % file_subtrahend)
    print ("#   from \"%s\"" % file_minuend)
    print ("#   and creating \"%s\"" % file_output)
    print ("#")

    # command
    command = "%s %s %s %s" % ("./advobs202202_s05_07.py", file_minuend, \
                               file_subtrahend, file_output)

    # executing command
    subprocess.run (command, shell=True)
