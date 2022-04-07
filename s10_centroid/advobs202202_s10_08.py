#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/07 16:26:36 (CST) daisuke>
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
import astropy.modeling

# importing photutils module
import photutils.centroids

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.patches

# constructing parser object
desc   = 'PSF fitting for a point-source object using 2-D Gaussian profile'
parser = argparse.ArgumentParser (description=desc)

# centroid measurement technique
choices_centroid = ['com', '1dg', '2dg']

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'ocean', 'terrain', \
                'gnuplot', 'cubehelix', 'jet', 'turbo']

# adding command-line arguments
parser.add_argument ('-c', '--centroid', choices=choices_centroid, \
                     default='com', \
                     help='centroid measurement algorithm (default: com)')
parser.add_argument ('-w', '--width', type=int, default=5, \
                     help='half-width of centroid calculation box (default: 5)')
parser.add_argument ('-x', '--xinit', type=int, default=-1, \
                     help='a rough x coordinate of target')
parser.add_argument ('-y', '--yinit', type=int, default=-1, \
                     help='a rough y coordinate of target')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution in DPI (default: 450)')
parser.add_argument ('-m', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')
parser.add_argument ('-o', '--output', default='centroid.png', \
                     help='output file name (default: centroid.png)')
parser.add_argument ('file', default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
half_width  = args.width
x_init      = args.xinit
y_init      = args.yinit
centroid    = args.centroid
resolution  = args.resolution
cmap        = args.cmap
file_fits   = args.file
file_output = args.output

# making pathlib objects
path_fits   = pathlib.Path (file_fits)
path_output = pathlib.Path (file_output)

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
# if output file exists, then stop the script
if (path_output.exists ()):
    # printing message
    print ("Output file exists.")
    # exit
    sys.exit ()
# output file must be either EPS, PDF, PNG, or PS file
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("Output file must be either EPS, PDF, PNG, or PS file.")
    # exit
    sys.exit ()

# printing information
print ("#")
print ("# input parameters")
print ("#")
print ("#  input file name          = %s" % file_fits)
print ("#  half-width of search box = %f" % half_width)
print ("#  x_init                   = %f" % x_init)
print ("#  y_init                   = %f" % y_init)
print ("#  centroid technique       = %s" % centroid)
print ("#  output file name         = %s" % file_output)
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
if (centroid == 'com'):
    (x_centre, y_centre) = photutils.centroids.centroid_com (subframe)
elif (centroid == '1dg'):
    (x_centre, y_centre) = photutils.centroids.centroid_1dg (subframe)
elif (centroid == '2dg'):
    (x_centre, y_centre) = photutils.centroids.centroid_2dg (subframe)

# PSF fitting
subframe_y, subframe_x = numpy.indices (subframe.shape)
psf_init = astropy.modeling.models.Gaussian2D (x_mean=x_centre, y_mean=y_centre)
fit = astropy.modeling.fitting.LevMarLSQFitter ()
psf_fitted = fit (psf_init, subframe_x, subframe_y, subframe)

x_centre_psf = psf_fitted.x_mean.value
y_centre_psf = psf_fitted.y_mean.value
x_centre_sub = x_centre_psf
y_centre_sub = y_centre_psf
x_centre_psf += x_min
y_centre_psf += y_min
x_fwhm       = psf_fitted.x_fwhm
y_fwhm       = psf_fitted.y_fwhm
fwhm         = (x_fwhm + y_fwhm) / 2.0
amplitude    = psf_fitted.amplitude.value
theta        = psf_fitted.theta.value

# printing status
print ("# finished measuring centroid using centre-of-mass!")

# printing result
print ("#")
print ("# result of the measurement")
print ("#")
print ("#  x_centre  = %f" % x_centre_psf)
print ("#  y_centre  = %f" % y_centre_psf)
print ("#  x_fwhm    = %f" % x_fwhm)
print ("#  y_fwhm    = %f" % y_fwhm)
print ("#  amplitude = %f" % amplitude)
print ("#  theta     = %f" % theta)
print ("#")
print ("# x_fwhm, y_fwhm, fwhm")
print ("%f %f %f" % (x_fwhm, y_fwhm, fwhm) )

# printing status
print ("# now, generating a plot...")

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
im = ax.imshow (subframe, origin='lower', cmap=cmap)
fig.colorbar (im)
ax.plot (x_centre_sub, y_centre_sub, marker='+', color='red', markersize=10)

# adding a bar to represent FWHM
bar = matplotlib.patches.Rectangle (xy=(1,1), width=fwhm, height=1.0, \
                                    facecolor='green', edgecolor='white')
ax.add_patch (bar)

# saving file
fig.savefig (file_output, dpi=resolution)

# printing status
print ("# finished generating a plot!")
