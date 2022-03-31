#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 23:13:14 (CST) daisuke>
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
desc   = 'carrying out flatfielding'
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

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# processing FITS files
for file_darksub in list_files:
    # making pathlib object
    path_darksub = pathlib.Path (file_darksub)
    
    # if the extension of the file is not '.fits', the we skip
    if not (path_darksub.suffix == '.fits'):
        # printing message
        print ("### file '%s' is not a FITS file! skipping..." % file_darksub)
        # skipping
        continue

    # opening FITS file
    with astropy.io.fits.open (file_darksub) as hdu_list:
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
    if not (path_darksub.stem[-2:] == '_d'):
        continue

    # appending file name to the dictionary
    dict_target[file_darksub] = {}
    dict_target[file_darksub]['filter']  = filter_name
    dict_target[file_darksub]['exptime'] = exptime

# dark subtraction

print ("#")
print ("# Processing each FITS file...")
print ("#")

# processing each FITS file
for file_darksub in sorted (dict_target.keys () ):
    # making pathlib object
    path_darksub = pathlib.Path (file_darksub)
    
    # file names
    file_flatfielded = path_darksub.stem + 'f.fits'
    file_nflat       = 'nflat_' + dict_target[file_darksub]['filter'] + '.fits'

    # if normalised flatfield does not exist, then stop the script
    path_nflat = pathlib.Path (file_nflat)
    if not (path_nflat.exists () ):
        print ("The flatfield file \"%s\" does not exist." % file_nflat)
        print ("Check the data!")
        sys.exit ()
    
    print ("# dividing %s by %s..." % (file_darksub, file_nflat) )
    print ("#   %s ==> %s" % (file_darksub, file_flatfielded) )
    
    # opening FITS file (raw data)
    with astropy.io.fits.open (file_darksub) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header

        # printing status
        print ("#     reading dark-subtracted data from \"%s\"..." \
               % file_darksub)
    
        # image of primary HDU
        # reading the data as float64
        data_darksub = hdu_list[0].data.astype (numpy.float64)

    # opening FITS file (nflat)
    with astropy.io.fits.open (file_nflat) as hdu_list:
        # header of primary HDU
        header_nflat = hdu_list[0].header

        # printing status
        print ("#     reading normalised flatfield data from \"%s\"..." \
               % file_nflat)

        # image of primary HDU
        # reading the data as float64
        data_nflat = hdu_list[0].data.astype (numpy.float64)

    # printing status
    print ("#     dividing \"%s\" by \"%s\"..." % (file_darksub, file_nflat) )

    # flatfielding
    data_flatfielded = data_darksub / data_nflat

    # printing information
    print ("#     mean value of %-32s = %8.1f ADU" \
           % (file_nflat, numpy.mean (data_nflat)) )
    print ("#     mean value of %-32s = %8.1f ADU" \
           % (file_darksub, numpy.mean (data_darksub)) )
    print ("#     mean value of %-32s = %8.1f ADU" \
           % (file_flatfielded, numpy.mean (data_flatfielded)) )

    # adding comments to new FITS file
    header['history'] = "FITS file created by the command \"%s\"" % (command)
    header['history'] = "Updated on %s" % (now)
    header['comment'] = "flatfielding was carried out"
    header['comment'] = "dark-subtracted data: %s" % (file_darksub)
    header['comment'] = "normalised flatfield data: %s" % (file_nflat)
    header['comment'] = "flatfielded data: %s" % (file_flatfielded)

    # printing status
    print ("#     writing new file \"%s\"..." % file_flatfielded)

    # writing a new FITS file
    astropy.io.fits.writeto (file_flatfielded, data_flatfielded, header=header)
