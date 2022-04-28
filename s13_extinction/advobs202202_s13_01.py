#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/27 22:11:46 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = "checking FITS header"
parser = argparse.ArgumentParser (description=desc)

# adding argument
parser.add_argument ('-d', '--dir', default='', help='reduced data directory')
parser.add_argument ('-n', '--name', default='', help='name of target object')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
dir_data    = args.dir
target_name = args.name

# checking "dir_data" and "target_name"
if (dir_data == ''):
    print ("You have to specify data directory name by using -d option!")
    sys.exit ()
if (target_name == ''):
    print ("You have to specify target object name by using -n option!")
    sys.exit ()

# making a pathlib object for "dir_data"
path_datadir = pathlib.Path (dir_data)
# if not a directory, then stop the script
if not (path_datadir.is_dir () ):
    print ("%s is not a directory!" % dir_data)
    sys.exit ()

# reading directory
list_fits = path_datadir.iterdir ()

# printing header
print ("# file name, time-obs, data type, exptime, filter, object, airmass")

# processing each FITS file
for path_fits in list_fits:
    # file name
    file_fits = str (path_fits)

    # if the file is not a FITS file, then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print ("# file '%s' is not a FITS file, skipping..." % file_fits)
        # skipping to next
        continue
    # if the file is not a reduced data, then skip
    if not (path_fits.stem[-3:] == '_df'):
        # printing message
        print ("# file '%s' is not a reduced data, skipping..." % file_fits)
        # skipping to next
        continue

    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # reading header information
        header = hdu_list[0].header

    # checking header information
    # data type should be 'LIGHT' (= object frame)
    # target object must be matched with the specified name
    if not ( (header['IMAGETYP'] == 'LIGHT') \
             and (header['OBJECT'] == target_name) ):
        # if not matched, skip
        continue

    # printing file information
    print ("%s %s %s %6.1f %s %s %5.3f" \
           % (path_fits.name, header['TIME-OBS'], header['IMAGETYP'], \
              header['EXPTIME'], header['FILTER'], header['OBJECT'], \
              header['AIRMASS']) )
