#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 21:41:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'carrying out dark subtraction'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
default_exptime_keyword  = 'EXPTIME'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-d', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.datatype
keyword_exptime  = args.exptime
list_files       = args.files

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# processing FITS files
for file_raw in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_raw)

    # if the extension of the file is not '.fits', the we skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print ("### file '%s' is not a FITS file! skipping..." % file_fits)
        # skipping
        continue

    # opening FITS file
    with astropy.io.fits.open (file_raw) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

    # data type
    if (keyword_datatype in header):
        datatype = header[keyword_datatype]
    else:
        datatype = "__NONE__"
    # exptime
    if (keyword_exptime in header):
        exptime = header[keyword_exptime]
    else:
        exptime = -999.99

    # filter name
    if (keyword_filter in header):
        filter_name = header[keyword_filter]
    else:
        filter_name = "__NONE__"

    # if the data type is not "LIGHT" or "FLAT", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        continue

    # appending file name to the dictionary
    dict_target[file_raw] = {}
    dict_target[file_raw]['filter']  = filter_name
    dict_target[file_raw]['exptime'] = exptime

# printing FITS file list
print ("# List of FITS files for dark subtraction:")
for file_raw in sorted (dict_target.keys () ):
    print ("#   %s (%s, %d sec)" % (file_raw, \
                                  dict_target[file_raw]['filter'],
                                  dict_target[file_raw]['exptime']) )
print ("# Total number of FITS files for dark subtraction:")
print ("#   %d files" % len (dict_target) )

# dark subtraction

print ("#")
print ("# Processing each FITS file...")
print ("#")

# processing each FITS file
for file_raw in sorted (dict_target.keys () ):
    # making pathlib object
    path_raw = pathlib.Path (file_raw)
    
    # file name of dark subtracted FITS file
    file_subtracted = path_raw.stem + '_d.fits'
    
    print ("# subtracting dark from %s..." % file_raw)
    print ("#   %s ==> %s" % (file_raw, file_subtracted) )
    
    
    # opening FITS file (raw data)
    with astropy.io.fits.open (file_raw) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

        # printing status
        print ("#     reading raw data from \"%s\"..." % file_raw)
    
        # image of primary HDU
        # reading the data as float64
        data_raw = hdu_list[0].data.astype (numpy.float64)

    # exptime
    exptime = header[keyword_exptime]

    # dark file name
    file_dark = "dark_%04d.fits" % (int (exptime) )

    # making pathlib object
    path_dark = pathlib.Path (file_dark)

    # checking whether dark file exists
    # if dark file does not exist, then stop the script
    if not (path_dark.exists () ):
        # printing message
        print ("The dark file \"%s\" is NOT found." % file_dark)
        print ("Check the data!")
        # exit
        sys.exit ()

    # opening FITS file (dark)
    with astropy.io.fits.open (file_dark) as hdu_list:
        # header of primary HDU
        header_dark = hdu_list[0].header

        # checking exptime of dark frame
        exptime_dark = header_dark[keyword_exptime]

        # if exptime_dark is not the same as exptime, then stop the script
        if not (exptime == exptime_dark):
            # printing message
            print ("Exposure times of raw frame and dark frame are NOT same.")
            print ("Check the data!")
            # exit
            sys.exit ()
    
        # printing status
        print ("#     reading dark data from \"%s\"..." % file_dark)

        # image of primary HDU
        # reading the data as float64
        data_dark = hdu_list[0].data.astype (numpy.float64)

    # printing status
    print ("#     subtracting dark from \"%s\"..." % file_raw)

    # dark subtraction
    data_subtracted = data_raw - data_dark

    # printing status
    print ("#     mean value of raw data             = %8.1f ADU" \
           % numpy.ma.mean (data_raw))
    print ("#     mean value of dark data            = %8.1f ADU" \
           % numpy.ma.mean (data_dark))
    print ("#     mean value of dark subtracted data = %8.1f ADU" \
           % numpy.ma.mean (data_subtracted))

    # adding comments to new FITS file
    header['history'] = "FITS file created by the command \"%s\"" % (command)
    header['history'] = "Updated on %s" % (now)
    header['comment'] = "dark subtraction was carried out"
    header['comment'] = "raw data: %s" % (file_raw)
    header['comment'] = "dark data: %s" % (file_dark)
    header['comment'] = "dark subtracted data: %s" % (file_subtracted)

    # printing status
    print ("#     writing new file \"%s\"..." % file_subtracted)

    # writing a new FITS file
    astropy.io.fits.writeto (file_subtracted, data_subtracted, header=header)

    # printing status
    print ("#     writing new file \"%s\" done!" % file_subtracted)
