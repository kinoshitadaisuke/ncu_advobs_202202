#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 16:13:09 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'opening FITS files and printing values of selected header keywords'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-k', '--keywords', \
                     help='list of keywords (e.g. "NAXIS1,NAXIS2,IMAGETYP")')
parser.add_argument ('files', nargs='+', help='list of FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters
list_fits = args.files
keywords  = args.keywords

# keywords
list_keywords = keywords.split (',')

# processing files one-by-one
for file_fits in list_fits:
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]

    # header of primary HDU
    header0 = hdu0.header

    # closing FITS file
    hdu_list.close ()

    # printing specific keywords and their values in FITS header
    print ("file = %s" % file_fits)
    for keyword in list_keywords:
        print ("  %-8s ==> %s" % (keyword, header0[keyword]) )
