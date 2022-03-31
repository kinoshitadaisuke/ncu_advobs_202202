#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 16:21:50 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Checking exposure time of object and flatfield frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_exptime_keyword  = 'EXPTIME'
default_datatype_keyword = 'IMAGETYP'
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('-t', '--type', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_exptime  = args.exptime
keyword_datatype = args.type
list_files       = args.files

# declaring a dictionary for filter names
dict_exptime_object = {}
dict_exptime_flat   = {}
dict_exptime_dark   = {}

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

    # if the data type is not "LIGHT" or "FLAT" or "DARK", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') \
             or (datatype == 'DARK') ):
        continue

    # exposure time
    if (keyword_exptime in header):
        exptime = header[keyword_exptime]
    else:
        exptime = -999.99

    if (datatype == 'LIGHT'):
        # object frames
        if not (exptime in dict_exptime_object):
            # appending exptime to the dictionary "dict_exptime_object"
            dict_exptime_object[exptime] = 1
        else:
            # add 1
            dict_exptime_object[exptime] += 1
    elif (datatype == 'FLAT'):
        # flatfield frames
        if not (exptime in dict_exptime_flat):
            # appending exptime to the dictionary "dict_exptime_flat"
            dict_exptime_flat[exptime] = 1
        else:
            # add 1
            dict_exptime_flat[exptime] += 1
    elif (datatype == 'DARK'):
        # dark frames
        if not (exptime in dict_exptime_dark):
            # appending exptime to the dictionary "dict_exptime_dark"
            dict_exptime_dark[exptime] = 1
        else:
            # add 1
            dict_exptime_dark[exptime] += 1

# printing information
print ("Exposure time information:")
print ("  object frames:")
for exptime in sorted (dict_exptime_object.keys () ):
    print ("    %.3f sec exposure ==> %4d frames" \
           % (float (exptime), dict_exptime_object[exptime]) )
    print ("      Do we have dark frames of %.3f sec exposure?" \
           % float (exptime) )
    if (exptime in dict_exptime_dark):
        print ("      Yes, we do have dark frames of %.3f sec exposure." \
               % float (exptime) )
        print ("      We have %d frames of %.3f sec dark frames." \
               % (dict_exptime_dark[exptime], float (exptime) ) )
    else:
        print ("      No, we do not have dark frames of %.3f sec exposure." \
               % float (exptime) )
        print ("      ERROR! Check the data.")
print ("  flatfield frames:")
for exptime in sorted (dict_exptime_flat.keys () ):
    print ("    %.3f sec exposure ==> %4d frames" \
           % (float (exptime), dict_exptime_flat[exptime]) )
    print ("      Do we have dark frames of %.3f sec exposure?" \
           % float (exptime) )
    if (exptime in dict_exptime_dark):
        print ("      Yes, we do have dark frames of %.3f sec exposure." \
               % float (exptime) )
        print ("      We have %d frames of %.3f sec dark frames." \
               % (dict_exptime_dark[exptime], float (exptime) ) )
    else:
        print ("      No, we do not have dark frames of %.3f sec exposure." \
               % float (exptime) )
        print ("      ERROR! Check the data.")
print ("  Summary of dark frames:")
list_exptime = list ( dict_exptime_object.keys () ) \
    + list ( dict_exptime_flat.keys () )
complete = 1
for exptime in sorted (list_exptime):
    if (exptime in dict_exptime_dark):
        print ("    %8.3f sec dark frames ==> %4d frames are found." \
               % (float (exptime), dict_exptime_dark[exptime] ) )
    else:
        print ("    %8.3f sec dark frames ==> NOT found, check the data!" \
               % (float (exptime) ) )
        complete = 0
if (complete):
    print ("Looks OK. All the necessary dark frames exist.")
else:
    print ("Some dark frames are missing. Check the data!")
