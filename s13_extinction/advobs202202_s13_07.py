#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/28 14:23:54 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing subprocess module
import subprocess

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = "carrying out aperture photometry for multiple FITS files"
parser = argparse.ArgumentParser (description=desc)

# adding argument
parser.add_argument ('-f', '--filter', default='', help='filter name')
parser.add_argument ('-n', '--name', default='', help='name of target object')
parser.add_argument ('-e1', '--exptime-min', type=float, default=5.0, \
                     help='minimum exposure time for use')
parser.add_argument ('-e2', '--exptime-max', type=float, default=90.0, \
                     help='maximum exposure time for use')
parser.add_argument ('-a', '--aperture', type=float, default=2.0, \
                     help='aperture radius in FWHM (default: 2.0)')
parser.add_argument ('-r', '--ra', type=float, default=-999.999, \
                     help='RA in degree')
parser.add_argument ('-d', '--dec', type=float, default=-999.999, \
                     help='Dec in degree')
parser.add_argument ('-o', '--object', default='', \
                     help='target object name')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
target_name          = args.name
filter_name          = args.filter
exptime_min          = args.exptime_min
exptime_max          = args.exptime_max
aperture_radius_fwhm = args.aperture
target_ra_deg        = args.ra
target_dec_deg       = args.dec
files_fits           = args.files

# checking "target_name", and "filter_name"
if (target_name == ''):
    # printing message
    print ("You have to specify target object name by using -n option!")
    # exit
    sys.exit ()
if (filter_name == ''):
    # printing message
    print ("You have to specify filter name by using -f option!")
    # exit
    sys.exit ()

# processing each FITS file
for file_fits in files_fits:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    # file name
    filename = path_fits.name
    name_list = file_fits.split ('_')
    frame_id = int (name_list[-2])

    # output data file name
    file_output  = "phot_%s_%s_%04d.phot" % (target_name, filter_name, frame_id)
    # output graphic file name
    file_graphic = "phot_%s_%s_%04d.pdf" % (target_name, filter_name, frame_id)

    # if the file is not a FITS file, then skip
    if not (path_fits.suffix == '.fits'):
        # skip
        continue
    # if the file is not a reduced data, then skip
    if not (path_fits.stem[-3:] == '_df'):
        # skip
        continue

    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # reading header information
        header = hdu_list[0].header
    # checking header information
    if not ( (header['IMAGETYP'] == 'LIGHT') \
             and (header['FILTER'] == filter_name) \
             and (header['EXPTIME'] > exptime_min) \
             and (header['EXPTIME'] < exptime_max) ):
        continue

    # command to carry out photometry
    command_phot \
        = ("./advobs202202_s13_06.py -i %s -r %f -d %f -a %f -o %s -g %s" \
           % (file_fits, target_ra_deg, target_dec_deg, \
              aperture_radius_fwhm, file_output, file_graphic) )

    # execute the command
    subprocess.run (command_phot, shell=True)
