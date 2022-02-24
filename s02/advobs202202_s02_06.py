#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 15:40:32 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'opening FITS files and printing HDU information'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='list of FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters
list_fits = args.files

# processing FITS files one-by-one
for file_fits in list_fits:
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # printing HDU list information
    print (hdu_list.info () )

    # closing FITS file
    hdu_list.close ()
