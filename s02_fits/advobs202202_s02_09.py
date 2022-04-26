#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 16:27:34 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'Generating a simple observing log'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_keyword = 'TIME-OBS,IMAGETYP,OBJECT,EXPTIME,FILTER'
parser.add_argument ('-k', '--keyword', default=default_keyword, \
                     help='a comma-separated list of FITS keywords')
parser.add_argument ('files', nargs='+', help='list of FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword = args.keyword
files   = args.files

# a list of keywords
list_keyword = keyword.split (',')

# processing files
for file in files:
    # if the extension of the file is not '.fits', then skip
    if (file[-5:] != '.fits'):
        continue

    # file name
    path = file.split ('/')
    filename = path[-1]

    # opening FITS file
    hdu_list = astropy.io.fits.open (file)

    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # gathering information from FITS header
    record = filename
    for key in list_keyword:
        if key in header0:
            value = str (header0[key])
        else:
            value = "__NONE__"
        record += " %8s" % value

    # closing FITS file
    hdu_list.close ()

    # printing information
    print (record)
    
