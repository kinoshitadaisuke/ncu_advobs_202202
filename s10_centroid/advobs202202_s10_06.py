#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/07 15:26:03 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# importing photutils module
import photutils.centroids

# constructing parser object
desc   = 'centroid measurement using 2-D Gaussian fitting'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-w', '--width', type=int, default=5, \
                     help='half-width of centroid calculation box (default: 5)')
parser.add_argument ('-x', '--xinit', type=int, default=-1, \
                     help='a rough x coordinate of target')
parser.add_argument ('-y', '--yinit', type=int, default=-1, \
                     help='a rough y coordinate of target')
parser.add_argument ('file', nargs=1, default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
half_width = args.width
x_init     = args.xinit
y_init     = args.yinit
file_fits  = args.file[0]

# making pathlib object
path_fits = pathlib.Path (file_fits)

# checking input FITS file name
if (file_fits == ''):
    # printing message
    print ("You need to specify input file name.")
    # exit
    sys.exit ()
# if input file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()
# if input file does not exist, then stop the script
if not (path_fits.exists ()):
    # printing message
    print ("Input file does not exist.")
    # exit
    sys.exit ()

# printing information
print ("#")
print ("# input parameters")
print ("#")
print ("#  input file name = %s" % file_fits)
print ("#  half-width of search box = %f" % half_width)
print ("#  x_init = %f" % x_init)
print ("#  y_init = %f" % y_init)
print ("#")

# printing status
print ("# now, reading FITS file...")

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading FITS header
    header = hdu_list[0].header

    # image size
    image_size_x = header['NAXIS1']
    image_size_y = header['NAXIS2']
    
    # checking x_init and y_init
    if not ( (x_init > 0) and (x_init < image_size_x) ):
        print ("Input x_init value exceed image size.")
        sys.exit ()
    if not ( (y_init > 0) and (y_init < image_size_y) ):
        print ("Input y_init value exceed image size.")
        sys.exit ()
    
    # reading FITS image data
    data = hdu_list[0].data

# printing status
print ("# finished reading FITS file!")

# printing status
print ("# now, extracting image around the target object...")

# region of calculation
x_min = x_init - half_width
x_max = x_init + half_width + 1
y_min = y_init - half_width
y_max = y_init + half_width + 1

# extraction of subframe for calculation
subframe = data[y_min:y_max, x_min:x_max]

# printing status
print ("# finished extracting image around the target object!")

# printing status
print ("# now, subtracting background...")

# rough background subtraction
subframe -= numpy.median (subframe)

# printing status
print ("# finished subtracting background!")

# printing status
print ("# now, measuring centroid using centre-of-mass...")

# centroid calculation
#(x_centre, y_centre) = photutils.centroids.centroid_com (subframe)
#(x_centre, y_centre) = photutils.centroids.centroid_1dg (subframe)
(x_centre, y_centre) = photutils.centroids.centroid_2dg (subframe)
x_centre += x_min
y_centre += y_min

# printing status
print ("# finished measuring centroid using centre-of-mass!")

# printing result
print ("#")
print ("# result of the measurement")
print ("#")
print ("%f %f" % (x_centre, y_centre) )
