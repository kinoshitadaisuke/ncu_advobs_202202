#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/18 00:26:42 (CST) daisuke>
#

# importing argparse
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# importing subprocess module
import subprocess

# construction of parser object
desc = 'Subtracting dark from raw flatfield'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_filter = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                  'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-f', '--filter', choices=choices_filter, \
                     default='__NONE__', help='filter')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files  = args.files
filter_name = args.filter

# processing files one-by-one
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    
    # if the extension of the file is not '.fits', then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print ("# the file \"%s\" is not a FITS file, skipping..." % fits_fits)
        # skipping
        continue

    # if the file does not exist, then skip
    if not (path_fits.exists ()):
        # printing message
        print ("# the file \"%s\" does not exist, skipping..." % fits_fits)
        # skipping
        continue

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
    
        # header of primary HDU
        header0 = hdu0.header

    # skip, if the data type is not 'FLAT'
    if not (header0['IMAGETYP'] == 'FLAT'):
        # printing message
        print ("# the file \"%s\" is not a flatfield, skipping..." % file_fits)
        # skipping
        continue

    # skip, if filter is not the one specified by the command-line argument
    if not (header0['FILTER'] == filter_name):
        # printing message
        print ("# %s is not %s band data, skipping..." \
               % (file_fits, filter_name) )
        # skipping
        continue

    # exposure time
    exptime = float (header0['EXPTIME'])

    # combined dark frame file name
    file_dark = "dark_%04d.fits" % exptime

    # output FITS file name
    file_output = path_fits.stem + '_d.fits'

    # dark subtraction command
    command = "%s %s %s %s" % ('./advobs202202_s05_07.py', file_fits, \
                               file_dark, file_output)

    # printing message
    print ("#")
    print ("# Now subtracting \"%s\"" % file_fits)
    print ("#   from \"%s\"" % file_dark)
    print ("#   and creating \"%s\"" % file_output)
    print ("#")

    # executing command
    subprocess.run (command, shell=True)
