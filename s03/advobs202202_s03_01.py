#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 15:10:45 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Checking a keyword IMAGETYP'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files

# processing files
for file_fits in list_files:
    # if input file is not a FITS file, then skip
    if not (file_fits[-5:] == '.fits'):
        # printing a message
        print ("The file \"%s\" is not a FITS file!" % file_fits)
        # moving to next file
        continue
    
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # closing FITS file
    hdu_list.close ()

    # check of existence of IMAGETYP keyword
    if not ('IMAGETYP' in header0):
        print ("A keyword IMAGETYP does not exist in the file \"%s\"." \
               % file_fits)

    # check of existence of EXPTIME keyword
    if not ('EXPTIME' in header0):
        print ("A keyword EXPTIME does not exist in the file \"%s\"." \
               % file_fits)
    
    # printing values of IMAGETYP and EXPTIME keywords
    print ("%s : %s (integration time = %d sec)" \
           % (file_fits, header0['IMAGETYP'], header0['EXPTIME']) )
