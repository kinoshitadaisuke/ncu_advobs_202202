#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/26 22:03:55 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# import pathlib module
import pathlib

# importing astropy module
import astropy.table

# constructing parser object
desc   = 'reading table from a file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-c', '--catalogue-file', default='', \
                     help='input catalogue file name')

# command-line argument analysis
args = parser.parse_args ()

# catalogue file name
file_catalogue = args.catalogue_file

# making pathlib object
path_catalogue = pathlib.Path (file_catalogue)

# check of catalogue file name
if (file_catalogue == ''):
    # printing message
    print ("ERROR: Catalogue file name must be specified.")
    # exit
    sys.exit ()

# existence check of catalogue file
if not (path_catalogue.exists () ):
    # printing message
    print ("ERROR: Catalogue file '%s' does not exist." % (file_catalogue) )
    # exit
    sys.exit ()

# reading catalogue from a file
table_source = astropy.table.Table.read (file_catalogue, \
                                         format='ascii.commented_header')

# printing table
print (table_source)
