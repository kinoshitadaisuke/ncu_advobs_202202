#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 22:58:44 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'listing dark subtracted object frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
default_exptime_keyword  = 'EXPTIME'
default_timeobs_keyword  = 'TIME-OBS'
default_dateobs_keyword  = 'DATE-OBS'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-d', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('-t', '--timeobs', default=default_timeobs_keyword, \
                     help='FITS keyword for time-obs')
parser.add_argument ('-y', '--dateobs', default=default_dateobs_keyword, \
                     help='FITS keyword for date-obs')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.datatype
keyword_exptime  = args.exptime
keyword_timeobs  = args.timeobs
keyword_dateobs  = args.dateobs
list_files       = args.files

# declaring an empty dictionary for storing FITS file information
dict_target = {}

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
    # date-obs
    if (keyword_dateobs in header):
        date_obs = header[keyword_dateobs]
    else:
        date_obs = "__NONE__"
    # time-obs
    if (keyword_timeobs in header):
        time_obs = header[keyword_timeobs]
    else:
        time_obs = "__NONE__"

    # if the data type is not "LIGHT", then we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # if the file name is not "*_d.fits", then we skip the file
    if not (path_fits.stem[-2:] == '_d'):
        continue

    # appending FITS header information to the dictionary
    if not (filter_name in dict_target):
        dict_target[filter_name] = {}
    dict_target[filter_name][file_fits] = {}
    dict_target[filter_name][file_fits]['exptime']  = exptime
    dict_target[filter_name][file_fits]['date-obs'] = date_obs
    dict_target[filter_name][file_fits]['time-obs'] = time_obs

# printing FITS file list
print ("List of FITS files for flatfielding:")
for filter_name in sorted (dict_target.keys () ):
    # normalised flatfield file name
    nflat = "nflat_%s.fits" % filter_name
    # making pathlib object
    path_nflat = pathlib.Path (nflat)
    # if normalised flatfield does not exist, then stop the script
    if not (path_nflat.exists () ):
        print ("The flatfield file \"%s\" does not exist." % nflat)
        print ("Check the data!")
        sys.exit ()
    # printing information
    print ("  %s band data:"% filter_name)
    print ("    normalised flatfield = %s" % nflat)
    for file_fits in sorted (dict_target[filter_name].keys () ):
        flatfielded = path_fits.stem + "f.fits"
        print ("      %s / %s" % (file_fits, nflat) )
        print ("          ==> %s" % flatfielded)

# counting total number of files for flatfielding
total_files = 0
for filter_name in sorted (dict_target.keys () ):
    n_files = len (dict_target[filter_name].keys () )
    print ("  %s band data: %d files" % (filter_name, n_files) )
    total_files += n_files
# printing information
print ("Total number of files to be processed:")
print ("  Total number of files: %d files" % total_files)
