#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 15:39:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Checking filters used for the observation'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-t', '--type', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.type
list_files       = args.files

# declaring an empty dictionary for filter names
dict_filters = {}

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

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

    # data type
    if (keyword_datatype in header):
        datatype = header[keyword_datatype]
    else:
        datatype = "__NONE__"

    # if the data type is not "LIGHT", the we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # filter
    if (keyword_filter in header):
        filter_name = header[keyword_filter]
    else:
        filter_name = "__NONE__"

    # if the filter name is not in the dictionary "dict_filters", then append
    # if the filter name is in the dictionary "dict_filters", then add 1
    if not (filter_name in dict_filters):
        # appending "filter_name" to the dictionary "dict_filters"
        dict_filters[filter_name] = 1
    else:
        # add 1
        dict_filters[filter_name] += 1

# printing filter names and number of images
print ("List of filters used for acquiring object frames:")
# for each filter name
for filter_name in sorted (dict_filters.keys () ):
    # printing filter name and number of images
    print ("  %s (%d files)" % (filter_name, dict_filters[filter_name]) )
