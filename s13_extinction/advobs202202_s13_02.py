#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/27 22:36:14 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing shutil module
import shutil

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = "copying FITS files"
parser = argparse.ArgumentParser (description=desc)

# adding argument
parser.add_argument ('-d', '--dir', default='', help='reduced data directory')
parser.add_argument ('-n', '--name', default='', help='name of target object')
parser.add_argument ('-t', '--to', default='', help='target directory name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
dir_data        = args.dir
target_name     = args.name
dir_destination = args.to

# checking "dir_data" and "target_name"
if (dir_data == ''):
    print ("You have to specify data directory name by using -d option!")
    sys.exit ()
if (dir_destination == ''):
    print ("You have to specify destination directory name by using -t option!")
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

# making a pathlib object for "dir_destination"
path_destination = pathlib.Path (dir_destination)

# if directory does not exist, then make a directory
if not (path_destination.exists ()):
    # making a directory
    path_destination.mkdir (parents=True, exist_ok=True)

# reading directory
list_fits = path_datadir.iterdir ()

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

    # printing status
    print ("Now copying the file '%s' to '%s'..." \
           % (path_fits.name, dir_destination) )

    # copying the file to current directory
    shutil.copy2 (file_fits, path_destination)

    # printing status
    print ("Finished copying the file '%s' to '%s'!" \
           % (path_fits.name, dir_destination) )
