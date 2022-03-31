#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 15:21:51 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Generating a list of FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_keyword = 'TIME-OBS,IMAGETYP,EXPTIME,FILTER,OBJECT'
parser.add_argument ('-k', '--keyword', default=default_keyword, \
                     help='a list of keyword to check')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword    = args.keyword
list_files = args.files

# a list of FITS keywords
list_keyword = keyword.split (',')

# processing FITS files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    
    # if the extension of the file is not '.fits', the we skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print ("### file '%s' is not a FITS file! skipping..." % file_fits)
        # skipping
        continue

    # file name
    # for example, file = '/some/where/in/the/disk/abc0123.fits'
    # filename ==> 'abc0123.fits'
    filename = path_fits.name

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

    # gathering information from FITS header
    record = "%-24s" % filename
    for key in list_keyword:
        # check of existence of keyword
        if key in header:
            # obtaining a value for given keyword
            value = str (header[key])
        else:
            # if a given key does not exist, then store "__NONE__"
            value = "__NONE__"
        # appending the value to the string "record"
        if (key == 'DATE-OBS'):
            record += "  %-10s" % value
        elif (key == 'TIME-OBS'):
            record += "  %-8s" % value
        elif (key == 'IMAGETYP'):
            record += "  %-5s" % value
        elif (key == 'EXPTIME'):
            record += "  %6.1f" % float (value)
        elif (key == 'FILTER'):
            record += "  %-16s" % value
        else:
            record += "  %s" % value

    # printing information
    print (record)
