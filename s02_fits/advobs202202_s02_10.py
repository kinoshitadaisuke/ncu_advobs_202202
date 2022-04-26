#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 16:37:45 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'opening FITS files and reading image data'
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

# data of primary HDU
data0 = hdu0.data

# closing FITS file
hdu_list.close ()

# printing a value of a pixel [1024,1024]
print ("image[1024,1024] =", data0[1024,1024])

# printing values of 10x10 subframe of near the centre of the image
print ("image[1024:1034,1024:1034] =")
print (data0[1024:1034,1024:1034])
