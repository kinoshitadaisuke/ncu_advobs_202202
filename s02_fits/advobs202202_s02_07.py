#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 23:45:14 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'opening FITS files and printing header information'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='name of FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.file

# opening FITS file
hdu_list = astropy.io.fits.open (file_fits)

# primary HDU
hdu0 = hdu_list[0]

# header of primary HDU
header0 = hdu0.header

# closing FITS file
hdu_list.close ()

# printing FITS header
print (repr (header0))
